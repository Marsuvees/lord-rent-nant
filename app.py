from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'developer'

from auth import auth_bp

app.register_blueprint(auth_bp)

if __name__ == '__main__': 
    app.run(port=5000, host='0.0.0.0', debug=True)