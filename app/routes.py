from flask import render_template, Blueprint, request, redirect, url_for,flash, request, session, Flask
from werkzeug.security import check_password_hash, generate_password_hash
# from sqlalchemy import desc
from .models import User,Task
from .database import db
from datetime import date, datetime

blueprint = Blueprint('app', __name__)
app = Flask(__name__,template_folder='../templates', static_folder='../static')


from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@blueprint.route('/login', methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email:
            error = "Please provide username"
            return render_template("login.html", error=error)
        elif not password:
            error = "Please provide password"
            return render_template("login.html", error=error)
        
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            error = "Invalid username or password"
            return render_template("login.html", error=error)
        
        session["user_id"] = user.id

        return redirect("/")
    
    return render_template("login.html")

@blueprint.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        emailid = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirm_password')
        if not emailid:
            error = 'Please provide an email'
            return render_template("signup.html", error=error)
        elif not password or not confirmation:
            error = 'Please provide password'
            return render_template("signup.html", error=error)
        elif confirmation:
            if password != confirmation:
                error = 'Passwords do not match'
                return render_template("signup.html", error=error)
        
        existing_user = User.query.filter_by(email=emailid).first()
        if existing_user:
            error = 'Username already exists!'
            return render_template("signup.html", error=error)
        hash = generate_password_hash(password)
        new_user = User(email=emailid, password=hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect('/login')
    
    return render_template('signup.html')

@blueprint.route('/')
@login_required
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access your dashboard')
        return redirect('/login')
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect('/login')
    
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.deadline).all()
    
    return render_template('dashboard.html', tasks=tasks, user=user)

@blueprint.route('/create_task', methods=["GET", "POST"])
@login_required
def create_task():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to create tasks')
        return redirect('/login')

    if request.method == 'POST':
        title = request.form.get('Title')
        description = request.form.get('Description')
        deadline = request.form.get('Deadline')
        
        if not title:
            flash('Title is required')
            return redirect('/create_task')

        if not deadline:
            flash("Deadline is required")
            return redirect('/create_task')
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

        new_task = Task(
            created_on=date.today(),
            user_id=user_id,
            title=title,
            description=description,
            deadline=deadline,
            status='Not Done'
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect('/')

    return render_template('create_task.html')

@blueprint.route('/edit_task/<int:id>', methods=["GET", "POST"])
@login_required
def edit_task(id):
    task = Task.query.get(id)
    if not task:
        return redirect('/')

    if request.method == 'POST':
        task.title = request.form.get('Task title')
        task.description = request.form.get('Description')
        deadline = request.form.get('Deadline')
        print(f"Title: {task.title}, Description: {task.description}, Due Date: {deadline}")
        if deadline:
            try:
                task.deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.')
                return redirect(url_for('edit_task', id=task.id))

        db.session.commit()
        return redirect('/')
        
    # else:
    return render_template('edit_task.html', task=task)

@blueprint.route('/view_task/<int:id>', methods=['GET','POST'])
@login_required
def view_task(id):
    task = Task.query.get_or_404(id)
    return render_template('view_task.html', task=task)

@blueprint.route('/delete_task/<int:id>')
@login_required
def delete_task(id):
    task_to_del = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_del)
        db.session.commit()
    except:
        flash('There was a problem deleting that task')
    return redirect('/')
    
@blueprint.route('/markdone/<int:id>')
@login_required
def markdone(id):
    task = Task.query.get(id)
    if task.status == 'Done':
        task.status = 'Not Done'
    else:
        task.status = 'Done'
    db.session.commit()
    return redirect('/')

@blueprint.route('/changepw', methods=["POST", "GET"])
@login_required
def changepw():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        newpass = request.form.get('newpassword')
        confirmation = request.form.get('confirmation')
        
        if not email or not password or not newpass or not confirmation:
            flash("Please fill all fields!")
            return redirect('/changepw')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password")
            return redirect("/changepw")

        if newpass != confirmation:
            flash("Passwords do not match")
            return redirect("/changepw")      
        
        user.password = generate_password_hash(newpass)
        db.session.commit()

        return redirect("/login")
    
    return render_template('changepw.html')

@blueprint.route('/logout')
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@blueprint.route('/completion_rates', methods=['GET', 'POST'])
def completion_rates():
    if request.method == 'POST':
        selected_month = request.form.get('selected_month')
        selected_year = request.form.get('selected_year')
        selected_date = datetime.strptime(f'{selected_year}-{selected_month}', '%Y-%m')
        start_date = selected_date.replace(day=1)
        end_date = selected_date.replace(day=1, month=int(selected_month) % 12 + 1, year=int(selected_year) if int(selected_month) % 12 != 0 else int(selected_year) + 1)
        
        completed_tasks = Task.query.filter(Task.deadline >= start_date, Task.deadline < end_date, Task.status == 'Done').count()
        incomplete_tasks = Task.query.filter(Task.deadline >= start_date, Task.deadline < end_date, Task.status == 'Not Done').count()

        return render_template('pie_chart.html', completed_tasks=completed_tasks, incomplete_tasks=incomplete_tasks, selected_month=selected_month, selected_year=selected_year)

    return render_template('completion_rates.html')