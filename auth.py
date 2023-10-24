from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from database import session as sess, Users
from bcrypt import checkpw, gensalt, hashpw

salt = gensalt()
auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/create_account', methods=['GET', 'POST'])
# def create_account():
#     if request.method == 'POST':
#         name = request.form['Name']
#         email = request.form['Em@il']
#         password = request.form['Pass_word']
#         user = sess.query(Users).filter_by(email=email).first()
#         if user:
#             flash('Email already exists')
#         else:
#             new_user = Users(name=name, email=email, password=hashpw(password.encode('utf-8'), salt).decode('utf-8'))
#             sess.add(new_user)
#             sess.commit()
#             return redirect(url_for('auth.sign_in'))
#     return render_template('Sign in.html')

@auth_bp.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Em@il']
        password = request.form['Pass_word']
        user = sess.query(Users).filter_by(email=email).first()
        if user:
            flash('Email already exists')
        else:
            new_user = Users(name=name, email=email, password=hashpw(password.encode('utf-8'), salt).decode('utf-8'))
            sess.add(new_user)
            sess.commit()
            return redirect(url_for('auth.acounts'))
        login_email = request.form['Email']
        login_password = request.form['Password']
        existing_user = sess.query(Users).filter_by(email=login_email).first()
        hashed_pass = user.password
        if user and checkpw(login_password.encode('utf-8'), hashed_pass.encode('utf-8')):
            session['user_id'] = existing_user.id
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password')
    return render_template('Sign in.html')
     

if __name__ == '__main__':
    pass