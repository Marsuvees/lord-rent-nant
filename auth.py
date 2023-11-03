from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g,
)
from database import session as sess, Users
from bcrypt import checkpw, gensalt, hashpw
import functools

salt = gensalt()
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/accounts", methods=["POST", "GET"])
def accounts():
    return render_template("Sign in.html")


@auth_bp.route("/sign_up", methods=["POST","GET"])
def sign_up():
    if request.method == "POST":
        first_name = request.form["fname"]
        surnname = request.form["sname"]
        email = request.form["email"] 
        password = request.form["password"]
        hashed_pass = hashpw(str(password).encode("utf-8"), salt).decode("utf-8")
        user = sess.query(Users).filter_by(email=email).first()
        if user:
            print(user.name)
            return render_template("Sign in.html")
        else:
            new_user = Users(name=f"{first_name} {surnname}", email=email, password=hashed_pass)
            sess.add(new_user)
            sess.commit()
            return render_template("Sign in.html")
    return render_template("Sign in.html")

@auth_bp.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = sess.query(Users).filter_by(email = email).first()
        hashed_pass = str(user.password)
        if user == None:
            error = "No user with this email exists."
            return redirect(url_for("auth.accounts"))
        elif not checkpw(password.encode("utf-8"), hashed_pass.encode("utf-8")):
            error = "Incorrect password provided."
            return redirect(url_for("auth.accounts"))
        if error is None:
            session.clear()
            session["user_id"] = user.id 
            return redirect(url_for("home"))  
    return redirect(url_for("accounts"))


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.accounts'))


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print(user_id)
    if user_id is None:
        g.user = None
    else:
        g.user = sess.query(Users).filter_by(id=user_id).one()


def login_required(page):
    @functools.wraps(page)
    def wrapper(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.accounts"))
        return page(**kwargs)
    return wrapper



if __name__ == "__main__":
    user_index = sess.query(Users).filter_by(email = 'kiingjay77@gmail.com').first()
    if user_index:
        print('user exists')
    else:
        new_user = Users(name='Jeremiah Chibueze', email='kiingjay77@gmail.com', password=hashpw('987654321'.encode('utf-8'), salt).decode('utf-8'))
        sess.add(new_user)
        sess.commit()
        print('user created')




