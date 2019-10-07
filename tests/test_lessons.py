import os
import pytest
from pytypist.lessons import Lesson, Section, Sections, util
from pytypist.lessons.lessons import (
    collect_lesson,
    validate_lesson,
    LessonValidationFailed,
)


class TestLessons:

    def test_is_singleton(self):
        sections1 = Sections()
        sections2 = Sections()
        assert sections1 is sections2

    def test_list_folder_paths(self):
        folder_paths = util.list_folder_paths()
        assert len(folder_paths) > 0
        for folder_path in folder_paths:
            assert os.path.isdir(folder_path)

    def test_list_files(self):
        for folder_path in util.list_folder_paths():
            files = util.list_files(
                folder_path, endswith="ini"
            )
            assert isinstance(files, list)
            assert len(files) > 0
            for file_name in files:
                assert file_name.endswith("ini")

    def test_collect_lesson(self):
        with pytest.raises(TypeError):
            collect_lesson(None)
        with pytest.raises(ValueError):
            collect_lesson("some_lesson.csv")

    def test_validate_lesson_extra_sections(self):
        with pytest.raises(LessonValidationFailed):
            validate_lesson("lesson_extra_sections.ini")

    def test_validate_lesson_missing_number(self):
        with pytest.raises(LessonValidationFailed):
            validate_lesson("lesson_missing_number.ini")

    def test_validate_lesson_missing_content(self):
        with pytest.raises(LessonValidationFailed):
            validate_lesson("lesson_missing_content.ini")

    def test_lesson_list_names(self):
        names_list = Lesson.list_names()
        assert isinstance(names_list, list)
        assert len(names_list) > 0

    def test_get_lesson_by_name(self):
        names_list = Lesson.list_names()
        lesson_name = names_list[0]
        lesson1 = Lesson.get_lesson_by_name(lesson_name)
        lesson2 = Lesson.get_lesson_by_name(lesson_name)
        assert lesson1 is lesson2
        assert isinstance(lesson1, Lesson)

    def test_lesson_str(self):
        names_list = Lesson.list_names()
        lesson = Lesson.get_lesson_by_name(names_list[0])
        assert str(lesson) == "Keys 'asdf'"

    def test_lesson_ordering(self):
        names_list = Lesson.list_names()
        lesson_name1 = names_list[0]
        lesson_name2 = names_list[1]
        lesson1 = Lesson.get_lesson_by_name(lesson_name1)
        lesson2 = Lesson.get_lesson_by_name(lesson_name2)
        assert lesson1 == lesson1
        assert lesson1 != lesson2
        assert lesson1 < lesson2
