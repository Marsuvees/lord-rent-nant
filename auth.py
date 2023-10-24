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
    return render_template("Sign In.html")


@auth_bp.route("/process_form", methods=["POST"])
def process_form():
    if request.method == "POST":
        if request.form["submit"] == "sign_in":
            email = request.form["email"]
            password = request.form["password"]
            user = sess.query(Users).filter_by(email=email).first()
            if user and checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                session["user_id"] = user.id
                return redirect(url_for("main.home"))
            else:
                print("wrong email or password")
                return render_template("Sign in.html")
        elif request.form["submit"] == "sign_up":
            name = request.form["new_name"]
            email = request.form["new_email"]
            password = hashpw(
                request.form["new_password"].encode("utf-8"), salt
            ).decode("utf-8")
            user = sess.query(Users).filter_by(email=email).first()
            if user:
                print("Email already exists")
                flash("Email already exists")
            else:
                new_user = Users(name=name, email=email, password=password)
                sess.add(new_user)
                sess.commit()
                return redirect(url_for("accounts"))
    return redirect(url_for("accounts"))


if __name__ == "__main__":
    pass