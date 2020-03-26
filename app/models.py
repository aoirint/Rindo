import os
import json
from datetime import datetime as dt
from sqlalchemy import *
from sqlalchemy.orm import *

import markdown

from settings import BaseModel, Session

def generate_unique_id(length=14):
    return os.urandom(length).hex()


class EntryStatus:
    UNSAVED_DRAFT = 0
    DRAFT = 1
    PUBLISHED = 2

class Entry(BaseModel):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Text) # unique id
    title = Column(Text)
    body = Column(Text)
    status = Column(Integer, default=EntryStatus.UNSAVED_DRAFT)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow)
    posted_at = Column(DateTime)
    modified_at = Column(DateTime)

    tags = relationship('Tag', secondary='entrytagrelations', back_populates='entries')

    @staticmethod
    def create_new_draft():
        entry_uid = generate_unique_id()
        entry = Entry()
        entry.uid = entry_uid

        return entry

    def set_tags(self, tagify_string):
        if len(tagify_string) > 0:
            tagify_tags = json.loads(tagify_string)
        else:
            tagify_tags = []

        tags = []
        for tagify_tag in tagify_tags:
            name = tagify_tag['value']
            tag = Tag.query.filter(Tag.name == name).first()
            if tag is None:
                tag = Tag(name=name)
            tags.append(tag)

        self.tags = tags

    def is_draft(self):
        return self.status in [ EntryStatus.UNSAVED_DRAFT, EntryStatus.DRAFT ]

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

    entries = relationship('Entry', secondary='entrytagrelations', back_populates='tags')

class EntryTagRelation(BaseModel):
    __tablename__ = 'entrytagrelations'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entry_id = Column(Integer, ForeignKey('entries.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))

    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow)
