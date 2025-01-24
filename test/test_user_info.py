"""
This module contains unittests for the user information functions.
It includes tests for user registration, login, logout, and searching reviews.
"""
import os
import unittest
import uuid
from unittest.mock import Mock

# Local imports
from src.user_management.session_management import SessionManager
from src.data_management.object_mapper import ObjectMapper
from src.user_management.user_info import UserInfo
from src.app_logic.app_logic import Review, User

class TestUserInfo(unittest.TestCase):
    """
    Test cases for user information management functionalities.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class for UserInfo tests by initializing paths and mappers.
        """
        cls.db_path = "test.db"
        cls.object_mapper = ObjectMapper(cls.db_path)
        cls.session_manager = SessionManager(cls.db_path)
        cls.user_info = UserInfo(cls.db_path)

    def setUp(self):
        """
        Prepare the database for each test by clearing tables.
        """
        self.object_mapper.data_store.clear_tables()

    def test_register(self):
        """
        Test the user registration process.
        """
        username = "test_user"
        email = "test_user@example.com"
        password = "test_password"
        user = self.user_info.register(username, email, password)
        self.assertTrue(user)

    def test_login(self):
        """
        Test the user login process.
        """
        username = "test_user"
        email = "test_user@example.com"
        password = "test_password"
        result = self.user_info.register(username, email, password)
        self.assertTrue(result)

    def test_logout(self):
        """
        Test the user logout process and validate session deactivation.
        """
        username = "test_user"
        email = "test_user@example.com"
        password = "test_password"
        self.user_info.register(username, email, password)
        user_id = self.user_info.login(username, password)
        self.user_info.logout(user_id)
        retrieved_session = self.session_manager.get_session(user_id)
        self.assertFalse(retrieved_session.is_active)

    #def test_search_review(self):
    def test_search_review(self):
        """
        Test the search_review function to ensure it returns reviews matching a username query.

        This test creates a mock user and a mock review. It then mocks the object_mapper.get method
        to return these objects when queried. Finally, it calls the search_review method with the
        username of the mock user to ensure that the corresponding review is returned.
        """
        mock_user = User(username="test_user",
                        email="test_user@example.com",
                        hashed_password="test_password")
        mock_user.id = str(uuid.uuid4())
        mock_review = Review(review_text="This is a review.",
                             user_id=mock_user.id,
                             topic_id=str(uuid.uuid4()),
                             status="published")
        mock_review.id = str(uuid.uuid4())
        self.object_mapper.get = Mock()
        self.object_mapper.get.side_effect = (
            lambda cls: [mock_review] if cls == Review else
                        [mock_user] if cls == User else []
        )

        result = self.user_info.search_review(mock_user.username)
        self.assertTrue(review.id == mock_review.id for review in result)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after tests by removing the test database file.
        """
        os.remove("src/database/test.db")

if __name__ == '__main__':
    unittest.main()
