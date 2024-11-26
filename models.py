from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TaskGroup(db.Model):
    __tablename__ = 'taskGroup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the group
    description = db.Column(db.String(255))           # Optional description
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Owner of the group

    # Relationship to User (Cascade delete tasks when user is deleted)
    user = db.relationship('User', backref=db.backref('taskGroup', cascade='all, delete'), lazy=True)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mem_ques1 = db.Column(db.String(200), nullable=False)
    mem_ques2 = db.Column(db.String(200), nullable=False)
    mem_ans1 = db.Column(db.String, nullable=False)
    mem_ans2 = db.Column(db.String, nullable=False)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship to User (Cascade delete tasks when user is deleted)
    user = db.relationship('User', backref=db.backref('tasks', cascade='all, delete'), lazy=True)

class CompletedTask(db.Model):
    __tablename__ = 'completedTasks'

    completed_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign key to users
    title = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('taskGroup.id'), nullable=True)  # Foreign key to TaskGroup
    completed_date = db.Column(db.Date, nullable=False)

    # Relationship to User (Cascade delete completed tasks when user is deleted)
    user = db.relationship('User', backref=db.backref('completed_tasks', cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f"<CompletedTask {self.completed_id} - {self.title}>"