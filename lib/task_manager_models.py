# lib/task_manager_models.py
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///task_manager.db')
Session = sessionmaker(bind=engine)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    tasks = relationship('Task', back_populates='category')
    
    def __str__(self):
        return f"Category: {self.name}"

    @classmethod
    def create_category(cls, name):
        session = Session()
        category = Category(name=name)
        session.add(category)
        session.commit()
        session.close()

        return category
    @classmethod
    def get_all_categories(cls):
        session = Session()
        categories = session.query(Category).all()
        session.close()
        return categories
    @classmethod
    def delete_category(cls, category_id):
        session = Session()
        category = session.query(Category).filter_by(id=category_id).first()
        if category:
            session.delete(category)
            session.commit()
            session.close()
        else:
            print("Category not found.")
    @classmethod
    def find_category_by_id(cls, category_id):
        session = Session()
        category = session.query(Category).filter_by(id=category_id).first()
        session.close()
        return category      
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    due_date = Column(Date)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='tasks')

    def __str__(self):
        return f"Task ID: {self.id}, Title: {self.title}, Description: {self.description}, Due Date: {self.due_date}, Category ID: {self.category_id}"

    @classmethod
    def create_task(cls, title, description, due_date, category_id):
        session = Session()
        task = Task(title=title, description=description, due_date=due_date, category_id=category_id)
        session.add(task)
        session.commit()
        session.close()

    @classmethod
    def delete_task(cls, task_id):
        session = Session()
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            session.delete(task)
            session.commit()
        session.close()

    @classmethod
    def get_all_tasks(cls):
        session = Session()
        tasks = session.query(Task).all()
        session.close()
        return tasks
    @classmethod
    def get_tasks_by_category(cls, category_id):
        session = Session()
        tasks = session.query(Task).filter_by(category_id=category_id).all()
        session.close()
        return tasks

    @classmethod
    def find_task_by_id(cls, task_id):
        session = Session()
        task = session.query(Task).filter_by(id=task_id).first()
        session.close()
        return task

Base.metadata.create_all(engine)