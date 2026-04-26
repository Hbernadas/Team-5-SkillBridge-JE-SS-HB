from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from supabase_client import supabase, supabase_admin
from functools import wraps

profile_bp = Blueprint('profile', __name__)

US_STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
    'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia',
    'Puerto Rico', 'Guam', 'U.S. Virgin Islands', 'American Samoa',
    'Northern Mariana Islands',
]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated


def _upload_photo(user_id, photo_file):
    ext = photo_file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ('jpg', 'jpeg', 'png'):
        return None, 'Only JPG and PNG files are allowed.'
    data = photo_file.read()
    if len(data) > 2 * 1024 * 1024:
        return None, 'Photo must be under 2MB.'
    path = f"{user_id}.{ext}"
    try:
        supabase_admin.storage.from_('profile-photos').upload(path, data, {'content-type': photo_file.content_type})
    except Exception:
        supabase_admin.storage.from_('profile-photos').update(path, data, {'content-type': photo_file.content_type})
    url = supabase_admin.storage.from_('profile-photos').get_public_url(path)
    return url, None


def _save_social(uid, form):
    data = {
        'linkedin_url': form.get('linkedin_url', '').strip() or None,
        'github_url':   form.get('github_url',   '').strip() or None,
        'other_url':    form.get('other_url',     '').strip() or None,
    }
    existing = supabase.table('social_links').select('id').eq('user_id', uid).execute().data
    if existing:
        supabase.table('social_links').update(data).eq('user_id', uid).execute()
    else:
        supabase.table('social_links').insert({**data, 'user_id': uid}).execute()


# ─── Wizard ──────────────────────────────────────────────────────────────────

@profile_bp.route('/profile/wizard/1', methods=['GET', 'POST'])
@login_required
def wizard_step1():
    uid = session['user_id']
    if supabase.table('profiles').select('user_id').eq('user_id', uid).execute().data:
        return redirect(url_for('profile.view_profile'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name',  '').strip()
        if not first_name or not last_name:
            flash('First name and last name are required.')
            return redirect(url_for('profile.wizard_step1'))

        photo_url = None
        photo = request.files.get('profile_photo')
        if photo and photo.filename:
            photo_url, err = _upload_photo(uid, photo)
            if err:
                flash(err)
                return redirect(url_for('profile.wizard_step1'))

        supabase.table('profiles').upsert({
            'user_id': uid, 'first_name': first_name,
            'last_name': last_name, 'profile_photo_url': photo_url,
        }).execute()
        return redirect(url_for('profile.wizard_step2'))

    return render_template('wizard_step1.html')


@profile_bp.route('/profile/wizard/2', methods=['GET', 'POST'])
@login_required
def wizard_step2():
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action in ('skip', 'next'):
            return redirect(url_for('profile.wizard_step3'))
        if action == 'add':
            school_name = request.form.get('school_name', '').strip()
            if school_name:
                currently_attending = 'currently_attending' in request.form
                supabase.table('education').insert({
                    'user_id': uid,
                    'school_name': school_name,
                    'education_level': request.form.get('education_level', ''),
                    'currently_attending': currently_attending,
                    'start_date': request.form.get('start_date') or None,
                    'end_date': None if currently_attending else (request.form.get('end_date') or None),
                    'area_of_study': request.form.get('area_of_study', '').strip(),
                    'description': request.form.get('description', '').strip()[:250],
                }).execute()
            else:
                flash('School name is required to add an entry.')
        if action == 'delete':
            eid = request.form.get('entry_id')
            if eid:
                supabase.table('education').delete().eq('id', eid).eq('user_id', uid).execute()

    entries = supabase.table('education').select('*').eq('user_id', uid).execute().data
    return render_template('wizard_step2.html', entries=entries)


@profile_bp.route('/profile/wizard/3', methods=['GET', 'POST'])
@login_required
def wizard_step3():
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action in ('skip', 'next'):
            return redirect(url_for('profile.wizard_step4'))
        if action == 'add':
            employer_name = request.form.get('employer_name', '').strip()
            if employer_name:
                currently_working = 'currently_working' in request.form
                start_date = request.form.get('start_date') or None
                if not start_date:
                    flash('Start date is required for experience entries.')
                else:
                    supabase.table('experience').insert({
                        'user_id': uid,
                        'employer_name': employer_name,
                        'job_title': request.form.get('job_title', '').strip(),
                        'job_type': request.form.get('job_type', ''),
                        'currently_working': currently_working,
                        'start_date': start_date,
                        'end_date': None if currently_working else (request.form.get('end_date') or None),
                        'city': request.form.get('city', '').strip(),
                        'state': request.form.get('state', ''),
                        'description': request.form.get('description', '').strip()[:500],
                    }).execute()
            else:
                flash('Employer name is required to add an entry.')
        if action == 'delete':
            eid = request.form.get('entry_id')
            if eid:
                supabase.table('experience').delete().eq('id', eid).eq('user_id', uid).execute()

    entries = supabase.table('experience').select('*').eq('user_id', uid).execute().data
    return render_template('wizard_step3.html', entries=entries, states=US_STATES)


@profile_bp.route('/profile/wizard/4', methods=['GET', 'POST'])
@login_required
def wizard_step4():
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action in ('skip', 'next'):
            return redirect(url_for('profile.wizard_step5'))
        if action == 'save':
            selected_ids = request.form.getlist('skill_ids')[:15]
            supabase.table('user_skills').delete().eq('user_id', uid).execute()
            for sid in selected_ids:
                supabase.table('user_skills').insert({'user_id': uid, 'skill_id': int(sid)}).execute()
            return redirect(url_for('profile.wizard_step5'))

    all_skills = supabase.table('skills_list').select('*').order('name').execute().data
    user_skill_ids = [s['skill_id'] for s in supabase.table('user_skills').select('skill_id').eq('user_id', uid).execute().data]
    return render_template('wizard_step4.html', all_skills=all_skills, user_skill_ids=user_skill_ids)


@profile_bp.route('/profile/wizard/5', methods=['GET', 'POST'])
@login_required
def wizard_step5():
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action in ('skip', 'next'):
            return redirect(url_for('profile.wizard_step6'))
        if action == 'add':
            title = request.form.get('title', '').strip()
            if title:
                currently_working = 'currently_working' in request.form
                supabase.table('projects').insert({
                    'user_id': uid,
                    'title': title,
                    'role': request.form.get('role', '').strip() or None,
                    'currently_working': currently_working,
                    'start_date': request.form.get('start_date') or None,
                    'end_date': None if currently_working else (request.form.get('end_date') or None),
                    'url': request.form.get('url', '').strip() or None,
                    'description': request.form.get('description', '').strip() or None,
                }).execute()
            else:
                flash('Project title is required to add an entry.')
        if action == 'delete':
            eid = request.form.get('entry_id')
            if eid:
                supabase.table('projects').delete().eq('id', eid).eq('user_id', uid).execute()

    entries = supabase.table('projects').select('*').eq('user_id', uid).execute().data
    return render_template('wizard_step5.html', entries=entries)


@profile_bp.route('/profile/wizard/6', methods=['GET', 'POST'])
@login_required
def wizard_step6():
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'skip':
            return redirect(url_for('profile.view_profile'))
        if action == 'save':
            _save_social(uid, request.form)
            return redirect(url_for('profile.view_profile'))

    existing = supabase.table('social_links').select('*').eq('user_id', uid).execute().data
    social = existing[0] if existing else {}
    return render_template('wizard_step6.html', social=social)


# ─── Profile View ─────────────────────────────────────────────────────────────

@profile_bp.route('/profile')
@login_required
def view_profile():
    uid = session['user_id']
    profile_rows = supabase.table('profiles').select('*').eq('user_id', uid).execute().data
    profile = profile_rows[0] if profile_rows else {}

    education  = supabase.table('education').select('*').eq('user_id', uid).order('id', desc=True).execute().data
    experience = supabase.table('experience').select('*').eq('user_id', uid).order('id', desc=True).execute().data
    projects   = supabase.table('projects').select('*').eq('user_id', uid).order('id', desc=True).execute().data

    skill_rows = supabase.table('user_skills').select('skills_list(id, name)').eq('user_id', uid).execute().data
    skills = [s['skills_list'] for s in skill_rows if s.get('skills_list')]

    social_rows = supabase.table('social_links').select('*').eq('user_id', uid).execute().data
    social = social_rows[0] if social_rows else {}

    return render_template('profile.html',
        profile=profile, education=education, experience=experience,
        skills=skills, projects=projects, social=social,
        email=session.get('email'),
    )


# ─── Edit Routes ──────────────────────────────────────────────────────────────

@profile_bp.route('/profile/edit/basic', methods=['GET', 'POST'])
@login_required
def edit_basic():
    uid = session['user_id']
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name',  '').strip()
        if not first_name or not last_name:
            flash('First name and last name are required.')
            return redirect(url_for('profile.edit_basic'))

        existing = supabase.table('profiles').select('profile_photo_url').eq('user_id', uid).execute().data
        photo_url = existing[0].get('profile_photo_url') if existing else None

        photo = request.files.get('profile_photo')
        if photo and photo.filename:
            new_url, err = _upload_photo(uid, photo)
            if err:
                flash(err)
                return redirect(url_for('profile.edit_basic'))
            photo_url = new_url

        supabase.table('profiles').upsert({
            'user_id': uid, 'first_name': first_name,
            'last_name': last_name, 'profile_photo_url': photo_url,
        }).execute()
        flash('Basic info updated.')
        return redirect(url_for('profile.view_profile'))

    profile_rows = supabase.table('profiles').select('*').eq('user_id', uid).execute().data
    profile = profile_rows[0] if profile_rows else {}
    return render_template('edit_basic.html', profile=profile)


@profile_bp.route('/profile/edit/education', methods=['GET', 'POST'])
@profile_bp.route('/profile/edit/education/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_education(entry_id=None):
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'delete':
            eid = request.form.get('entry_id')
            if eid:
                supabase.table('education').delete().eq('id', eid).eq('user_id', uid).execute()
            return redirect(url_for('profile.edit_education'))

        school_name = request.form.get('school_name', '').strip()
        if not school_name:
            flash('School name is required.')
            return redirect(url_for('profile.edit_education', entry_id=entry_id))

        currently_attending = 'currently_attending' in request.form
        data = {
            'user_id': uid,
            'school_name': school_name,
            'education_level': request.form.get('education_level', ''),
            'currently_attending': currently_attending,
            'start_date': request.form.get('start_date') or None,
            'end_date': None if currently_attending else (request.form.get('end_date') or None),
            'area_of_study': request.form.get('area_of_study', '').strip(),
            'description': request.form.get('description', '').strip()[:250],
        }
        if action == 'update' and entry_id:
            supabase.table('education').update(data).eq('id', entry_id).eq('user_id', uid).execute()
            flash('Education updated.')
        else:
            supabase.table('education').insert(data).execute()
            flash('Education entry added.')
        return redirect(url_for('profile.edit_education'))

    entries = supabase.table('education').select('*').eq('user_id', uid).execute().data
    editing = next((e for e in entries if e['id'] == entry_id), None) if entry_id else None
    return render_template('edit_education.html', entries=entries, editing=editing)


@profile_bp.route('/profile/edit/experience', methods=['GET', 'POST'])
@profile_bp.route('/profile/edit/experience/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_experience(entry_id=None):
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'delete':
            eid = request.form.get('entry_id')
            if eid:
                supabase.table('experience').delete().eq('id', eid).eq('user_id', uid).execute()
            return redirect(url_for('profile.edit_experience'))

        employer_name = request.form.get('employer_name', '').strip()
        if not employer_name:
            flash('Employer name is required.')
            return redirect(url_for('profile.edit_experience', entry_id=entry_id))

        start_date = request.form.get('start_date') or None
        if not start_date:
            flash('Start date is required.')
            return redirect(url_for('profile.edit_experience', entry_id=entry_id))

        currently_working = 'currently_working' in request.form
        data = {
            'user_id': uid,
            'employer_name': employer_name,
            'job_title': request.form.get('job_title', '').strip(),
            'job_type': request.form.get('job_type', ''),
            'currently_working': currently_working,
            'start_date': start_date,
            'end_date': None if currently_working else (request.form.get('end_date') or None),
            'city': request.form.get('city', '').strip(),
            'state': request.form.get('state', ''),
            'description': request.form.get('description', '').strip()[:500],
        }
        if action == 'update' and entry_id:
            supabase.table('experience').update(data).eq('id', entry_id).eq('user_id', uid).execute()
            flash('Experience updated.')
        else:
            supabase.table('experience').insert(data).execute()
            flash('Experience entry added.')
        return redirect(url_for('profile.edit_experience'))

    entries = supabase.table('experience').select('*').eq('user_id', uid).execute().data
    editing = next((e for e in entries if e['id'] == entry_id), None) if entry_id else None
    return render_template('edit_experience.html', entries=entries, editing=editing, states=US_STATES)


@profile_bp.route('/profile/edit/skills', methods=['GET', 'POST'])
@login_required
def edit_skills():
    uid = session['user_id']
    if request.method == 'POST':
        selected_ids = request.form.getlist('skill_ids')[:15]
        supabase.table('user_skills').delete().eq('user_id', uid).execute()
        for sid in selected_ids:
            supabase.table('user_skills').insert({'user_id': uid, 'skill_id': int(sid)}).execute()
        flash('Skills updated.')
        return redirect(url_for('profile.view_profile'))

    all_skills = supabase.table('skills_list').select('*').order('name').execute().data
    user_skill_ids = [s['skill_id'] for s in supabase.table('user_skills').select('skill_id').eq('user_id', uid).execute().data]
    return render_template('edit_skills.html', all_skills=all_skills, user_skill_ids=user_skill_ids)


@profile_bp.route('/profile/edit/projects', methods=['GET', 'POST'])
@profile_bp.route('/profile/edit/projects/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_projects(entry_id=None):
    uid = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'delete':
            eid = request.form.get('entry_id')
            if eid:
                supabase.table('projects').delete().eq('id', eid).eq('user_id', uid).execute()
            return redirect(url_for('profile.edit_projects'))

        title = request.form.get('title', '').strip()
        if not title:
            flash('Project title is required.')
            return redirect(url_for('profile.edit_projects', entry_id=entry_id))

        currently_working = 'currently_working' in request.form
        data = {
            'user_id': uid,
            'title': title,
            'role': request.form.get('role', '').strip() or None,
            'currently_working': currently_working,
            'start_date': request.form.get('start_date') or None,
            'end_date': None if currently_working else (request.form.get('end_date') or None),
            'url': request.form.get('url', '').strip() or None,
            'description': request.form.get('description', '').strip() or None,
        }
        if action == 'update' and entry_id:
            supabase.table('projects').update(data).eq('id', entry_id).eq('user_id', uid).execute()
            flash('Project updated.')
        else:
            supabase.table('projects').insert(data).execute()
            flash('Project added.')
        return redirect(url_for('profile.edit_projects'))

    entries = supabase.table('projects').select('*').eq('user_id', uid).execute().data
    editing = next((e for e in entries if e['id'] == entry_id), None) if entry_id else None
    return render_template('edit_projects.html', entries=entries, editing=editing)


@profile_bp.route('/profile/edit/social', methods=['GET', 'POST'])
@login_required
def edit_social():
    uid = session['user_id']
    if request.method == 'POST':
        _save_social(uid, request.form)
        flash('Social links updated.')
        return redirect(url_for('profile.view_profile'))

    existing = supabase.table('social_links').select('*').eq('user_id', uid).execute().data
    social = existing[0] if existing else {}
    return render_template('edit_social.html', social=social)
