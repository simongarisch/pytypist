from functools import total_ordering
from . import util


@total_ordering
class Lesson:
    def __init__(self, file_name):
        self.file_name = file_name
        section, name, number, content = util.validate_lesson(
            file_name
        )
        self.name = name
        self.number = number

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Lesson({})".format(self.file_name)

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number


def get_lessons():
    return sorted([Lesson(f) for f in util.list_files()])
