# lib/task_manager_cli.py
import sys
from task_manager_models import Task, Category, Session
from datetime import datetime
from sqlalchemy.orm import joinedload

class TaskManagerCLI:
    def __init__(self):
        self.running = True
        self.initialize()

    def initialize(self):
        print("Welcome to Task Manager CLI!")

    def display_menu(self):
        print("\nMenu:")
        print("1. Tasks")
        print("2. Categories")
        print("3. Exit")

    def handle_input(self):
        choice = input("Enter your choice: ")
        if choice == "1":
            self.handle_tasks_menu()
        elif choice == "2":
            self.handle_categories_menu()
        elif choice == "3":
            self.exit()
        else:
            print("Invalid choice. Please try again.")

    def handle_tasks_menu(self):
        print("\nTasks Menu:")
        print("1. Create Task")
        print("2. Delete Task")
        print("3. View All Tasks")
        print("4. View Tasks by Category")
        print("5. Find Task by ID")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            self.create_task()
        elif choice == "2":
            self.delete_task()
        elif choice == "3":
            self.view_all_tasks()
        elif choice == "4":
            self.view_tasks_by_category()
        elif choice == "5":
            self.find_task_by_id()
        elif choice == "6":
            return

    def handle_categories_menu(self):
        print("\nCategories Menu:")
        print("1. Create Category")
        print("2. Delete Category")
        print("3. View All Categories")
        print("4. View Tasks of a Category")
        print("5. Find Category by ID")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            self.create_category()
        elif choice == "2":
            self.delete_category()
        elif choice == "3":
            self.view_all_categories()
        elif choice == "4":
            self.view_tasks_of_category()
        elif choice == "5":
            self.find_category_by_id()
        elif choice == "6":
            return

    def create_task(self):
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date_str = input("Enter due date (YYYY-MM-DD): ")
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            print("Parsed due date:", due_date)  
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
            return

        category_id = input("Enter category ID: ")

        task = Task.create_task(title=title, description=description, due_date=due_date, category_id=category_id)
        print("Task created successfully.")

    def delete_task(self):
     task_id = input("Enter task ID to delete: ")
     session = Session()
     task = session.query(Task).filter_by(id=task_id).first()
     session.close()
    
     if task:
        Task.delete_task(task_id)
        print("Task deleted successfully.")
     else:
        print("Task with the given ID does not exist.")
    def view_all_tasks(self):
     session = Session()
     tasks = session.query(Task).all()
     session.close()
     if tasks:
        for task in tasks:
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Due Date: {task.due_date}")
            print(f"Category ID: {task.category_id}")
            print ()
            print ()
     else:
        print("No tasks found.")

    def view_tasks_by_category(self):
        category_id = input("Enter category ID: ")
        tasks = Task.get_tasks_by_category(category_id)
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("No tasks found for the specified category.")

    def find_task_by_id(self):
        task_id = input("Enter task ID: ")
        task = Task.find_task_by_id(task_id)
        if task:
            print(task)
        else:
            print("Task not found.")

    def create_category(self):
        name = input("Enter category name: ")
        Category.create_category(name=name)
        print("Category created successfully.")

    def delete_category(self):
        category_id = input("Enter category ID to delete: ")
        Category.delete_category(category_id)
        print("Category deleted successfully.")

    def view_all_categories(self):
     with Session() as session:
        categories = session.query(Category).all()
        if categories:
            for category in categories:
                print(f"Category ID: {category.id}")
                print(f"Name: {category.name}")
                print()
        else:
            print("No categories found.")
    def view_tasks_of_category(self):
     category_id = input("Enter category ID: ")
     category = Category.find_category_by_id(category_id)
     if category:
        session = Session()
        category_with_tasks = session.query(Category).options(joinedload(Category.tasks)).filter_by(id=category_id).first()
        session.close()
        if category_with_tasks:
            for task in category_with_tasks.tasks:
                print(f"Task ID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"Due Date: {task.due_date}")
                print(f"Category ID: {task.category_id}")
                print()
        else:
            print("No tasks found for the specified category.")
     else:
        print("Category not found.")

    def find_category_by_id(self):
     category_id = input("Enter category ID: ")
     category = Category.find_category_by_id(category_id)
     if category:
        print(f"Category ID: {category.id}")
        print(f"Category Name: {category.name}")
     else:
        print("Category not found.")

    def exit(self):
        print("Exiting Task Manager!")
        self.running = False
        sys.exit()

    def run(self):
        while self.running:
            self.display_menu()
            self.handle_input()

if __name__ == "__main__":
    cli = TaskManagerCLI()
    cli.run()
