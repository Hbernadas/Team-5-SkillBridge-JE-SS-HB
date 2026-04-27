from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from supabase_client import supabase, supabase_admin

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
                return redirect(url_for('jobs.explore'))
            return redirect(url_for('profile.wizard_step1'))
        except Exception as e:
            try:
                users = supabase_admin.auth.admin.list_users()
                if email not in [u.email for u in users]:
                    flash('Account does not exist.')
                else:
                    flash('Invalid login credentials.')
            except Exception:
                flash('Login failed. Please try again.')
            return redirect(url_for('login.login'))
    return render_template('index.html')


@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))