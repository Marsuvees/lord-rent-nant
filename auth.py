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


# @auth_bp.route("/create_account", methods=["GET", "POST"])
# def create_account():
#     if request.method == "POST":
#         name = request.form["Name"]
#         email = request.form["Em@il"]
#         password = request.form["Pass_word"]
#         user = sess.query(Users).filter_by(email=email).first()
#         if user:
#             flash("Email already exists")
#         else:
#             new_user = Users(
#                 name=name,
#                 email=email,
#                 password=hashpw(password.encode("utf-8"), salt).decode("utf-8"),
#             )
#             sess.add(new_user)
#             sess.commit()
#             return redirect(url_for("auth.sign_in"))
#     return render_template("Sign in.html")


@auth_bp.route("/accounts", methods=["POST", "GET"])
def accounts():
    return render_template("Sign in.html")


@auth_bp.route("/process_form", methods=["POST"])
def process_form():
    if request.method == "POST":
        if request.form.get("submit") == "sign_in":
            error = None
            email = request.form["email"]
            password = request.form["password"]
            user = sess.query(Users).filter_by(email=email).first()
            if user and checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                session["user_id"] = user.id
                error = None
                return redirect(url_for("main.home"))
            else:
                error = "Invalid email or password"
                print("wrong email or password")
                return render_template("Sign in.html")
            if error is not None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for("auth.sign_in"))
        elif request.form.get("submit") == "create_account":
            name = request.form["name"]
            email = request.form["email"]
            password = hashpw(
                request.form["password"].encode("utf-8"), salt
            ).decode("utf-8")
            user = sess.query(Users).filter_by(email=email).first()
            if user:
                print("Email already exists")
                flash("Email already exists")
            else:
                new_user = Users(name=name, email=email, password=password)
                sess.add(new_user)
                sess.commit()
                print("New user added")
                return redirect(url_for("accounts"))
            
    return redirect(url_for("accounts"))

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
            return redirect(url_for("auth.sign_in"))
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




