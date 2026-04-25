from flask import Blueprint, render_template, request, flash, redirect, url_for
from supabase_client import supabase

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            return redirect(url_for('registration.platform'))
        except Exception as e:
            flash(f'Login failed: {str(e)}')
            return redirect(url_for('login.login'))
    return render_template('index.html')