import os
import sqlite3
from src.data_management import db_schema

class SQLiteConnection:
    """Context manager for SQLite database connection."""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database and enables foreign key support. Returns the connection object."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys=ON;")
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the connection to the SQLite database."""
        self.connection.commit()
        self.connection.close()

class DataStore:
    TABLES = {
        "user": db_schema.USER_TABLE,
        "topic": db_schema.TOPIC_TABLE,
        "review": db_schema.REVIEW_TABLE,
        "session": db_schema.SESSION_TABLE
    }

    def __init__(self, db_path: str):
        """
        Initializes a DataStore instance with the path to the SQLite database file.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = "src/database/" + db_path
        self._create_tables()

    def _create_tables(self):
        """
        Creates the necessary tables in the database by executing the table schemas.
        """
        # check if database folder exists, if not make one
        if not os.path.exists("src/database"):
            os.makedirs("src/database")

        with SQLiteConnection(self.db_path) as connection:
            cursor = connection.cursor()
            for table in self.TABLES.values():
                cursor.execute(table)

    def save(self, data, table_name):
        """
        Saves the provided data to the specified table.

        Args:
            data (dict): The data to be saved.
            table_name (str): The name of the table to save the data to.

        Returns:
            int or bool: The last inserted row id if successful, False if an integrity error occurs.
        """
        query, columns = self._construct_insert_query(table_name)
        with SQLiteConnection(self.db_path) as connection:
            try:
                data_values = tuple(data[column] for column in columns)
                cursor = connection.cursor()
                cursor.execute(query, data_values)
                return True
            except Exception:
                return False

    def _construct_insert_query(self, table_name: str):
        """
        Generates an INSERT query for the given table name.

        Args:
            table_name (str): The name of the table.

        Returns:
            Tuple[str, List[str]]: The generated INSERT query and list of columns.
        """
        columns = self._get_columns_from_table_schema(self.TABLES[table_name])
        placeholders = ", ".join(["?" for _ in columns])
        return f"REPLACE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", columns  # Returning columns too

    @staticmethod
    def _get_columns_from_table_schema(table_schema: str) -> list:
        """
        Extracts column names from the table schema.

        Args:
            table_schema (str): The schema of the table.

        Returns:
            list: The list of column names.
        """
        # Split the schema by comma and then filter out unwanted entries.
        columns = [column.strip().split()[0] for column in table_schema.split("(")[1].split(",")]
        return [column for column in columns if not column.upper().startswith(('FOREIGN', 'PRIMARY', 'CHECK', 'UNIQUE'))]

    def load(self, table_name, id=None):
        """
        Loads data from the specified table, optionally filtering by ID.

        Args:
            table_name (str): The name of the table.
            id (int, optional): The ID to filter by. Defaults to None.

        Returns:
            list or None: The loaded data as a list of dictionaries, or None if no data is found.
        """
        with SQLiteConnection(self.db_path) as connection:
            try:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                query = f"SELECT * FROM {table_name}"
                if id:
                    query += self._construct_where_clause(table_name, id)
                cursor.execute(query)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            except sqlite3.Error as e:
                print(f"Error loading data from table {table_name}: {str(e)}")
                return None

    def _construct_where_clause(self, table_name: str, id: int) -> str:
        """
        Generates a WHERE clause for the query based on the table name and ID.

        Args:
            table_name (str): The name of the table.
            id (int): The ID to filter by.

        Returns:
            str: The generated WHERE clause.
        """
        return f" WHERE id = '{id}'"

    def delete(self, id, table_name):
        """
        Deletes data from the specified table based on the ID.

        Args:
            id (int): The ID of the data to delete.
            table_name (str): The name of the table.

        Returns:
            bool: True if the deletion is successful, False otherwise.
        """
        with SQLiteConnection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                print(f"Error deleting entry from table {table_name}: {str(e)}")
                return False
            
    def clear_tables(self):
        """
        Clears all tables in the database.
        """
        with SQLiteConnection(self.db_path) as connection:
            cursor = connection.cursor()
            for table in self.TABLES.keys():
                cursor.execute(f"DELETE FROM {table}")
