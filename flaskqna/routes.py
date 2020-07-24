from flaskqna import app, bcrypt, db
from flaskqna.forms import RegisterForm, LoginForm, QuestionForm
from flaskqna.models import User, Question, Comment
from flask import Flask, render_template, url_for, redirect, flash, request,abort
from flask_login import login_user, logout_user, current_user

# MAIN HOME ROUTE

@app.route('/home')
@app.route('/')
def home():
    questions = Question.query.all()
    comments = Comment.query.all()
    return render_template('home.html', title='Question & Answers', questions=questions, comments=comments)

# QUESTION ROUTES --------------------------------------------------------------------------------------------------

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(question=form.question.data, context=form.context.data, author=current_user)
        db.session.add(question)
        db.session.commit()
        flash('Question posted', 'success')
        return redirect(url_for('home'))
    return render_template('ask.html', title='Ask Question', form=form)
    

@app.route('/question/<int:id>', methods=['GET'])
def question_page(id):
    question = Question.query.get_or_404(id)
    user = User.query.filter_by(username=current_user.username)
    return render_template('question_page.html', question=question, user=user)


@app.route('/question/delete/<int:id>', methods=['GET', 'POST'])
def delete_question(id):
    q = question = Question.query.get_or_404(id)
    if question.user_id == current_user.id:
        db.session.delete(q)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        abort(403)
    return render_template('question_page.html', q=q)

# -------------------------------------------------------------------------------------------------------------------

# USER LOGIN ROUTES -------------------------------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered!', 'warning')
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Create An Account', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'warning')
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Logged in', 'success')   
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Incorrect username or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('home'))

# -------------------------------------------------------------------------------------------------------------------

# COMMENTS ----------------------------------------------------------------------------------------------------------

@app.route('/post/comment', methods=['POST'])
def post_comment():
    reply = request.form.get('reply')
    if reply:
        comment = Comment(comment=reply, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
    else:
        flash("You didn't write a comment", 'warning')
    return redirect(url_for('home'))


@app.route('/comment', methods=['GET'])
def view_comment():
    comments = Comment.query.all()
    return render_template('home.html', comments=comments)

# -------------------------------------------------------------------------------------------------------------------