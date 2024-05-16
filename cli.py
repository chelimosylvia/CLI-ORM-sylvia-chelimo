from models import Task, Category, Session
from datetime import datetime

class TaskManagerCLI:
    def __init__(self):
        self.running = True
        self.session = Session()

    def initialize(self):
        print("Welcome to Task Manager!")

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
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
            return

        category_id = input("Enter category ID: ")

        task = Task(title, 
                    description, 
                    due_date, 
                    category_id)
        self.session.add_task(task)
        print("Task created successfully.")

    def delete_task(self):
        task_id = input("Enter task ID to delete: ")
        self.session.delete_task(task_id)
        print("Task deleted successfully.")

    def view_all_tasks(self):
        tasks = self.session.get_all_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(task)

    def view_tasks_by_category(self):
        category_id = input("Enter category ID: ")
        tasks = self.session.get_all_tasks()
        filtered_tasks = [task for task in tasks if task[4] == int(category_id)]
        if not filtered_tasks:
            print("No tasks found for the specified category.")
        else:
            for task in filtered_tasks:
                print(task)

    def find_task_by_id(self):
        task_id = input("Enter task ID: ")
        tasks = self.session.get_all_tasks()
        for task in tasks:
            if task[0] == int(task_id):
                print(task)
                return
        print("Task not found.")

    def create_category(self):
        name = input("Enter category name: ")
        category = Category(name)
        self.session.add_category(category)
        print("Category created successfully.")

    def delete_category(self):
        category_id = input("Enter category ID to delete: ")
        self.session.delete_category(category_id)
        print("Category deleted successfully.")

    def view_all_categories(self):
        categories = self.session.get_all_categories()
        if not categories:
            print("No categories found.")
        else:
            for category in categories:
                print(category)

    def view_tasks_of_category(self):
        category_id = input("Enter category ID: ")
        tasks = self.session.get_all_tasks()
        filtered_tasks = [task for task in tasks if task[4] == int(category_id)]
        if not filtered_tasks:
            print("No tasks found for the specified category.")
        else:
            for task in filtered_tasks:
                print(task)

    def find_category_by_id(self):
        category_id = input("Enter category ID: ")
        categories = self.session.get_all_categories()
        for category in categories:
            if category[0] == int(category_id):
                print(category)
                return
        print("Category not found.")

    def exit(self):
        print("Exiting Task Manager. Goodbye!")
        self.running = False
        self.session.db.close()

    def run(self):
        self.initialize()
        while self.running:
            self.display_menu()
            self.handle_input()
