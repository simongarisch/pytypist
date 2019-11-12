import os
from sqlalchemy.orm import sessionmaker
from pytypist.lessons import Sections
from . import table_models
from .table_models import Db


def clear():
    Db.Base.metadata.drop_all(bind=Db.engine)
    Db.Base.metadata.create_all(bind=Db.engine)


def populate_lessons(use_testdb=False):
    Db.initialize(use_testdb)
    Session = sessionmaker(bind=Db.engine)
    session = Session()

    db_lessons = session.query(table_models.Lessons).all()
    db_lesson_names = [lesson.name for lesson in db_lessons]

    sections = Sections()
    for section in sections.values():
        for lesson in section.lessons:
            lesson_name = lesson.name
            if lesson_name in db_lesson_names:
                # lesson has already been loaded
                continue
            entry = table_models.Lessons(
                section=lesson.section,
                name=lesson_name
            )
            session.add(entry)

    session.commit()
