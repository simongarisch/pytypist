import os
import pytest
from pytypist.lessons import Sections, util
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

    def test_validate_lesson(self):
        with pytest.raises(LessonValidationFailed):
            validate_lesson("lesson_extra_sections.ini")
        with pytest.raises(LessonValidationFailed):
            validate_lesson("lesson_missing_number.ini")
