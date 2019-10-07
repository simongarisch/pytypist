import os
import pytest
from pytypist.lessons import Lesson, util

from pytypist.lessons.lessons import (
    collect_lesson,
    validate_lesson,
    LessonValidationFailed,
    LessonNotFound,
    LessonNameNotUnique,
)

from pytypist.lessons.sections import (
    Section,
    Sections,
    SectionNotFound,
    SectionNameNotUnique,
    SlidesNotFound
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
        with pytest.raises(LessonNotFound):
            Lesson.get_lesson_by_name("zzz.ini")

    def test_lesson_name_not_unique(self):
        lesson_name = Lesson.list_names()[0]
        lesson = Lesson.get_lesson_by_name(lesson_name)
        with pytest.raises(LessonNameNotUnique):
            Lesson.register(lesson)

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
        assert isinstance(lesson1, Lesson)
        assert isinstance(lesson2, Lesson)
        assert lesson1 == lesson1
        assert lesson1 != lesson2
        assert lesson1 < lesson2

    def test_get_section_by_name(self):
        names_list = Section.list_names()
        section_name = names_list[0]
        section = Section.get_section_by_name(section_name)
        assert isinstance(section, Section)
        with pytest.raises(SectionNotFound):
            Section.get_section_by_name("zzz")

    def test_section_name_not_unique(self):
        section_name = Section.list_names()[0]
        section = Section.get_section_by_name(section_name)
        with pytest.raises(SectionNameNotUnique):
            Section.register(section)

    def test_collect_slides(self):
        section_name = Section.list_names()[0]
        section = Section.get_section_by_name(section_name)
        slides = section.collect_slides()
        assert os.path.isfile(slides)
        assert slides.endswith(".html")

        with pytest.raises(SlidesNotFound):
            section._section_folder = "zzz"
            section.collect_slides()
