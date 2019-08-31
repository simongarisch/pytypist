from . import util


class Lesson:
    def __init__(self, file_name):
        self.file_name = file_name
        section, name, number, content = validate_lesson()



def main():
    lesson = Lesson("lesson_0.ini")


if __name__ == "__main__":
    main()