from flask import Flask, render_template
from auth import login_required, load_logged_in_user

app = Flask(__name__)
app.secret_key = "DEV"

@app.route('/')
@app.route('/houses')
# @login_required
def home():	
    return render_template('Home page.html')

from auth import auth_bp
app.register_blueprint(auth_bp)

@app.route('/payments')
def payments():
    return render_template('table-payments.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)