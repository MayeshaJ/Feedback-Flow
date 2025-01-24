
"""
server_app.py - Web Application

This file contains the logic and routing for a web application built using Bottle. 
The application handles user registration, login, dashboard, topic management,
and review creation/editing. It interfaces with a user information system, a logic system and
uses templates to render HTML views for various user interactions.

Author:
- Cody Cribb

Date:
- Oct. 17, 2023

Version:
- 1.0
"""

import random
import json
import os
from bottle import Bottle, run, template, request, redirect, response, static_file, TEMPLATE_PATH
from src.user_management.user_info import UserInfo
from src.app_logic.app_logic import Topic, Review

TEMPLATE_PATH.insert(0, './src/templates/')

class WebServer(Bottle):
    """
    WebServer class to handle web application routing and functionality, uses Bottle.
    """
    def __init__(self):
        """
        Initialize the WebServer instance.
        """
        super().__init__()
        self.TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '../../templates')
        self.database_path = 'database_path'
        self.secret = 'secret'

        # Route definitions
        self.route('/', callback=self.home)
        self.route('/home', callback=self.home)
        self.route('/login', callback=self.login)
        self.route('/login', method='POST', callback=self.do_login)
        self.route('/register', callback=self.register)
        self.route('/register', method='POST', callback=self.do_register)
        self.route('/dashboard', callback=self.dashboard)
        self.route('/dashboard', method='POST', callback=self.create_review)
        self.route('/topics', callback=self.list_topics)
        self.route('/topics/add', callback=self.show_create_topic_form)
        self.route('/topics/create', method='POST', callback=self.create_topic)
        self.route('/topics/<topic_id>/create_review', method=['GET', 'POST'], callback=self.create_review)
        self.route('/reviews', method=['GET', 'POST'], callback=self.list_reviews)
        self.route('/reviews/<review_id>/edit', method=['GET', 'POST'], callback=self.edit_review)
        self.route('/reviews/<review_id>/delete', method=['GET', 'POST'], callback=self.delete_review)
        self.route('/reviews/search', method=['GET', 'POST'], callback=self.search_review)
        self.route('/logout', method=['GET', 'POST'], callback=self.logout)
        self.route('/static/<filepath:path>', callback=self.server_static)

    def server_static(self, filepath):
        """Serve static files."""
        return static_file(filepath, root='./static/')

    def home(self):
        """
        Callback for the home route.

        Returns:
            str: Response for the home route. (base template)
        """
        return template('base.tpl', title='Home Page', base='<h1>Welcome to the home page!</h1>')

    def dashboard(self):
        """
        Callback for the dashboard route.

        Returns:
            str: Response for the dashboard route. (logged_in template)
        """
        self.login_check()
        return template('base_logged_in.tpl', title="Dashboard", base="Welcome to the dashboard!")

    def login(self):
        """
        Callback for the login route.

        Returns:
            str: Response for the login route. (login template)
        """
        return template('login')

    def do_login(self):
        """
        Implements the login itself, requests username and password from user, checks validity.

        Returns:
            str: Redirection to the dashboard if log in is successful, else returns an error message.
        """
        username = request.forms.get('username')
        password = request.forms.get('password')
        session_id = UserInfo(self.database_path).login(username, password)

        # set cookie
        response.set_cookie("session_id", session_id, secret=self.secret)

        if session_id:
            self.logged_in_user = username
            return redirect('/dashboard')
        else:
            return redirect('/')
        
    def login_check(self):
        """
        Implements a check to make sure the user is logged in, prevents access to other pages of the server unless logged in.

        Returns:
            str: Does nothing if user is logged in, redirects to login page if user is not logged in.
        """
        session_id = request.get_cookie("session_id", secret=self.secret)
    
        if not session_id:
            return redirect('/login')

    def register(self):
        """
        Callback for the registration route.

        Returns:
            str: Response for the login route (registration template).
        """
        return template('register')

    def do_register(self):
        """
        Handle the user registration process.

        Registers a new user using the provided username, email, and password.

        Returns:
            str: Redirect to login route.
        """
        username = request.forms.get('username')
        password = request.forms.get('password')
        email = request.forms.get('email')
        UserInfo(self.database_path).register(username, email, password)
        return redirect('/login')

    def create_review(self, topic_id):
        """
        Create a new review for a given topic.

        Args:
            topic_id (int): The ID of the topic for which the review is being created.

        Returns:
            str: Response indicating the success or failure of the review creation.
        """
        self.login_check()
        if request.method == 'POST':
            review_content = request.forms.get('review_text')
            review_ratings = [
                int(request.forms.get('effort')), 
                int(request.forms.get('communication')),
                int(request.forms.get('participation')),
                int(request.forms.get('attendance'))
                ]
            review_ratings = json.dumps(review_ratings) # converts "[0, 0, 0, 0]" to [0, 0, 0, 0]

             # Check which button was clicked
            if request.forms.get('save'):
                action = 'Save Draft'
            elif request.forms.get('publish'):
                action = 'Publish Review'
            else:
                action = None  # No known action
            
            session_id = request.get_cookie("session_id", secret=self.secret)
            user_id = UserInfo(self.database_path).session_manager.get_session(session_id).user_id

            status = "draft" if action == "Save Draft" else "published"

            review = Review(review_content, user_id, topic_id, status, review_ratings=review_ratings)

            UserInfo(self.database_path).object_mapper.add(review)
            return redirect('/topics')
        return template('create_review.tpl', title="Create Review", topic_id=topic_id, base="base_logged_in.tpl")
    
    def edit_review(self, review_id):
        """
        Edit an existing review.

        Args:
            review_id (int): The ID of the review to be edited.

        Returns:
            str: Response indicating the success or failure of the review editing.
        """
        self.login_check()
        user_info = UserInfo(self.database_path)
        review = user_info.object_mapper.get(Review, id=review_id)

        # Ensure the review exists and belongs to the logged-in user
        if not review:
            return "Review not found"

        if request.method == 'POST':
            updated_review_text = request.forms.get('review_text')
            review_ratings = [
                int(request.forms.get('effort')), 
                int(request.forms.get('communication')),
                int(request.forms.get('participation')),
                int(request.forms.get('attendance'))
                ]
            review_ratings = json.dumps(review_ratings) # converts "[0, 0, 0, 0]" to [0, 0, 0, 0]
            review.review_text = updated_review_text
            
            # Check which button was clicked
            if request.forms.get('save'):
                review.status = "draft"
            elif request.forms.get('publish'):
                review.status = "published"

            user_info.object_mapper.add(review)
            
            return redirect('/reviews')
        return template('edit_review.tpl', review=review)
    
    def delete_review(self, review_id):
        """
        Delete an existing review.

        Args:
            review_id (int): The ID of the review to be edited.

        Returns:
            str: Response indicating the success or failure of the review deletion.
        """
        self.login_check()
        user_info = UserInfo(self.database_path)

        if request.method == 'POST':
            review = user_info.object_mapper.get(Review, id=review_id)
            session_id = request.get_cookie("session_id", secret=self.secret)
            user_id = user_info.session_manager.get_session(session_id).user_id
            if review.user_id == user_id:
                user_info.object_mapper.remove(review)
            return redirect('/reviews')
        reviews = user_info.object_mapper.get(Review)
        return template('list_reviews.tpl', reviews=reviews, filter_criteria="all", request=request, base="base_logged_in.tpl")
    
    def search_review(self):
        """
        Searches for a review based on the provided query.

        Returns:
            str: HTML response displaying a list of topics based that conform with the user's search query.
        
        """
        if request.method == 'POST':
            query = request.forms.get('query')
            filter_criteria = request.forms.get('filter') or 'all'
            reviews = UserInfo(self.database_path).search_review(query)
            reviews = [review for review in reviews if review.status != "draft"]
            return template('list_reviews.tpl', title="Reviews", reviews=reviews, filter_criteria=filter_criteria, base="base_logged_in.tpl")
        
    def list_topics(self):
        """
        List all topics available.

        Returns:
            str: HTML response displaying a list of topics.
        """
        self.login_check()
        topics = UserInfo(self.database_path).object_mapper.get(Topic)
        raw_reviews = UserInfo(self.database_path).object_mapper.get(Review)
      
        reviews = {}
        for topic in topics:
            reviews[topic.id] = [review for review in raw_reviews if review.topic_id == topic.id and review.status == "published"]
        return template('list_topics.tpl', title="Topics", topics=topics, reviews=reviews, base="base_logged_in.tpl")

    def list_reviews(self):
        """
        List all reviews available.

        Returns:
            str: HTML response displaying a list of reviews.
        """
        self.login_check()
        filter_criteria = request.forms.get('filter') or 'all'

        #get session id from cookie
        session_id = request.get_cookie("session_id", secret=self.secret)
        user_id = UserInfo(self.database_path).session_manager.get_session(session_id).user_id
        reviews = UserInfo(self.database_path).object_mapper.get(Review)

        if filter_criteria == 'all':
            reviews = [review for review in reviews if review.user_id == user_id]
        elif filter_criteria == 'published':
            reviews = [review for review in reviews if review.user_id == user_id and review.status == "published"]
        elif filter_criteria == 'draft':
            reviews = [review for review in reviews if review.user_id == user_id and review.status == "draft"]
        else:
            reviews = []

        return template('list_reviews.tpl', title="Reviews", reviews=reviews, filter_criteria=filter_criteria, base="base_logged_in.tpl")

    def show_create_topic_form(self):
        """
        Display the form for creating a new topic.

        Returns:
            str: HTML response displaying the topic creation form.
        """
        self.login_check()
        return template('create_topic.tpl', title="Create Topic", base='base_logged_in.tpl')

    def create_topic(self):
        """
        Create a new topic based on the provided form data.

        Returns:
            str: HTML response indicating the success or failure of the topic creation.
        """
        self.login_check()
        if request.method == 'POST':
        
            topic_name = request.forms.get('name')
            topic_description = request.forms.get('description')
            session_id = request.get_cookie("session_id", secret=self.secret)
            user_id = UserInfo(self.database_path).session_manager.get_session(session_id).user_id
            topic = Topic(topic_name, topic_description, user_id)
            UserInfo(self.database_path).object_mapper.add(topic)
            return redirect("/topics")
    
    def logout(self):
        if request.method == 'POST':
            #get session id from cookie
            session_id = request.get_cookie("session_id", secret=self.secret)
            UserInfo(self.database_path).logout(session_id)
            response.delete_cookie("session_id")
            return redirect('/login')
        return template('logout.tpl', title="Logout", base="base_logged_in.tpl")

if __name__ == "__main__":
    host_name = "localhost"
    server_port = 8080
    app = WebServer()

    TEMPLATE_PATH.insert(0, './src/templates/')

    app.run(host=host_name, port=server_port)
    print("Server stopped.")