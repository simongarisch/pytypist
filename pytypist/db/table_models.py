from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    NVARCHAR,
    DateTime,
)
from .db_settings import config


class Db:
    engine = None
    Base = declarative_base()

    @classmethod
    def initialize(cls, use_testdb=False):
        test_or_prod = "test" if use_testdb else "prod"
        engine_desc = config.get("engines", test_or_prod)
        cls.engine = create_engine(engine_desc)
        cls.Base.metadata.create_all(cls.engine)


class Lessons(Db.Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    section = Column(String)
    name = Column(String, unique=True, nullable=False)


class LessonsStats(Db.Base):
    __tablename__ = "lessons_completed"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    seconds_elapsed = Column(Integer, nullable=False)
    wpm = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)


class TypingErrors(Db.Base):
    __tablename__ = "typing_errors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    letter = Column(NVARCHAR(1), nullable=False)
    word = Column(String, nullable=False)
    CheckConstraint(
        "len(letter) == 1",
        name="Incorrect letter must be one char only"
    )
