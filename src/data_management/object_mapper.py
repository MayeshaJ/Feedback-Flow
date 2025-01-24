from src.data_management.data_store import DataStore

class ObjectMapper:
    """
    The `ObjectMapper` class is responsible for mapping objects to the database using the `DataStore` class.
    It provides methods to add, remove, and retrieve objects from the database.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes the ObjectMapper with the path to the database file.

        Args:
            db_path: The path to the database file.
        """
        self.data_store = DataStore(db_path)

    def _get_obj_type(self, obj) -> str:
        """
        Returns the type of the object as a string.

        Args:
            obj: The object.

        Returns: 
            The type of the object as a string.
        """  
        # if obj is a Class (ie: obj = User) or an instance of a class (ie: obj = User())
        if isinstance(obj, type):
            type_name = obj.__name__.lower()
        else:
            type_name = obj.__class__.__name__.lower()
        
        return type_name

    def add(self, obj) -> bool:
        """
        Adds an object to the database.

        Args:
            obj: The object to add.

        Returns:
            True if successful, False otherwise.
        """
        obj_type = self._get_obj_type(obj)
        if obj_type in self.data_store.TABLES.keys():
            result = self.data_store.save(obj.data, obj_type)
        else:
            raise ValueError(f"Invalid object type: {obj_type}")
        
        if result:
            return result
        else:
            raise ValueError(f"error adding {obj_type} with id {obj.id}")

    def remove(self, obj) -> bool:
        """
        Removes an object from the database.

        Args:
            obj: The object to remove.
        Returns:
            True if successful, False otherwise.
        """
        obj_type = self._get_obj_type(obj)
        result = self.data_store.delete(obj.id, obj_type)
        if result:
            return result
        else:
            raise ValueError(f"{obj_type} with id {obj.id} not found")
        

    def get(self, obj_class, id=None):
        """
        Retrieves an object from the database.
        Args:
            obj_class: The class of the object to retrieve.
            id: The ID of the object to retrieve.

        Returns:
            The object if found, None otherwise.
        """
        try:
            obj_type = self._get_obj_type(obj_class)
            data = self.data_store.load(obj_type, id=id)
            if data is None:
                raise ValueError(f"{obj_type} with id {id} not found")
            result = [obj_class(**obj_data) for obj_data in data]
            if result and id:
                return result[0]
            return result
        except Exception as e:
            print(f"Error retrieving {obj_type}: {str(e)}")
            raise e
