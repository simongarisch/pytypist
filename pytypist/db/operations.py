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


def populate_lessons_stats(stats, use_testdb=False, ):
    Db.initialize(use_testdb)
    Session = sessionmaker(bind=Db.engine)
    session = Session()

    db_lessons = session.query(table_models.Lessons).all()
    ids_dict = {lesson.name: lesson.id for lesson in db_lessons}

    lesson_id = ids_dict[stats.lesson_name]
    date_time = stats.date_time
    seconds_elapsed = stats.seconds_elapsed
    wpm = stats.wpm
    accuracy = stats.accuracy

    entry = table_models.LessonsStats(
        lesson_id=lesson_id,
        date_time=stats.date_time,
        seconds_elapsed=stats.seconds_elapsed,
        wpm=stats.wpm,
        accuracy=stats.accuracy,
    )
    session.add(entry)

    session.commit()
