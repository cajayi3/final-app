from forms import UserLoginForm, UserSignupForm
from models import User, db
from datetime import datetime, timezone, timedelta
from werkzeug.security import check_password_hash
from flask import Blueprint, make_response, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
import logging
import jwt

auth = Blueprint('auth', __name__, template_folder='auth_templates')
logger = logging.getLogger(__name__)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('Login successful! Welcome Back.', 'auth-success')

            token = jwt.encode({'user_id': logged_user.id, 'exp': datetime.now(timezone.utc)+ timedelta(hours=2)}, current_app.config['SECRET_KEY'],
            algorithm='HS256')

            response = make_response(redirect(url_for('site.books')))
            response.set_cookie('jwt.token', token)
            return response
        else:
            flash('Invalid email or password. Please try again.', 'auth-failed')
    return render_template('signin.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            name = form.name.data
            email = form.email.data
            password = form.password.data

            # Create new user
            new_user = User(
                email=email,
                first_name=name.split()[0] if name else '',
                last_name=' '.join(name.split()[1:]) if ' ' in name else '',
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully! Please sign in.', 'auth-success')
            return redirect(url_for('auth.signin'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Signup error: {str(e)}")
            flash(f'An error occurred during signup: {str(e)}', 'auth-failed')
    
    return render_template('signup.html', form=form)
            

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('site.home'))