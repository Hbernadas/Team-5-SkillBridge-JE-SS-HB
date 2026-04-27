from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from supabase_client import supabase_admin
from functools import wraps
from datetime import datetime, timezone, timedelta

jobs_bp = Blueprint('jobs', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated


def _user_ctx(uid):
    rows = supabase_admin.table('profiles').select('first_name, last_name, profile_photo_url').eq('user_id', uid).execute().data
    return rows[0] if rows else {}


def _viewed_ids(uid):
    rows = supabase_admin.table('job_views').select('job_id').eq('user_id', uid).execute().data or []
    return {r['job_id'] for r in rows}


# ─── Explore ─────────────────────────────────────────────────────────────────

@jobs_bp.route('/explore')
@login_required
def explore():
    uid = session['user_id']
    jobs = supabase_admin.table('jobs').select(
        'id, title, company, location, job_type, salary_range, deadline'
    ).eq('is_active', True).order('created_at', desc=True).limit(3).execute().data or []

    viewed = _viewed_ids(uid)
    return render_template('explore.html',
        jobs=jobs, viewed_ids=viewed,
        user=_user_ctx(uid), page='explore',
    )


# ─── Jobs listing ─────────────────────────────────────────────────────────────

@jobs_bp.route('/jobs')
@login_required
def jobs_list():
    uid = session['user_id']
    q = request.args.get('q', '').strip()

    query = supabase_admin.table('jobs').select(
        'id, title, company, location, job_type, salary_range, deadline'
    ).eq('is_active', True)

    if q:
        query = query.or_(f'title.ilike.%{q}%,company.ilike.%{q}%,location.ilike.%{q}%')

    jobs = query.order('created_at', desc=True).execute().data or []
    viewed = _viewed_ids(uid)

    return render_template('jobs.html',
        jobs=jobs, viewed_ids=viewed, q=q,
        user=_user_ctx(uid), page='jobs',
    )


# ─── Job detail ───────────────────────────────────────────────────────────────

@jobs_bp.route('/jobs/<job_id>')
@login_required
def job_detail(job_id):
    uid = session['user_id']

    rows = supabase_admin.table('jobs').select('*').eq('id', job_id).eq('is_active', True).execute().data
    if not rows:
        return redirect(url_for('jobs.jobs_list'))
    job = rows[0]

    try:
        supabase_admin.table('job_views').insert({'user_id': uid, 'job_id': job_id}).execute()
    except Exception:
        pass

    app_rows = supabase_admin.table('applications').select('*').eq('user_id', uid).eq('job_id', job_id).execute().data
    application = app_rows[0] if app_rows else None

    if application and application.get('status') == 'Under Review':
        submitted_at = datetime.fromisoformat(application['submitted_at'].replace('Z', '+00:00'))
        if datetime.now(timezone.utc) - submitted_at > timedelta(seconds=5):
            supabase_admin.table('applications').update({'status': 'Denied'}).eq('id', application['id']).execute()
            application['status'] = 'Denied'

    return render_template('job_detail.html',
        job=job, application=application,
        user=_user_ctx(uid), page='jobs',
    )


# ─── Apply ────────────────────────────────────────────────────────────────────

@jobs_bp.route('/jobs/<job_id>/apply', methods=['POST'])
@login_required
def apply(job_id):
    uid = session['user_id']
    existing = supabase_admin.table('applications').select('id').eq('user_id', uid).eq('job_id', job_id).execute().data
    if not existing:
        supabase_admin.table('applications').insert({'user_id': uid, 'job_id': job_id}).execute()
        flash('Your application has been submitted successfully.')
    return redirect(url_for('jobs.job_detail', job_id=job_id))


# ─── My Jobs ──────────────────────────────────────────────────────────────────

@jobs_bp.route('/my-jobs')
@login_required
def my_jobs():
    uid = session['user_id']
    apps = supabase_admin.table('applications').select(
        '*, jobs(title, company, location, job_type)'
    ).eq('user_id', uid).order('submitted_at', desc=True).execute().data or []

    return render_template('my_jobs.html',
        apps=apps, user=_user_ctx(uid), page='my_jobs',
    )
