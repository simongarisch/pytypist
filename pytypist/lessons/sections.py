from collections import OrderedDict
from . import util
from .lessons import Lessons
from .singleton import Singleton


class SectionError(Exception):
    """ Base error for sections. """


class SlidesNotFound(SectionError):
    """ Unable to find slides. """


class Section(OrderedDict):
    def __init__(self, section_folder):
        super().__init__()
        self._section_folder = section_folder
        lessons = Lessons(section_folder)
        self[lessons.section] = lessons
        self._name = lessons.section

    def collect_slides(self):
        """ Return the path to slides.html for this section. """
        slides_path = os.path.join(
            self._section_folder, "site_folder", "slides.html"
        )
        if not os.path.isfile(slides_path):
            raise SlidesNotFound
        return slides_path


class Sections(OrderedDict, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._populate()

    def _populate(self):
        section_folders = util.list_folder_paths()
        for section_folder in section_folders:
            section = Section(section_folder)
            self.update(section)
