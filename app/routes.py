from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from app.models import User, UserRole
from app.forms import LoginForm, RegisterForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=['GET'])
def home():
    first_name = "Karthik"
    last_name = "P"
    email = "karthik@bicsglobal.com"
    hashed_pw = generate_password_hash("admin@123")
    new_user = User(
        first_name = first_name,
        last_name = last_name,
        email=email,
        password=hashed_pw,
        role=UserRole["ADMIN"]
    )
    user = User.query.filter_by(email=email).first()
    if not user:
        db.session.add(new_user)
        db.session.commit()

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid username or password")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/manage-users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != UserRole.ADMIN:
        flash("Access denied")
        return redirect(url_for('dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email=form.email.data,
            password=hashed_pw,
            role=UserRole[form.role.data]
        )
        db.session.add(user)
        db.session.commit()
        flash("User created successfully")
        return redirect(url_for('manage_users'))

    users = User.query.all()
    return render_template('manage_users.html', users=users, form=form)
