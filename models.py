from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class TaskGroup(db.Model):
    __tablename__ = 'taskGroup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the group
    description = db.Column(db.String(255))           # Optional description
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Owner of the group

    # Relationship to tasks
    tasks = db.relationship('Task', backref='group', lazy=True)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Define the relationship with Task
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    # Flask-Login required methods
    def get_id(self):
        return str(self.id)  # This returns the user id as a string

    @property
    def is_active(self):
        # Return True to indicate the user is active
        return True

    @property
    def is_authenticated(self):
        # Return True if the user is authenticated, it will return True when login_user() is called
        return True

    @property
    def is_anonymous(self):
        # Return False, since we don't want to support anonymous users in this case
        return False

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')
    group_id = db.Column(db.Integer, db.ForeignKey('taskGroup.id'), nullable=True)  # Foreign key to group

    # Define the foreign key linking to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

