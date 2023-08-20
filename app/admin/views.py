from flask import render_template, redirect, url_for, flash, request, \
    current_app, make_response
from .. import db
from . import admin
from ..models import Permission, User, Post, Comment, Notification, Like, Activity, Recruitment, Certification, Rank


@admin.route('/display/<file>', methods=['GET', 'POST'])
def display_certification(file):
    return render_template('admin/certification_display.html', file=file)


@admin.route('/permit/<teacher_id>', methods=['GET', 'POST'])
def permit_certification(teacher_id):
    professor = User.query.filter_by(college_id=teacher_id).first()
    professor.certification = 1
    certification = Certification.query.filter_by(teacher_id=teacher_id).first()
    certification.validated = True
    db.session.commit()
    return redirect(url_for('main.index_certification'))


@admin.route('/reject/<teacher_id>', methods=['GET', 'POST'])
def reject_certification(teacher_id):
    professor = User.query.filter_by(college_id=teacher_id).first()
    professor.certification = 1
    certification = Certification.query.filter_by(teacher_id=teacher_id).first()
    certification.validated = False
    db.session.commit()
    return redirect(url_for('main.index_certification'))


@admin.route('/delete/<name>', methods=['GET', 'POST'])
def delete_rank(name):
    university = Rank.query.filter_by(name=name).first()
    db.session.delete(university)
    db.session.commit()
    return redirect(url_for('main.index_rank'))
