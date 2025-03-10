import datetime


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


class Student:
    """Класс, представляющий студента."""

    def __init__(self, first_name: str, last_name: str):
        """
        Инициализация объекта студента.

        :param first_name: Имя студента
        :param last_name: Фамилия студента
        """
        self.first_name = first_name
        self.last_name = last_name

    def do_homework(self, homework: Homework):
        """
        Выполняет домашнее задание.

        :param homework: Экземпляр класса Homework
        :return: Экземпляр Homework, если задание ещё не просрочено, иначе None
        """
        if homework.is_active():
            return homework
        print("You are late")
        return None


class Teacher:
    """Класс, представляющий учителя."""

    def __init__(self, first_name: str, last_name: str):
        """
        Инициализация объекта учителя.

        :param first_name: Имя учителя
        :param last_name: Фамилия учителя
        """
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def create_homework(text: str, days: int) -> Homework:
        """
        Создаёт домашнее задание.

        :param text: Текст задания
        :param days: Количество дней на выполнение
        :return: Экземпляр класса Homework
        """
        return Homework(text, days)


if __name__ == "__main__":
    teacher = Teacher("Daniil", "Shadrin")
    student = Student("Roman", "Petrov")

    print(teacher.last_name)  # Shadrin
    print(student.first_name)  # Roman

    expired_homework = teacher.create_homework("Learn functions", 0)
    print(expired_homework.created)  # Example: 2025-03-10 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too("create 2 simple classes", 5)
    print(oop_homework.deadline)  # 5 days, 0:00:00

    student.do_homework(oop_homework)  # Вернёт объект homework
    student.do_homework(expired_homework)  # Выведет 'You are late'