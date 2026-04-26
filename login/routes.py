from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from supabase_client import supabase

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session['user_id'] = result.user.id
            session['email'] = result.user.email
            session['access_token'] = result.session.access_token

            profile = supabase.table('profiles').select('user_id').eq('user_id', result.user.id).execute()
            if profile.data:
                return redirect(url_for('profile.view_profile'))
            return redirect(url_for('profile.wizard_step1'))
        except Exception as e:
            flash(f'Login failed: {str(e)}')
            return redirect(url_for('login.login'))
    return render_template('index.html')