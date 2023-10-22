from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():	
    return render_template('Home page.html')

@app.route('/login_signup')
def login_signup():
    return render_template('/Login_Signup.html')

@app.route('/login', methods=['POST'])
def login():
    pass



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)