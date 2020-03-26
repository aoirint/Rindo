import os
import json
from datetime import datetime as dt
from sqlalchemy import *
from sqlalchemy.orm import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

from settings import *
from models import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post/<post_uid>')
def post(post_uid):
    post = Post.query.filter(and_(Post.uid == post_uid, Post.status == PostStatus.PUBLISHED)).first()
    if post is None:
        return render_template('404.html'), 404

    return render_template('post.html', post=post)

@app.route('/admin/post/new')
def admin_post_new():
    post = Post.create_new_draft()

    session = Session()
    session.add(post)
    session.commit()

    return redirect(url_for('admin_post_edit', post_uid=post.uid))

@app.route('/admin/post/<post_uid>', methods=[ 'GET', 'POST', ])
def admin_post_edit(post_uid):
    if request.method == 'POST':
        post = Post.query.filter(Post.uid == post_uid).first()
        if post is None:
            post = Post.create_new_draft()

        post.title = request.form['title']
        post.body = request.form['body']
        post.set_tags(request.form['tags'])

        status = int(request.form['status'])
        assert status in [ PostStatus.DRAFT, PostStatus.PUBLISHED ]

        post.status = status

        if status == PostStatus.PUBLISHED:
            if post.posted_at is None:
                post.posted_at = dt.now()
            post.modified_at = dt.now()

        session = Session()
        session.add(post)
        session.commit()
    else:
        post = Post.query.filter(Post.uid == post_uid).first()

    return render_template('admin/edit.html', post=post)

@app.route('/admin/post/update', methods=[ 'POST', ])
def admin_post_update():
    post_uid = request.form.get('post_uid')
    post = create_or_update_post(post_uid=post_uid)

    return jsonify({
        'post_uid': post.uid,
    })

@app.route('/admin/post/preview/<post_uid>', methods=[ 'GET', ])
def admin_preview(post_uid):
    post = Post.query.filter(Post.uid == post_uid).first()

    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')
