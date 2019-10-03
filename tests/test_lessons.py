from pytypist.lessons import Lessons, util


class TestLessons:
    def test_is_singleton(self):
        lessons1 = Lessons()
        lessons2 = Lessons()
        assert lessons1 is lessons2

    def test_list_files(self):
        files = util.list_lesson_files()
        assert isinstance(files, list)
        assert len(files) > 0
