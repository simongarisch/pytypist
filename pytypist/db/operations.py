import os
from sqlalchemy.orm import sessionmaker
from pytypist.lessons import Sections
from .table_models import Db


def clear():
    Db.Base.metadata.drop_all(bind=Db.engine)
    Db.Base.metadata.create_all(bind=Db.engine)


def populate_lessons(use_testdb=False):
    Db.initialize(use_testdb)
    Session = sessionmaker(bind=Db.engine)
    session = Session()

    sections = Sections()

    session.commit()
