import sqlite3
from sqlite3 import Error


CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  sex INTEGER,
  is_closed BOOLEAN,
  bdate TEXT,
  about TEXT,
  activities TEXT,
  university INTEGER,
  university_name TEXT,
  faculty INTEGER,
  faculty_name TEXT,
  graduation INTEGER,
  home_town TEXT
);
"""

CREATE_FRIENDS_TABLE = """
CREATE TABLE IF NOT EXISTS friends (
  user_id INTEGER,
  friend_id INTEGER
);
"""

tables = [CREATE_USERS_TABLE, CREATE_FRIENDS_TABLE]

class SQLiteDriver:
    def __init__(self, path):
        self.path = path
        self.connection = self._create_connection()
        for table in tables:
          self.execute_query(table)
        print("Tables has been created")

    def _create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection   
    
    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            #print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred while processing quary: {query}")