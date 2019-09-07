import os
from configparser import ConfigParser


class LessonError(Exception):
    """ Base exception for this module. """


class LessonValidationFailed(LessonError):
    """ Lesson failed validation. """


class LessonNotFound(LessonError):
    """ Unable to find lesson. """


def list_files():
    """ List all of the lesson files. """
    dire_path = os.path.dirname(os.path.realpath(__file__))
    return [f for f in os.listdir(dire_path) if f.endswith(".ini")]


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
    number = lesson.getint("details", "number", fallback=None)

    content = lesson.get("details", "content", fallback=None)
    if None in [section, name, number, content]:
        raise LessonValidationFailed(
            """Each lesson requires details for 'section',
                'name', 'number' and 'content'."""
        )
    content = clean_lesson_content(content)
    return section, name, number, content


def collect_lesson(file_name):
    """ Collects and returns data in the lesson .ini file. """
    if not isinstance(file_name, str):
        raise TypeError("file_name should be of the type str.")
    if not file_name.endswith("ini"):
        raise ValueError("lesson files should be in .ini format.")
    config = ConfigParser()
    config.read(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            file_name
        )
    )
    return config


def main():
    files = list_files()
    for file_name in files:
        print(validate_lesson(file_name))


if __name__ == "__main__":
    main()
