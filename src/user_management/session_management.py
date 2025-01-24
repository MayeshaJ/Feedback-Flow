from src.data_management.object_mapper import ObjectMapper
from src.app_logic.app_logic import Session

class SessionManager:
    """Manages user sessions, including creation, retrieval, and updating of session data.

    The SessionManager interacts with a database to persist session information
    using an ObjectMapper to translate between Session objects and database records.

    Attributes:
        db_path (str): The path to the database where session data is stored.
        object_mapper (ObjectMapper): An instance of ObjectMapper to handle database operations.
    """

    def __init__(self, db_path: str):
        """Initializes a new SessionManager instance.

        Args:
            db_path (str): The path to the database where session data is stored.
        """
        self.db_path = db_path
        self.object_mapper = ObjectMapper(self.db_path)

    def create_session(self, user_id: int, is_active: int = 1):
        """Creates a new session for a user.

        Args:
            user_id (int): The ID of the user for whom the session is created.
            is_active (int, optional): A flag indicating whether the session is active 
            (default is 1).

        Returns:
            Session: The created session object.
        """
        session = Session(user_id=user_id, is_active=is_active)
        self.object_mapper.add(session)
        return session

    def get_session(self, id: str):
        """
        Retrieves a session by its ID.

        Args:
            id (str): The ID of the session to retrieve.

        Returns:
            Session: The session object if found, None otherwise.
        """
        return self.object_mapper.get(Session, id)

    def get_user_session(self, user_id: int):
        """Retrieves the session associated with a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Session: The session object if found, None otherwise.
        """
        sessions = self.object_mapper.get(Session)
        for session in sessions:
            if session.user_id == user_id:
                session.is_active = 1
                self.update_session(session)
                return session
        return None

    def update_session(self, session):
        """Updates a session.

        Args:
            session (Session): The session object to update.
        """
        self.object_mapper.add(session)
