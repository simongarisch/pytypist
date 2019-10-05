from functools import total_ordering
from collections import OrderedDict
from . singleton import Singleton
from . import util


@total_ordering
class Lesson:
    def __init__(self, file_path):
        self.file_path = file_path
        section, name, number, content = util.validate_lesson(
            file_path
        )
        self.section = section
        self.name = name
        self.number = number
        self.content = content

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Lesson({})".format(self.file_path)

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number


class Lessons(metaclass=Singleton):
    def __init__(self):
        self.lessons = self.sections = None
        self.get_sections()

    def get_sections(self):
        lessons = self.lessons = sorted(
            [Lesson(f) for f in util.list_lesson_files()]
        )
        sections = OrderedDict()
        for lesson in lessons:
            section = lesson.section
            if section not in sections:
                sections[section] = OrderedDict()
            sections[section][str(lesson)] = lesson
        self.sections = sections

    def get_lesson_content(self, lesson_name):
        for lesson in self.lessons:
            if str(lesson) == lesson_name:
                return lesson.content
        raise util.LessonNotFound(
            "Unable to find lesson '{}'".format(lesson_name)
        )


class Sections:
    @classmethod
    def __init__(class):
        cls._section_folders = util.get_section_folder_paths()
