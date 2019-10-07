import os
from pytypist.lessons import Sections, util


class TestLessons:

    def test_is_singleton(self):
        sections1 = Sections()
        sections2 = Sections()
        assert sections1 is sections2

    def test_list_folder_paths():
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
