import os
from sqlalchemy import *
from sqlalchemy.orm import *
from flask import Flask, render_template, request, redirect, url_for
from common import *
from database import *
from models import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/post/new', methods=[ 'GET', 'POST' ])
def admin_post_new():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tagnames = request.form['tags']

        updater = PostUpdater()
        session, post = updater.create(title="title", body="body", tagnames=[ "a", "b", "c" ])
        session.commit()

        return redirect(url_for('admin_post_edit', post_uid=post.uid))

    else:
        post = None

    return render_template('admin/post.html')

@app.route('/admin/post/<post_uid>', methods=[ 'GET', 'POST' ])
def admin_post_edit(post_uid):
    session = Session()
    post = session.query(Post).filter(Post.uid == post_uid).first()

    return render_template('admin/post.html', post=post)


if __name__ == '__main__':
    BaseModel.metadata.create_all(ENGINE)

    app.debug = DEBUG
    app.run(host='0.0.0.0')
