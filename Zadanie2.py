import datetime
from collections import defaultdict


class DeadlineError(Exception):
    """Ошибка, возникающая при просроченном задании."""

    pass


class Person:
    """Базовый класс для студентов и преподавателей."""

    def __init__(self, first_name: str, last_name: str):
        """
        Инициализация объекта.

        :param first_name: Имя
        :param last_name: Фамилия
        """
        self.first_name = first_name
        self.last_name = last_name


class Homework:
    """Класс, представляющий домашнее задание."""

    def __init__(self, text: str, days: int):
        """
        Инициализация объекта домашнего задания.

        :param text: Текст задания
        :param days: Количество дней на выполнение
        """
        self.text = text
        self.deadline = datetime.timedelta(days=days)
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        """
        Проверяет, не истёк ли срок выполнения задания.

        :return: True, если задание ещё можно выполнить, иначе False
        """
        return datetime.datetime.now() - self.created < self.deadline


class HomeworkResult:
    """Класс, представляющий результат выполнения домашнего задания."""

    def __init__(self, author: "Student", homework: Homework, solution: str):
        """
        Инициализация результата выполнения ДЗ.

        :param author: Автор работы (объект Student)
        :param homework: Исходное задание (объект Homework)
        :param solution: Решение в виде строки
        """
        if not isinstance(homework, Homework):
            raise TypeError("You gave a not Homework object")
        self.author = author
        self.homework = homework
        self.solution = solution
        self.created = datetime.datetime.now()


class Student(Person):
    """Класс, представляющий студента."""

    def do_homework(self, homework: Homework, solution: str) -> HomeworkResult:
        """
        Выполняет домашнее задание.

        :param homework: Экземпляр класса Homework
        :param solution: Решение задания в виде строки
        :return: Экземпляр HomeworkResult, если задание ещё не просрочено,
                 иначе вызывается исключение DeadlineError
        """
        if not homework.is_active():
            raise DeadlineError("You are late")
        return HomeworkResult(self, homework, solution)


class Teacher(Person):
    """Класс, представляющий учителя."""

    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text: str, days: int) -> Homework:
        """
        Создаёт домашнее задание.

        :param text: Текст задания
        :param days: Количество дней на выполнение
        :return: Экземпляр класса Homework
        """
        return Homework(text, days)

    @classmethod
    def check_homework(cls, result: HomeworkResult) -> bool:
        """
        Проверяет выполнение домашнего задания.

        :param result: Экземпляр HomeworkResult
        :return: True, если решение содержит больше 5 символов, иначе False
        """
        if len(result.solution) > 5:
            cls.homework_done[result.homework].add(result)
            return True
        return False

    @classmethod
    def reset_results(cls, homework: Homework = None) -> None:
        """
        Очищает результаты проверок домашних заданий.

        :param homework: Экземпляр Homework (если передан, удаляет только его результаты)
                         Если не передан, очищает весь homework_done.
        """
        if homework:
            cls.homework_done.pop(homework, None)
        else:
            cls.homework_done.clear()


if __name__ == "__main__":
    opp_teacher = Teacher("Daniil", "Shadrin")
    advanced_python_teacher = Teacher("Aleksandr", "Smetanin")

    lazy_student = Student("Roman", "Petrov")
    good_student = Student("Lev", "Sokolov")

    oop_hw = opp_teacher.create_homework("Learn OOP", 1)
    docs_hw = opp_teacher.create_homework("Read docs", 5)

    result_1 = good_student.do_homework(oop_hw, "I have done this hw")
    result_2 = good_student.do_homework(docs_hw, "I have done this hw too")
    result_3 = lazy_student.do_homework(docs_hw, "done")

    try:
        result_4 = HomeworkResult(good_student, "fff", "Solution")
    except Exception:
        print("There was an exception here")

    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done
    assert temp_1 == temp_2

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    print(Teacher.homework_done[oop_hw])
    Teacher.reset_results()