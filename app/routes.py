from flask import render_template, Blueprint, request, redirect, url_for, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from .models import User,Task
from .database import db

blueprint = Blueprint('app', __name__)

@blueprint.route('/login', methods=["POST", "GET"])
def login():
    # session.clear()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email:
            print("Please provide username")
            return redirect("/login")
        elif not password:
            print("Please provide password")
            return redirect("/login")
        
        user = User.query.filter_by(email=email).first()
        # print(user.password)
        # hash=generate_password_hash(password)
        # print(hash)
        # print(user.password == password)
        if not user or not (user.password == password):
            print("Invalid username or password")
            return redirect("/login")
        
        # session["user_id"] = user.id

        return redirect("/dashboard")
    
    else:
        return render_template("login.html")

@blueprint.route('/', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        emailid = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirm_password')
        if not emailid:
            print('Please provide username')
            return redirect('/')
        elif not password or not confirmation:
            print('Please provide password')
            return redirect('/')
        elif confirmation:
            if password != confirmation:
                print('Passwords do not match')
                return redirect('/')
        
        existing_user = User.query.filter_by(email=emailid).first()
        if existing_user:
            print('Username already exists!')
            return redirect('/')
        
        new_user = User(email=emailid, password=password)
        db.session.add(new_user)
        db.session.commit()
        print('Account created successfully! Please log in.')
        return redirect('/login')
    
    # else:
    #     return render_template("signup.html")
    return render_template('signup.html')

@blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@blueprint.route('/create_task')
def create_task():
    return render_template('create_task.html')

@blueprint.route('/edit_task', methods=["GET", "POST"])
def edit_task():
    # if request.method == 'POST':
        # Update the task data in your database
        # title = request.form['Task title']
        # description = request.form['Description']
        # Update the task data in your database
        # return redirect(url_for('/view_task'))
                                # , task_id=task_id))
    # else:
        # Get the task data from your database
        # task = get_task_from_database(task_id)
    return render_template('edit_task.html')
                            #    , task=task)

@blueprint.route('/view_task')
def view_task():
    return render_template('view_task.html')

@blueprint.route('/changepw')
def changepw():
    return render_template('changepw.html')
