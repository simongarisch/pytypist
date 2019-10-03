import os
from configparser import ConfigParser


class LessonError(Exception):
    """ Base exception for this module. """


class LessonValidationFailed(LessonError):
    """ Lesson failed validation. """


class LessonNotFound(LessonError):
    """ Unable to find lesson. """


def list_lesson_files():
    """ List all of the lesson files. """
    dire_path = os.path.dirname(os.path.realpath(__file__))
    lesson_files = []
    for item in os.listdir(dire_path):
        full_path = os.path.join(dire_path, item)
        if os.path.isdir(full_path) and not item.startswith("__"):
            subfolder_items = os.listdir(full_path)
            for subitem in subfolder_items:
                if subitem.endswith(".ini"):
                    subpath = os.path.join(full_path, subitem)
                    lesson_files.append(subpath)
    return lesson_files


def clean_lesson_content(content):
    """ Remove items such as new lines and multiple spaces. """
    content = content.replace("\n", " ")
    while "  " in content:
        content = content.replace("  ", " ")
    return content.strip()


def validate_lesson(file_name):
    """ All of the lesson files should obey a consistent format. """
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
        raise LessonValidationFailed(
            """Each lesson requires details for 'section',
                'name', 'number' and 'content'."""
        )
    content = clean_lesson_content(content)
    return section, name, number, content


def collect_lesson(file_path):
    """ Collects and returns data in the lesson .ini file. """
    if not isinstance(file_path, str):
        raise TypeError("file_path should be of the type str.")
    if not file_path.endswith("ini"):
        raise ValueError("lesson files should be in .ini format.")
    config = ConfigParser()
    config.read(file_path)
    return config
