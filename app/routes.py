from app import app, db
from flask import render_template, url_for, flash, redirect, jsonify, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Message


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username!')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        flash('You have been logged in')
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


@app.route('/_get_json')
def get_json():
    id = request.args.get('userId', 0, type=int)
    print(id)
    messages = Message.query.filter_by(sender_id=id)
    messages = list(map(lambda x: x.body, messages))

    return jsonify({'messages': messages})



