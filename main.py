from flask import Flask
from registration.routes import registration_bp
from login.routes import login_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(debug=True)