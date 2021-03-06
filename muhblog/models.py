import re
from datetime import datetime
from typing import Optional

from flask import Markup
from slugify import slugify
from peewee import TextField, DateTimeField, ForeignKeyField, CharField
from markdown_metadata import parse_metadata

from . import markdown
from .database import BaseModel

SLUG_LENGTH = 100
STUB_LENGTH = 600
DATE_FORMAT = '%Y-%m-%d %H:%M'


class MarkdownModel(BaseModel):
    text = TextField()

    def render_markdown(self) -> Markup:
        return markdown.render(self.text)


class Entry(MarkdownModel):
    slug = CharField(unique=True, max_length=SLUG_LENGTH)
    title = CharField()
    date = DateTimeField()

    @classmethod
    def create(cls, text: str) -> 'Entry':
        metadata, text = parse_metadata(text)

        instance = cls(
            slug=slugify(
                metadata['title'][0],
                max_length=SLUG_LENGTH
            ),
            title=metadata['title'][0],
            date=datetime.strptime(metadata['date'][0], DATE_FORMAT),
            text=text
        )
        instance.save()
        for tag in metadata['tags']:
            EntryTag.create(entry=instance, name=tag)

        return instance

    def render_stub(self) -> str:
        match = re.search(rf'^(.{{1,{STUB_LENGTH}}}[\.\!\?])', self.text)
        if match is None:
            return ''
        return markdown.render(match.group(1))

    def next_entry(self) -> Optional['Entry']:
        try:
            return self.__class__ \
                .get_by_id(self.id + 1)
        except self.__class__.DoesNotExist:
            return None

    def previous_entry(self) -> Optional['Entry']:
        try:
            return self.__class__ \
                .get_by_id(self.id - 1)
        except self.__class__.DoesNotExist:
            return None


class AboutPage(MarkdownModel):
    pass


class Tag(BaseModel):
    slug = CharField(unique=True, max_length=SLUG_LENGTH)
    name = TextField()

    @classmethod
    def create(cls, name: str) -> 'Tag':
        return super().create(
            name=name,
            slug=slugify(name, max_length=SLUG_LENGTH)
        )


class EntryTag(BaseModel):
    definition = ForeignKeyField(Tag, backref='entries')
    entry = ForeignKeyField(Entry, backref='tags')

    @classmethod
    def create(cls, entry: Entry, name: str) -> 'EntryTag':
        return super().create(
            entry=entry,
            definition=Tag.get_or_create(name=name)[0]
        )
