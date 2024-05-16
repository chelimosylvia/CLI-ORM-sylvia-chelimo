#models.py
import sqlite3
from database import Database

class Task:
    def __init__(self, title, description, due_date, category_id):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category_id = category_id

class Category:
    def __init__(self, name):
        self.name = name

class Session:
    def __init__(self):
        self.db = Database().get_connection()
        self.create_tables()

    def create_tables(self):
        with self.db:
            self.db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL,
                                description TEXT,
                                due_date TEXT,
                                category_id INTEGER)''')

            self.db.execute('''CREATE TABLE IF NOT EXISTS categories (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL)''')

    def add_task(self, task):
        with self.db:
            self.db.execute('INSERT INTO tasks (title, description, due_date, category_id) VALUES (?, ?, ?, ?)',
                            (task.title, task.description, task.due_date, task.category_id))

    def delete_task(self, task_id):
        with self.db:
            self.db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    def get_all_tasks(self):
        cursor = self.db.execute('SELECT * FROM tasks')
        return cursor.fetchall()

    def add_category(self, category):
        with self.db:
            self.db.execute('INSERT INTO categories (name) VALUES (?)', (category.name,))

    def delete_category(self, category_id):
        with self.db:
            self.db.execute('DELETE FROM categories WHERE id = ?', (category_id,))

    def get_all_categories(self):
        cursor = self.db.execute('SELECT * FROM categories')
        return cursor.fetchall()
