from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "DEV"

@app.route('/')
def home():	
    return render_template('Home page.html')

from auth import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)