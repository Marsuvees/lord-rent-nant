from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import Landlords, Tenants, session as sess
from bcrypt import checkpw, gensalt, hashpw

auth_bp = Blueprint('auth', __name__)
salt = gensalt()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        status = request.form['status']
        email = request.form['email']
        password = request.form['password']
        if status.lower() == 'landlord':
            user = sess.query(Landlords).filter_by(email=email).first()
            if user:    
                return render_template('auth/register.html', error='Email already exists')
            else:
                new_user = Landlords(name=f'{first_name} {middle_name} {last_name}', email=email, password=hashpw(password.encode('utf-8'), salt).decode())
                sess.add(new_user)
                sess.commit()
                return redirect(url_for('auth.login')) 
        elif status.lower() == 'tenant':
            user = sess.query(Tenants).filter_by(email=email).first()
            if user:
                return render_template('auth/register.html', error='Email already exists')
            else:
                new_user = Tenants(name=f'{first_name} {middle_name} {last_name}', email=email, password=hashpw(password.encode('utf-8'), salt).decode())
                sess.add(new_user)
                sess.commit()
                return redirect(url_for('auth.login')) 
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('auth/login.html')

if __name__ == '__main__':
    pass 
