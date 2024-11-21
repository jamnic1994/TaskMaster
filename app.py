from datetime import datetime, date

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task, TaskGroup, CompletedTask
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():

    # If the user is already logged in, redirect them to the index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'error')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password.', 'error')
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
            flash('Username or email already taken.', 'error')
            return redirect(url_for('register'))

        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/index')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.priority).all()
    # Fetch all groups for the current user
    groups = TaskGroup.query.filter_by(user_id=current_user.id).all()
    tasks_group = {group.id: Task.query.filter_by(user_id=current_user.id, group_id=group.id).all() for group in groups}
    return render_template('index.html', tasks=tasks, groups=groups, tasks_by_group=tasks_group)



@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        # Process form submission
        group_id = request.form.get('group')  # Get the selected group

        new_task = Task(
            title=request.form['title'],
            description=request.form['description'],
            priority=int(request.form['priority']),
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d'),
            group_id=int(group_id) if group_id else None,  # Assign group if selected
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))

    groups = TaskGroup.query.filter_by(user_id=current_user.id).all()  # Fetch user's groups
    return render_template('task_form.html', groups=groups)

@app.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Update task fields from form data
    task.title = request.form['title']
    task.priority = request.form['priority']
    task.status = request.form['status']

    # Convert due_date string to a Python date object, handle empty input
    due_date = request.form['due_date']
    if due_date:
        try:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()  # Parse string to date
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('index'))
    else:
        task.due_date = None  # Clear the due date if input is empty

    # Handle group_id
    group_id = request.form.get('group_id')
    task.group_id = int(group_id) if group_id else None

    # Commit changes to the database
    db.session.commit()
    flash('Task updated successfully', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/manage_groups', methods=['GET', 'POST'])
@login_required
def manage_groups():
    if request.method == 'POST':
        group_name = request.form['group_name']
        description = request.form.get('description', '')
        new_group = TaskGroup(name=group_name, description=description, user_id=current_user.id)
        db.session.add(new_group)
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('manage_groups'))

    groups = TaskGroup.query.filter_by(user_id=current_user.id).all()
    tasks = {group.id: Task.query.filter_by(group_id=group.id).all() for group in groups}

    return render_template('manage_groups.html', groups=groups, tasks=tasks)

@app.route('/edit-group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = TaskGroup.query.get_or_404(group_id)
    if request.method == 'POST':
        group.name = request.form['name']
        db.session.commit()
        flash('Group updated successfully!', 'success')
        return redirect(url_for('manage_groups'))
    return render_template('edit_group.html', group=group)


@app.route('/update_group/<int:group_id>', methods=['POST'])
@login_required
def update_group(group_id):
    group = TaskGroup.query.get_or_404(group_id)  # Fetch the group or return 404

    # Check if the current user owns the group
    if group.user_id != current_user.id:
        flash('Unauthorized action!', 'error')
        return redirect(url_for('manage_groups'))

    # Update the group's name and description
    group.name = request.form['group_name']
    group.description = request.form.get('description', '')  # Optional field

    db.session.commit()  # Save changes to the database
    flash('Group updated successfully.', 'success')
    return redirect(url_for('manage_groups'))


@app.route('/delete-group/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    group = TaskGroup.query.get_or_404(group_id)  # Fetch the group or return 404

    if group.user_id != current_user.id:
        flash('Unauthorized action!', 'error')
        return redirect(url_for('manage_groups'))

    db.session.delete(group)
    db.session.commit()
    flash('Group deleted successfully!', 'success')
    return redirect(url_for('manage_groups'))

@app.route('/index/<int:group_id>')
@login_required
def tasks_by_group(group_id):
    # Fetch tasks for the specified group
    tasks = Task.query.filter_by(user_id=current_user.id, group_id=group_id).all()
    # Fetch the group itself
    group = TaskGroup.query.get_or_404(group_id)
    return render_template('index.html', tasks=tasks, group=group)

@app.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Copy task details to CompletedTask
    completed_task = CompletedTask(
        user_id=task.user_id,
        title=task.title,
        group_id=task.group_id,
        completed_date=date.today()
    )

    # Add to CompletedTask table and delete from Task table
    db.session.add(completed_task)
    db.session.delete(task)
    db.session.commit()

    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))

@app.route('/completed-tasks')
@login_required
def completed_tasks():
    completed_tasks = CompletedTask.query.filter_by(user_id=current_user.id).all()
    return render_template('completed_tasks.html', completed_tasks=completed_tasks)

@app.route('/account', methods=['GET'])
@login_required
def account():
    # Get the user's tasks
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    completed_tasks = CompletedTask.query.filter_by(user_id=current_user.id).all()

    # Count the tasks
    total_tasks = len(tasks)
    completed_task_count = len(completed_tasks)

    return render_template('account.html', total_tasks=total_tasks, completed_task_count=completed_task_count)


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Delete the current user from the database
    db.session.delete(current_user)
    db.session.commit()

    # Log out the user after deletion
    logout_user()

    # Redirect to the login page or homepage
    return redirect(url_for('login'))

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Validate current password
    if not check_password_hash(current_user.password_hash, current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('account'))

    # Validate new password
    if new_password != confirm_password:
        flash('New password and confirmation do not match.', 'danger')
        return redirect(url_for('account'))

    # Update the password
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    flash('Your password has been updated.', 'success')
    return redirect(url_for('account'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def update_account():
    if request.method == 'POST':
        # Update user details
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.email = request.form['email']
        current_user.username = request.form['username']
        db.session.commit()
        flash('Your details have been updated!', 'success')
        return redirect(url_for('account'))

    return render_template('account.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
