"""This module contains unit tests for the object_mapper.py module."""
import os
from unittest import TestCase
from src.data_management.object_mapper import ObjectMapper
from src.app_logic.app_logic import User

class TestUserMapper(TestCase):
    """Unit tests for the UserMapper class."""
    @classmethod
    def setUpClass(cls):
        # Create a new test database for this test suite
        cls.object_mapper = ObjectMapper("test.db")

    def setUp(self):
        # Before each test, clear all tables to ensure there's no leftover data
        self.object_mapper.data_store.clear_tables()

    def test_add_success(self):
        """tests that data can be added to the database"""
        user = User("test", "testemail", "testpassword")
        self.assertTrue(self.object_mapper.add(user))

    def test_add_failure(self):
        """tests that data cannot be added to the database if the user is invalid"""
        user = "testuser"
        self.assertRaises(ValueError, self.object_mapper.add, user)

    def test_get_success(self):
        """tests that data can be retrieved from the database"""
        user = User("test", "testemail", "testpassword")
        user_id = user.id
        self.object_mapper.add(user)
        self.assertEqual(self.object_mapper.get(User, id=user_id).data, user.data)

    def test_get_failure(self):
        """tests that data cannot be retrieved from the database if the user's not in database"""
        user = User("testuser", "testpassword", "testemail")
        self.object_mapper.add(user)
        self.assertEqual(self.object_mapper.get(User, id=2), [])

    def test_remove_success(self):
        """tests that data can be removed from the database"""
        user = User("testuser", "testpassword", "testemail")
        self.object_mapper.add(user)
        self.assertTrue(self.object_mapper.remove(user))

    def test_remove_failure(self):
        """tests that data cannot be removed from the database if the user is not in the database"""
        user = User("testuser", "testpassword", "testemail")
        self.object_mapper.add(user)
        self.object_mapper.remove(user)
        self.assertRaises(ValueError, self.object_mapper.remove, user)

    @classmethod
    def tearDownClass(cls):
        # After all tests, delete the test database
        os.remove("src/database/test.db")
