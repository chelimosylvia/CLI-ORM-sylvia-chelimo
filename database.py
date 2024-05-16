# database.py
import sqlite3

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect('task_manager.db')
        return cls._instance

    def get_connection(self):
        return self.conn

    def close_connection(self):
        self.conn.close()
