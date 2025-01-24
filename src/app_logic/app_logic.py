import datetime
import uuid
import json

class Base:
    def __init__(self, id: str=None):
        self.id = id or uuid.uuid4().hex

class User(Base):
    """
    A user in the system
    """

    def __init__(self, username: str, email:str, hashed_password: str, 
                 id: str=None):
        super().__init__(id)
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
    
    @property
    def data(self):
        """
        Allows you to access class data as a dictionary
        
        This function creates an empty dictionary and if it is the first time
        this class is initialized assigns the id a key in the dictionary. 
        Then updates all other entries to their current states.
        In all updates after the first the id will remain the same.

        Returns: 
            the class variables as a dictionary
        """
        data = {}
        if self.id:
            data["id"] = self.id

        data.update({
            "username" : self.username,
            "email" : self.email,
            "hashed_password" : self.hashed_password 
            })

        return data

    
class Review(Base):
    """
    A review in the system
    """

    def __init__(self, review_text: str, user_id: str, topic_id: str, 
                 status: str = "draft", review_ratings: str = None, 
                 id: str = None):
        super().__init__(id)
        self.review_text = review_text
        self.user_id = user_id
        self.topic_id = topic_id
        self.status = status
        self.review_ratings = review_ratings or '[]'
    
    @property
    def ratings(self):
        return json.loads(self.review_ratings)

    @property
    def data(self):
        """
        Allows you to access class data as a dictionary
        
        This function creates an empty dictionary and if it is the first time
        this class is initialized assigns the id a key in the dictionary. 
        Then updates all other entries to their current states.
        In all updates after the first the id will remain the same.

        Returns: 
            the class variables as a dictionary
        """
        data = {}
        if self.id:
            data["id"] = self.id

        data.update({
            "review_text" : self.review_text,
            "user_id" : self.user_id,
            "topic_id" : self.topic_id,
            "status" : self.status,
            "review_ratings" : self.review_ratings
        })

        return data


class Topic(Base):
    """
    a topic in the system 
    """
    
    def __init__(self, name: str, description: str, user_id: str, 
                 id: str = None):
        super().__init__(id)
        self.name = name
        self.description = description
        self.user_id = user_id

    @property
    def data(self):
        """
        Allows you to access class data as a dictionary
        
        This function creates an empty dictionary and if it is the first time
        this class is initialized assigns the id a key in the dictionary. 
        Then updates all other entries to their current states.
        In all updates after the first the id will remain the same.

        Returns: 
            the class variables as a dictionary
        """
        data = {}
        if self.id:
            data["id"] = self.id

        data.update({
            "name" : self.name,
            "description" : self.description,
            "user_id" : self.user_id
            })

        return data


class Session(Base):
    """
    A session with the server 
    """

    def __init__(self, user_id, created_at = None, expires_at = None, 
                 last_activity_at  = None, is_active = 0, id = None):
        super().__init__(id)
        self.user_id = user_id
        self.created_at = created_at or datetime.datetime.now()
        self.expires_at = expires_at or (self.created_at 
                                         + datetime.timedelta(hours=1))
        self.last_activity_at = last_activity_at or datetime.datetime.now()
        self.is_active = is_active

    @property
    def data(self):
        """
        Allows you to access class data as a dictionary
        
        This function creates an empty dictionary and if it is the first time
        this class is initialized assigns the id a key in the dictionary. 
        Then updates all other entries to their current states. 
        In all updates after the first the id will remain the same.

        Returns: 
            the class variables as a dictionary
        """
        data = {}
        if self.id:
            data["id"] = self.id

        data.update({"user_id" : self.user_id,
            "created_at" : self.created_at,
            "expires_at" : self.expires_at,
            "last_activity_at" : self.last_activity_at,
            "is_active" : self.is_active,
        })

        return data