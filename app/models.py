import os
import json
from datetime import datetime as dt

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from common import *
from database import *

BaseModel = declarative_base()

class Post(BaseModel):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Text) # unique id
    title = Column(Text)
    body = Column(Text)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow)

    tags = relationship('Tag', secondary='posttagrelations', back_populates='posts')

    def tags_json(self):
        return json.dumps([ tag.name for tag in self.tags ], ensure_ascii=False)

class Tag(BaseModel):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow)

    posts = relationship('Post', secondary='posttagrelations', back_populates='tags')

class PostTagRelation(BaseModel):
    __tablename__ = 'posttagrelations'

    id = Column(Integer, primary_key=True, autoincrement=True)

    post_id = Column(Integer, ForeignKey('posts.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))

    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow)

class PostUpdater:
    def __init__(self):
        pass

    def _set_tags(self, session, post, tagnames):
        tags = []
        for tagname in tagnames:
            tag = session.query(Tag).filter(Tag.name == tagname).first()
            if tag is None:
                tag = Tag(name=tagname)
                session.add(tag)
            tags.append(tag)

        post.tags = tags

    def create(self, title, body, tagnames):
        session = Session()

        post_uid = generate_unique_id()
        post = Post()

        post.uid = post_uid
        post.title = title
        post.body = body

        self._set_tags(session, post, tagnames)

        session.add(post)
        return session, post

    def update(self, post_uid, title, body, tagnames):
        session = Session()

        post = session.query(Post).filter(Post.uid == post_uid).first()

        post.uid = post_uid
        post.title = title
        post.body = body

        self._set_tags(session, post, tagnames)

        session.add(post)
        return session, post
