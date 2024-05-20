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
            flash("Please provide username")
            return redirect("/login")
        elif not password:
            flash("Please provide password")
            return redirect("/login")
        
        user = User.query.filter_by(email=email).first()
        # print(user.password)
        # hash=generate_password_hash(password)
        # print(hash)
        # print(user.password == password)
        if not user or not (user.password == password):
            flash("Invalid username or password")
            return redirect("/login")
        
        session["user_id"] = user.id
        # print(session["user_id"])

        return redirect("/")
    
    else:
        return render_template("login.html")

@blueprint.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        emailid = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirm_password')
        if not emailid:
            print('Please provide an email')
            return redirect('/signup')
        elif not password or not confirmation:
            print('Please provide password')
            return redirect('/signup')
        elif confirmation:
            if password != confirmation:
                print('Passwords do not match')
                return redirect('/signup')
        
        existing_user = User.query.filter_by(email=emailid).first()
        if existing_user:
            print('Username already exists!')
            return redirect('/signup')
        
        new_user = User(email=emailid, password=password)
        db.session.add(new_user)
        db.session.commit()
        print('Account created successfully! Please log in.')
        return redirect('/login')
    
    # else:
    #     return render_template("signup.html")
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

        if deadline:
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        else:
            flash('Deadline is required')
            return redirect('/create_task')

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

        flash('Task created successfully!')
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
                # flash('Invalid date format. Please use YYYY-MM-DD.')
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
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
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

@blueprint.route('/changepw')
@login_required
def changepw():
    return render_template('changepw.html')

@blueprint.route('/logout')
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")