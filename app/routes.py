from app import app, db
from flask import render_template, url_for, flash, redirect
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered!!!')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
