import os
import json
from datetime import datetime as dt
from sqlalchemy import *
from sqlalchemy.orm import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

from settings import *
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    recent_entries = Entry.query.filter(Entry.status == EntryStatus.PUBLISHED).order_by(Entry.posted_at.desc()).limit(10)

    return render_template('index.html', recent_entries=recent_entries)

@app.route('/entry/<entry_uid>')
def entry(entry_uid):
    entry = Entry.query.filter(and_(Entry.uid == entry_uid, Entry.status == EntryStatus.PUBLISHED)).first()
    if entry is None:
        return render_template('404.html'), 404

    return render_template('entry.html', entry=entry)

@app.route('/admin/entry/new')
def admin_entry_new():
    entry = Entry.create_new_draft()

    session = Session()
    session.add(entry)
    session.commit()

    return redirect(url_for('admin_entry_edit', entry_uid=entry.uid))

@app.route('/admin/entry/<entry_uid>', methods=[ 'GET', 'POST', ])
def admin_entry_edit(entry_uid):
    if request.method == 'POST':
        entry = Entry.query.filter(Entry.uid == entry_uid).first()
        assert entry is not None

        entry.title = request.form['title']
        entry.body = request.form['body']
        entry.set_tags(request.form['tags'])

        status = int(request.form['status'])
        assert status in [ EntryStatus.DRAFT, EntryStatus.PUBLISHED ]

        entry.status = status

        if status == EntryStatus.PUBLISHED:
            if entry.posted_at is None:
                entry.posted_at = dt.now()
            entry.modified_at = dt.now()

        session = Session()
        session.add(entry)
        session.commit()
    else:
        entry = Entry.query.filter(Entry.uid == entry_uid).first()
        if entry is None:
            return redirect(url_for('admin_entry_new'))


    return render_template('admin/edit.html', entry=entry)

@app.route('/admin/entry/update', methods=[ 'POST', ])
def admin_entry_update():
    entry_uid = request.form.get('entry_uid')
    # FIXME:
    entry = create_or_update_post(entry_uid=entry_uid)

    return jsonify({
        'entry_uid': entry.uid,
    })

@app.route('/admin/entry/preview/<entry_uid>', methods=[ 'GET', ])
def admin_preview(entry_uid):
    entry = Entry.query.filter(Entry.uid == entry_uid).first()

    return render_template('admin/preview.html', entry=entry)

if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')
