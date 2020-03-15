import os
import json
from sqlalchemy import *
from sqlalchemy.orm import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

from common import *
from database import *
from models import *

app = Flask(__name__)

def create_or_update_post(post_uid=None):
    title = request.form['title']
    body = request.form['body']
    tags = request.form['tags']
    if len(tags) > 0:
        tags = json.loads(tags)
        tagnames = [ tag['value'] for tag in tags ]
    else:
        tagnames = []

    updater = PostUpdater()
    if post_uid is None:
        session, post = updater.create(title=title, body=body, tagnames=tagnames)
    else:
        session, post = updater.update(post_uid=post_uid, title=title, body=body, tagnames=tagnames)

    session.commit()

    return post


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/post/new', methods=[ 'GET', 'POST', ])
def admin_post_new():
    if request.method == 'POST':
        post = create_or_update_post()

        return redirect(url_for('admin_post_edit', post_uid=post.uid))
    else:
        post = None

    return render_template('admin/post.html')

@app.route('/admin/post/<post_uid>', methods=[ 'GET', 'POST', ])
def admin_post_edit(post_uid):
    if request.method == 'POST':
        post = create_or_update_post(post_uid=post_uid)
    else:
        session = Session()
        post = session.query(Post).filter(Post.uid == post_uid).first()
        if post is None:
            return redirect(url_for('admin_post_new'))

    return render_template('admin/post.html', post=post)

@app.route('/admin/post/update', methods=[ 'POST', ])
def admin_post_update():
    post_uid = request.form.get('post_uid')
    post = create_or_update_post(post_uid=post_uid)

    return jsonify({
        'post_uid': post.uid,
    })

@app.route('/admin/post/preview/<post_uid>', methods=[ 'GET', ])
def admin_preview(post_uid):
    session = Session()
    post = session.query(Post).filter(Post.uid == post_uid).first()

    return render_template('admin/preview.html', post=post)

if __name__ == '__main__':
    BaseModel.metadata.create_all(ENGINE)

    app.debug = DEBUG
    app.run(host='0.0.0.0')
