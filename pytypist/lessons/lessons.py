import functools
from collections import OrderedDict
from weakref import WeakValueDictionary
from configparser import ConfigParser
from . import util


class LessonError(Exception):
    """ Base exception for this module. """


class LessonValidationFailed(LessonError):
    """ Lesson failed validation. """


class LessonNotFound(LessonError):
    """ Unable to find lesson. """


class LessonNameNotUnique(LessonError):
    """ Every lesson should have a unique name. """


def collect_lesson(file_path):
    """ Collects and returns data in the lesson .ini file. """
    if not isinstance(file_path, str):
        raise TypeError("file_path should be of the type str.")
    if not file_path.endswith("ini"):
        raise ValueError("lesson files should be in .ini format.")
    config = ConfigParser()
    config.read(file_path)
    return config


def clean_lesson_content(content):
    """ Remove items such as new lines and multiple spaces. """
    content = content.replace("\n", " ")
    while "  " in content:
        content = content.replace("  ", " ")
    return content.strip()


def validate_lesson(file_name):
    """ All lesson files should obey a consistent format. """
    lesson = collect_lesson(file_name)
    if lesson.sections() != ["details"]:
        raise LessonValidationFailed(
            "There should only be one 'details' section."
        )

    section = lesson.get("details", "section", fallback=None)
    name = lesson.get("details", "name", fallback=None)
    number = lesson.getfloat("details", "number", fallback=None)
    content = lesson.get("details", "content", fallback=None)

    if None in [section, name, number, content]:
        message = """
            Each lesson requires details for 'section',
            'name', 'number' and 'content'.
        """
        raise LessonValidationFailed(message)
    content = clean_lesson_content(content)
    return section, name, number, content


@functools.total_ordering
class Lesson:
    _names = WeakValueDictionary()

    @classmethod
    def register(cls, lesson):
        name = lesson.name
        if name in cls._names:
            raise LessonNameNotUnique("%s" % name)
        cls._names[name] = lesson

    @classmethod
    def get_lesson_by_name(cls, name):
        lesson = cls._names.get(name)
        if lesson is None:
            raise LessonNotFound(name)
        return lesson

    @classmethod
    def list_names(cls):
        """ Returns a list of all lesson names. """
        return list(cls._names)

    def __init__(self, file_path):
        self.file_path = file_path
        section, name, number, content = validate_lesson(
            file_path
        )
        self.section = section
        self.name = name
        self.number = number
        self.content = content
        Lesson.register(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Lesson({})".format(self.file_path)

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number


class Lessons(OrderedDict):
    def __init__(self, section_folder):
        super().__init__()
        self._section_folder = section_folder
        self._collect_lessons()
        self._check_section_names_identical()

    @property
    def section(self):
        return self._section

    def _collect_lessons(self):
        # get a list of all the lesson files (ending with .ini)
        lesson_files = util.list_files(
            self._section_folder, endswith=".ini"
        )

        # convert these files to lesson objects
        lessons = self.lessons = sorted([
            Lesson(file_path) for file_path in lesson_files
        ])

        for lesson in lessons:
            self[lesson.name] = lesson

    def _check_section_names_identical(self):
        """ All lessons in the same folder should have the
            same section name.
        """
        section_names = [lesson.section for lesson in self.lessons]
        if len(set(section_names)) != 1:
            raise LessonValidationFailed(
                "Grouped Lessons should have identical section names."
            )
        self._section = section_names[0]
