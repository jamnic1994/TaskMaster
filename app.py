from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.priority).all()
    return render_template('index.html', tasks=tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        print(f"User found: {user}")  # Debugging: Print the user object

        if user:
            print(f"Entered password: {password}")
            print(f"Stored password hash: {user.password_hash}")

            if check_password_hash(user.password_hash, password):
                print("Password matches!")
                login_user(user)
                flash('Logged in successfully!')
                return redirect(url_for('index'))
            else:
                print("Password does not match.")
                flash('Invalid username or password.')
                return redirect(url_for('login'))
        else:
            print("User not found.")
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        user_data = {
            "username": request.form['username'],
            "password_hash": hashed_password,  # Make sure you're using password_hash
            "first_name": request.form['first_name'],
            "surname": request.form['surname'],
            "email": request.form['email']
        }

        if User.query.filter((User.username == user_data['username']) | (User.email == user_data['email'])).first():
            flash('Username or email already taken.')
            return redirect(url_for('register'))

        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        new_task = Task(
            title=request.form['title'],
            description=request.form.get('description'),
            priority=request.form.get('priority'),
            due_date=request.form.get('due_date'),
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('task_form.html')

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)