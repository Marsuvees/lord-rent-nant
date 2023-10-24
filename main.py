from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():	
    return render_template('Home page.html')

# @app.route('/login_signup')
# def login_signup():
#     return render_template('/Sign in.html')

# @app.route('/login', methods=['POST'])
# def login():
#     pass

from auth import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)