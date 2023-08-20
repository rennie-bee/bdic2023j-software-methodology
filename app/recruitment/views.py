from flask import render_template, redirect, request, url_for, flash, send_from_directory, make_response, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from . import recruitment
from ..models import Resume, Recruitment, Certification
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import random
from pyecharts import options as opts
from pyecharts.charts import Pie


@recruitment.route('/mresumes', methods=['GET', 'POST'])
def my_resumes():
    resumes = current_user.resumes
    return render_template('recruitment/mresume.html', resumes=resumes, panel_id=1)


@recruitment.route('/mresumes_pass', methods=['GET', 'POST'])
def my_resumes_pass():
    resumes = current_user.resumes
    _resumes = [resume for resume in resumes if resume.status == 1]
    return render_template('recruitment/mresume.html', resumes=_resumes, panel_id=2)


@recruitment.route('/mresumes_inprogress', methods=['GET', 'POST'])
def my_resumes_inprogress():
    resumes = current_user.resumes
    _resumes = [resume for resume in resumes if resume.status == 0]
    return render_template('recruitment/mresume.html', resumes=_resumes, panel_id=3)


@recruitment.route('/mresumes_dismiss', methods=['GET', 'POST'])
def my_resumes_dismiss():
    resumes = current_user.resumes
    _resumes = [resume for resume in resumes if resume.status == 2]
    return render_template('recruitment/mresume.html', resumes=_resumes, panel_id=4)


@recruitment.route('/download/<filename>', methods=['GET', 'POST'])
def download_my_resume(filename):
    if request.method == 'GET':
        filepath = os.path.join(current_app.root_path, 'static/resumes')
        return send_from_directory(filepath, filename, as_attachment=True)


@recruitment.route('/new_transaction', methods=['GET', 'POST'])
def new_transaction():
    if request.method == 'GET':
        certification = Certification.query.filter_by(teacher_id=current_user.college_id).first()
        valid = certification.validated
        if valid:
            return render_template('recruitment/new_recruitment.html')
        else:
            flash('You need to validate your certification first')
            return redirect(url_for('main.index'))
    if request.method == 'POST':
        title = request.form["recruit_title"]
        describe = request.form["recruit_describe"]
        detail = request.files["recruit_detail"]
        if title == "" or describe == "" or not detail:
            flash("Recruiting information should be whole")
            return render_template('recruitment/new_recruitment.html')

        current_time = datetime.now().strftime("%H%M%S%Y%m%d")
        underling = random.randint(11, 99)
        filename = secure_filename(detail.filename)
        strong_filename = str(current_time) + str(underling) + filename
        detail.save(os.path.join('app', 'static', 'recruits', strong_filename))
        recruits = Recruitment(title=title,
                               description=describe,
                               filename=strong_filename,
                               detail_path="../static/recruit/" + strong_filename,
                               professor=current_user)
        db.session.add(recruits)
        db.session.commit()
        flash('Your recruitment has been posted!')
        return redirect(url_for('main.index_recruitment'))


@recruitment.route('/recruitment/<int:id>', methods=['GET', 'POST'])
def recruitments(id):
    recruit = Recruitment.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (recruit.resumes.count('*') - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Resume.query.with_parent(recruit).order_by(Resume.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    resumes = pagination.items
    if request.method == 'POST':
        body = request.form["resume_body"]
        file = request.files["resume_detail"]
        if body == "" or not file:
            flash("Please enter all the information")
        else:
            current_time = datetime.now().strftime("%H%M%S%Y%m%d")
            underling = random.randint(11, 99)
            filename = secure_filename(file.filename)
            strong_filename = str(current_time) + str(underling) + filename
            file.save(os.path.join('app', 'static', 'resumes', strong_filename))
            resume = Resume(message=body,
                            recruitment=recruit,
                            resume_name=strong_filename,
                            student=current_user._get_current_object(),
                            status=0)
            resume.recruitment.recent_activity = datetime.utcnow()
            db.session.add(resume)
            db.session.commit()
            flash('Resume submitted successfully')
            return redirect(url_for('.recruitments', id=recruit.id))
    # return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)
    return render_template('recruitment.html', recruitment=recruit, resumes=resumes, pagination=pagination)


@recruitment.route('/recruitment_download/<filename>')
def download_recruitment(filename):
    directory = os.path.join(current_app.root_path, 'static/recruits')
    if os.path.isfile(os.path.join(directory, filename)):
        print(directory)
        return send_from_directory(directory, filename, as_attachment=True)


@recruitment.route('/resume_download/<filename>')
def download_resume(filename):
    directory = os.path.join(current_app.root_path, 'static/resumes')
    if os.path.isfile(os.path.join(directory, filename)):
        print(directory)
        return send_from_directory(directory, filename, as_attachment=True)


@recruitment.route('/resume_delete/<int:resume_id>')
@login_required
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if current_user == resume.student:
        db.session.delete(resume)
        db.session.commit()
        flash('Your resume submission has been deleted.')
    else:
        flash("You cannot delete other's resumes")
    return redirect(url_for('.recruitments', id=resume.recruitment_id))


@recruitment.route('/resume_update/<int:resume_id>/<int:status>')
@login_required
def update_resume(resume_id, status):
    resume = Resume.query.get_or_404(resume_id)
    if current_user == resume.recruitment.professor:
        resume.status = status
        db.session.commit()
        if status == 1:
            flash('This resume has been approved')
        else:
            flash('This resume has been rejected')
    else:
        flash("You cannot examine other's resumes")
    return redirect(url_for('.recruitments', id=resume.recruitment_id))


def pie_base() -> Pie:
    c = (
        Pie()
        .add("",[list(z) for z in zip(["All Resumes", "In Progress", "Pass", "Dismiss"],
                                      [Resume.query.count(),
                                       Resume.query.filter_by(status=0).count(),
                                       Resume.query.filter_by(status=1).count(),
                                       Resume.query.filter_by(status=2).count()])])
        .set_global_opts(title_opts=opts.TitleOpts(title="Statistic Pie", subtitle="Resume"))
    )
    return c


@recruitment.route("/resumeChart")
@login_required
def get_pie_chart():
    c = pie_base()
    return c.dump_options_with_quotes()
