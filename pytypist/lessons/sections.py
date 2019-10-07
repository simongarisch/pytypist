import os
from collections import OrderedDict
from weakref import WeakValueDictionary
from . import util
from .lessons import Lessons
from .singleton import Singleton


class SectionError(Exception):
    """ Base error for sections. """


class SectionNotFound(SectionError):
    """ Unable to find section. """


class SlidesNotFound(SectionError):
    """ Unable to find slides. """


class SectionNameNotUnique(SectionError):
    """ Unable to find slides. """


class Section(OrderedDict):
    _names = WeakValueDictionary()

    @classmethod
    def register(cls, section):
        name = section.name
        if name in cls._names:
            raise SectionNameNotUnique("%s" % name)
        cls._names[name] = section

    @classmethod
    def get_section_by_name(cls, name):
        section = cls._names.get(name)
        if section is None:
            raise SectionNotFound(name)
        return section

    @classmethod
    def list_names(cls):
        """ Returns a list of all section names. """
        return list(cls._names)

    def __init__(self, section_folder):
        super().__init__()
        self._section_folder = section_folder
        lessons = Lessons(section_folder)
        name = self._name = lessons.section
        self[name] = lessons
        Section.register(self)

    @property
    def name(self):
        return self._name

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
        sections_list = self._sections_list = []
        for section_folder in section_folders:
            section = Section(section_folder)
            sections_list.append(section)
            self.update(section)
