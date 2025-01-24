"""
This module contains unittests for the session management functions.
It includes tests for session creation, validation, termination, and other related utilities.
"""
import os
import unittest
from unittest.mock import patch, Mock

# Local imports
from src.data_management.object_mapper import ObjectMapper
from src.user_management.session_management import SessionManager
from src.app_logic.app_logic import Session

class TestSessionManager(unittest.TestCase):
    """
    Test cases for session management functionalities.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class for SessionManager tests by initializing paths and mappers.
        """
        cls.db_path = "test.db"
        cls.object_mapper = ObjectMapper(cls.db_path)
        cls.session_manager = SessionManager(cls.db_path)

    def setUp(self):
        """
        Prepare the database for each test by clearing tables.
        """
        self.object_mapper.data_store.clear_tables()

    def test_create_session(self):
        """
        Test the creation of a session to ensure it returns a Session instance.
        """
        user_id = 1
        with patch.object(self.session_manager.object_mapper, 'add', return_value=True):
            session = self.session_manager.create_session(user_id)
            self.assertIsInstance(session, Session)

    def test_get_session(self):
        """
        Test retrieval of a session to ensure the correct session is obtained.
        """
        user_id = 1
        with patch.object(self.session_manager.object_mapper, 'add', return_value=True):
            created_session = self.session_manager.create_session(user_id)
        retrieved_session = self.session_manager.get_session(created_session.user_id)
        self.assertIsNotNone(retrieved_session)

    def mock_db_get_method(self, _obj_class, _obj_id=None):
        """
        Mock method for database 'get' operation to simulate retrieving a session.
        
        param obj_class: The class type for the objects to retrieve.
        param id: Optional ID for the object to retrieve.
        return: A list containing a mock Session object.
        """
        return [Session(user_id=1, is_active=1)]

    def test_get_user_session(self):
        """
        Test the retrieval of a user's session to ensure the correct session is returned.
        """
        user_id = 1

        with patch('src.user_management.session_management.ObjectMapper.get',
                   side_effect=self.mock_db_get_method):
            with patch('src.user_management.session_management.SessionManager.update_session',
                       return_value=True):
                retrieved_session = self.session_manager.get_user_session(user_id)

        self.assertIsNotNone(retrieved_session)
        self.assertEqual(retrieved_session.user_id, user_id)

    def test_update_session(self):
        """
        Test updating a session's active status to ensure it is properly updated.
        """
        user_id = 1
        mock_session = Mock()
        mock_session.user_id = user_id
        mock_session.is_active = 1

        with patch('src.user_management.session_management.SessionManager.create_session',
                   return_value=mock_session):
            with patch.object(self.session_manager.object_mapper, 'add', return_value=True):
                session = self.session_manager.create_session(user_id)
                self.assertEqual(session.user_id, user_id)
                self.assertEqual(session.is_active, 1)
                session.is_active = 0
                with patch('src.user_management.session_management.SessionManager.get_user_session',
                           return_value=mock_session):
                    self.session_manager.update_session(session)
                    retrieved_session = self.session_manager.get_user_session(user_id)
                    self.assertEqual(retrieved_session.is_active, 0)


    @classmethod
    def tearDownClass(cls):
        """
        Clean up after tests by removing the test database file.
        """
        os.remove("src/database/test.db")

if __name__ == '__main__':
    unittest.main()
