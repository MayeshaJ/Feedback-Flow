"""This module contains unit tests for the data_store.py module."""
import os
from unittest import TestCase
from src.data_management.data_store import DataStore

class TestDataStore(TestCase):
    """Unit tests for the DataStore class."""
    @classmethod
    def setUpClass(cls):
        # Create a new test database for this test suite
        cls.data_store = DataStore("test.db")

    def setUp(self):
        # Before each test, clear all tables to ensure there's no leftover data
        self.data_store.clear_tables()

    def test_save_success(self):
        """tests that data can be saved to the database"""
        user_data = {
            "id": "1",
            "username": "test_user_1",
            "hashed_password": "test_password_1",
            "email": "test_email_1@example.com",
        }
        self.assertTrue(self.data_store.save(user_data, "user"))

    def test_save_failure(self):
        """tests a save failure when missing a required column"""
        user_data = {
            "id": "1",
            "username": "test_user_1",
            "hashed_password": "test_password_1",
            "email": "test_email_1@example.com",
        }
        self.assertTrue(self.data_store.save(user_data, "user"))
        # as long as required columns are present, save should succeed, disregarding extra columns
        user_data["invalid_column"] = "invalid_value"
        self.assertTrue(self.data_store.save(user_data, "user"))
        bad_user_data = {
            "id": "1",
            "username": "test_user_1",
            "hashed_password": "test_password_1",
        }
        self.assertFalse(self.data_store.save(bad_user_data, "user"))

    def test_load_success(self):
        """tests that data can be loaded from the database"""
        user_data = {
            "id": "1",
            "username": "test_user_1",
            "hashed_password": "test_password_1",
            "email": "test_email_1@example.com",
        }
        self.assertTrue(self.data_store.save(user_data, "user"))
        loaded_users = self.data_store.load("user")
        self.assertIn(user_data, loaded_users)

    def test_load_failure(self):
        """tests that data cannot be loaded from an invalid table"""
        user_data = {
            "id": "1",
            "username": "test_user_1",
            "hashed_password": "test_password_1",
            "email": "test_email_1@example.com",
        }
        self.assertTrue(self.data_store.save(user_data, "user"))
        loaded_users = self.data_store.load("invalid_table")
        self.assertEqual(loaded_users, None)

    def test_clear_tables(self):
        """tests that tables can be cleared"""
        user_data = {
            "id": "1",
            "username": "test_user_1",
            "hashed_password": "test_password_1",
            "email": "test_email_1@example.com",
        }
        self.assertTrue(self.data_store.save(user_data, "user"))
        self.data_store.clear_tables()
        loaded_users = self.data_store.load("user")
        self.assertEqual(loaded_users, [])

    def test_delete_success(self):
        """tests that data can be deleted from the database"""
        user_data = {
            "id": "1",
            "username": "test_user_1",
            "hashed_password": "test_password_1",
            "email": "test_email_1@example.com",
        }
        self.assertTrue(self.data_store.save(user_data, "user"))
        self.assertTrue(self.data_store.delete(1, "user"))

    def test_delete_failure(self):
        """tests that data cannot be deleted from an invalid table"""
        self.assertFalse(self.data_store.delete(1, "user"))

    @classmethod
    def tearDownClass(cls):
        os.remove("src/database/test.db")
