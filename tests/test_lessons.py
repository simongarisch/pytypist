from pytypist.lessons import Lessons


class TestLessons:
    def test_is_singleton(self):
        lessons1 = Lessons()
        lessons2 = Lessons()
        assert lessons1 is lessons2
