from pytypist import db


def test_populate_lessons():
    db.populate_lessons(use_testdb=True)
