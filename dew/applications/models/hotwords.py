# -*- coding: utf-8 -*-

from base import db
from base import BaseModel, TimestampMixin



class HotWords(BaseModel, TimestampMixin):

    __tablename__           = 'hot_words'

    word                    = db.Column(db.VARCHAR(255))

    def __init__(self, **kwargs):

        self.word = kwargs.pop('word', None)
