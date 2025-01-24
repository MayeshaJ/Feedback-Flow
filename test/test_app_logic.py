"""This module contains unit tests for the app_logic.py module."""
from unittest import TestCase
from src.app_logic.app_logic import User
from src.app_logic.app_logic import Topic
from src.app_logic.app_logic import Review
from src.app_logic.app_logic import Session

class TestAppLogic(TestCase):
    """Unittests for the Review, Topic, User and Session classes"""
    @classmethod
    def setUpClass(cls):
        # Create a new instance of each class for the tests
        cls.user = User('Martha','email@gmail.com','password','a')
        cls.topic = Topic('Stocks','They are going up','a','b')
        cls.review = Review('this is a test','a','b',"draft",'[1,2,3,4]','c',)
        cls.session = Session('a','b','c','d','e','f')

    def test_user_success(self):
        """tests the user class is initialized correctly"""
        user_data = {
            "id": 'a',
            "username": 'Martha',
            "hashed_password": 'password',
            "email": 'email@gmail.com',
        }
        self.assertEqual(self.user.data, user_data)

    def test_topic_success(self):
        """tests the topic class is initialized correctly"""
        topic_data = {
            "id" : 'b',
            "name" : 'Stocks',
            "description" : 'They are going up',
            "user_id" : 'a'
        }
        self.assertEqual(self.topic.data, topic_data)

    def test_review_success(self):
        """tests the Review class is initialized correctly"""
        review_data = {
            "id" : 'c',
            "review_text" : 'this is a test',
            "user_id" : 'a',
            "topic_id" : 'b',
            "status" : "draft",
            "review_ratings" : '[1,2,3,4]'
        }
        self.assertEqual(self.review.data, review_data)

    def test_session_success(self):
        """tests the Session class is initialized correctly"""
        review_data = {
            "id" : 'f',
            "user_id" : 'a',
            "created_at" : 'b',
            "expires_at" : 'c',
            "last_activity_at" : 'd',
            "is_active" : 'e',
        }
        self.assertEqual(self.session.data, review_data)
