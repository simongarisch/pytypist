import os
from configparser import ConfigParser


class LessonError(Exception):
    """ Base exception for this module. """


class LessonValidationFailed(LessonError):
    """ Lesson failed validation. """


class LessonNotFound(LessonError):
    """ Unable to find lesson. """


class SlidesNotFound(LessonError):
    """ Unable to find slides. """


def get_section_folder_paths():
    """ Collect the folder paths for all sections. """
    section_folder_paths = []
    dire_path = os.path.dirname(os.path.realpath(__file__))
    for item in os.listdir(dire_path):
        full_path = os.path.join(dire_path, item)
        if os.path.isdir(full_path) and not item.startswith("__"):
            section_folder_paths.append(full_path)
    return section_folder_paths


def list_lesson_files():
    """ Returns a list of all the lesson files. """
    lesson_files = []
    for section_path in get_section_folder_paths():
        folder_items = os.listdir(section_path)
        for item in folder_items:
            if item.endswith(".ini"):
                lesson_path = os.path.join(section_path, item)
                lesson_files.append(lesson_path)
    return lesson_files


def collect_slides():
    slide_paths = dict()
    for section_path in get_section_folder_paths():
        section = None
        slides_path = None


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
