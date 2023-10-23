from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from database import session as sess, Users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['E']
        password = request.form['password']
        user = sess.query(Users).filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password')

    return render_template('Sign in.html')
    pass 

if __name__ == '__main__':
    pass