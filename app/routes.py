from app import app, db
from flask import render_template, url_for, flash, redirect, jsonify, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Message, Chat


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index/<username>')
def index(username=None):
    print(username)
    return render_template('index.html', username=username)


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


@app.route('/_get_chats')
def get_chats():
    user_name = request.args.get('userName', '', type=str)
    user = User.query.filter_by(username=user_name).first()
    response = {}
    for chat in user.chats:
        username = [user.username for user in chat.users if user != current_user][0]
        last_messages = sorted(chat.messages, key=lambda x: x.timestamp)
        if last_messages:
            last_message_timestamp = last_messages[-1].timestamp
            last_message_body = last_messages[-1].body
        else:
            last_message_timestamp = ''
            last_message_body = ''
        response.update({f"{str(chat.id)}": {"users": {"username": username},
                                                  "last_message": last_message_body,
                                                  "timestamp": last_message_timestamp,
                                                  }
                         })
    return jsonify(response)


@app.route('/_get_chat_messages')
def get_chat_messages():
    id = int(request.args.get("chat_Id", 0, type=str))
    chat = Chat.query.filter_by(id=id).first()
    messages = chat.messages
    for message in messages:
        # print(message)
        pass
    response = {}
    for num, message in enumerate(messages):
        response.update({f'message_{str(num)}': {'body': message.body,
                                                 'timestamp': message.timestamp,
                                                 'user': 'current_user' if message.author == current_user else 'recipient'}})
    print(response)
    return jsonify(response)


@app.route('/send_message', methods=['POST'])
def send_message():
    body = request.args.get('body', 0, type=str)
    chat_id = request.args.get('chat_Id', 0, type=str)
    chat = Chat.query.get(int(chat_id[-1]))  # если чатов будет больше 9, то ничего не сработает!!!
    if chat is not None:
        message = Message(sender_id=current_user.id,
                          recipient_id=chat.users[0].id if chat.users[0] != current_user else chat.users[1].id,
                          body=body,
                          chat_id=chat.id)
        db.session.add(message)
        chat.messages.append(message)
        db.session.commit()
    else:
        pass
    return jsonify('200')


@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    image = user.avatar_path
    return render_template('profile.html', image=image, username=username)


@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)
