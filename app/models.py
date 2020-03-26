import os
import json
from datetime import datetime as dt
from sqlalchemy import *
from sqlalchemy.orm import *

import markdown

from settings import BaseModel, Session

def generate_unique_id(length=14):
    return os.urandom(length).hex()


class PostStatus:
    UNSAVED_DRAFT = 0
    DRAFT = 1
    PUBLISHED = 2

class Post(BaseModel):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Text) # unique id
    title = Column(Text)
    body = Column(Text)
    status = Column(Integer, default=PostStatus.UNSAVED_DRAFT)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow)
    posted_at = Column(DateTime)
    modified_at = Column(DateTime)

    tags = relationship('Tag', secondary='posttagrelations', back_populates='posts')

    @staticmethod
    def create_new_draft():
        post_uid = generate_unique_id()
        post = Post()
        post.uid = post_uid

        return post

    def set_tags(self, tagify_string):
        tagify_tags = json.loads(tagify_string)

        tags = []
        for tagify_tag in tagify_tags:
            name = tagify_tag['value']
            tag = Tag.query.filter(Tag.name == name).first()
            if tag is None:
                tag = Tag(name=name)
            tags.append(tag)

        self.tags = tags

    def tags_json(self):
        return json.dumps([ tag.name for tag in self.tags ], ensure_ascii=False)

    def body_html(self):
        if self.body is None:
            return ''

        extensions = []
        extensions += [ 'fenced_code', ] # https://python-markdown.github.io/extensions/fenced_code_blocks/
        extensions += [ 'tables', ] # https://python-markdown.github.io/extensions/tables/
        extensions += [ 'footnotes', ] # https://python-markdown.github.io/extensions/footnotes/

        body = self.body

        # Escape for MathJax
        body = body.replace('\\[', '\\\\[').replace('\\]', '\\\\]').replace('\\(', '\\\\(').replace('\\)', '\\\\)')
        body = markdown.markdown(body, extensions=extensions)

        return body


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
