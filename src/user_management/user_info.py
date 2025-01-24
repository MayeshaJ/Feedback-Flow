import hashlib
import os
from src.app_logic.app_logic import User, Review, Topic
from src.user_management.session_management import SessionManager
from src.data_management.object_mapper import ObjectMapper

class UserInfo:
    def __init__(self, db_path: str):
        """
        Initializes a UserInfo instance.

        Args:
            db_path (str): The path to the database where user information is stored.
        """
        self.db_path = db_path
        self.object_mapper = ObjectMapper(self.db_path)
        self.session_manager = SessionManager(self.db_path)

    def register(self, username, email, password):
        """
        Registers a new user with the provided username, email, and password.

        Args:
            username (str): The username of the user to be registered.
            email (str): The email address of the user to be registered.
            password (str): The password of the user to be registered.

        Returns:
            User: The User object representing the registered user.
        """
        hashed_password = self._hash_password(password)
        user = User(username, email, hashed_password)
        result = self.object_mapper.add(user)
        self.session_manager.create_session(user.id, is_active=0)
        return result

    def login(self, username, password):
        """
        Logs in a user with the provided username and password.

        Args:
            username (str): The username of the user trying to log in.
            password (str): The password of the user trying to log in.

        Returns:
            SessionManager: The SessionManager object if login is successful, None otherwise.
        """

        users = self.object_mapper.get(User)
        print(f"Users:{users}\nID: {users[0].id}")
        for user in users:
            if user.username == username and self._verify_password(user.hashed_password, password):
                user_session = self.session_manager.get_user_session(user.id)
                print(f"User session: {user_session}")
                if user_session:
                    user_session.is_active = 1
                    return user_session.id
                else:
                    new_session = self.session_manager.create_session(user.id)
                    new_session.is_active =1
                    return new_session.id
        return None

    def logout(self, id):
        """
        Logs out a user by invalidating the session with the given session ID.

        Args:
            id (str): The ID of the session to be invalidated.
        """
        session = self.session_manager.get_session(id)
        if session:
            session.is_active = 0
            self.session_manager.update_session(session)

    def _hash_password(self, password, salt=None):
        """
        Hashes the provided password using a salt.

        Args:
            password (str): The password to be hashed.
            salt (bytes, optional): The salt to be used for hashing (default is None).

        Returns:
            str: The hashed password.
        """
        if salt is None:
            salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + hashed_password

    def _verify_password(self, stored_password, provided_password):
        """
        Verifies if the provided password matches the stored (hashed) password.

        Args:
            stored_password (str): The stored (hashed) password.
            provided_password (str): The password provided for verification.

        Returns:
            bool: True if the provided password matches the stored password, False otherwise.
        """
        salt = stored_password[:16]
        return stored_password == self._hash_password(provided_password, salt)

    def search_review(self, query):
        """
        Search for reviews based on query.

        Args:
            Query made for a topic or username

        Returns:
            A list of Review objects that match the search criteria.
        """
        if not query:
            raise ValueError("Query cannot be empty.")

        result = []
        all_reviews = self.object_mapper.get(Review)  # This retrieves all reviews.
        all_topics = self.object_mapper.get(Topic)  # This retrieves all topics.
        all_users = self.object_mapper.get(User)  # This retrieves all users

        for review in all_reviews:
            for user in all_users:
                if user.id == review.user_id and query in user.username:
                    result.append(review)
            for topic in all_topics:
                if topic.id == review.topic_id and query in topic.name:
                    result.append(review)
        return result
