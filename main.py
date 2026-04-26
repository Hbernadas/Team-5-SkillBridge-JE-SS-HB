from flask import Flask
from datetime import datetime
from registration.routes import registration_bp
from login.routes import login_bp
from profile.routes import profile_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload

app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)

@app.template_filter('fmt_date')
def fmt_date(value):
    if not value:
        return ''
    try:
        return datetime.strptime(str(value)[:10], '%Y-%m-%d').strftime('%b %Y')
    except Exception:
        return str(value)

if __name__ == '__main__':
    app.run(debug=True)