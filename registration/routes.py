from flask import Blueprint, render_template, request, flash, redirect, url_for
from supabase_client import supabase

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Sign up the user; Supabase handles confirmation email and credentials storage
            supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            return render_template('registration.html', show_success=True)
        except Exception as e:
            flash(f'Registration failed: {str(e)}')
            return redirect(url_for('registration.register'))
    return render_template('registration.html', show_success=False)

@registration_bp.route('/platform')
def platform():
    try:
        # Check if user is authenticated
        user = supabase.auth.get_user()
        return render_template('platform.html', user=user)
    except Exception as e:
        flash('Please confirm your email first.')
        return redirect(url_for('login.login'))