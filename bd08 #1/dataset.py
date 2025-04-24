import random
from datetime import datetime, timedelta

# Типы действий, которые могут быть выполнены
action_types = [
    "Первый заход на сайт",
    "Регистрация",
    "Логин",
    "Логаут",
    "Создание темы",
    "Заход на тему",
    "Удаление темы",
    "Написание сообщения"
]


# Функция для генерации случайных данных
def generate_logs(start_date, num_days=30):
    logs = []
    current_date = start_date

    for _ in range(num_days):
        # Генерация числа действий за день (с учетом минимальных порогов)
        actions_per_day = {
            action: max(5, random.randint(5, 10))  # минимум 5 действий каждого типа
            for action in action_types
        }

        # Обрабатываем конкретные условия:

        # Создание темы — минимум 2 случая ошибки
        actions_per_day["Создание темы"] += 2
        actions_per_day["Создание темы"] -= 2  # Для двух случаев ошибки

        # Написание сообщения — случайное распределение залогиненых и незалогиненых пользователей
        logged_in_users_count = actions_per_day["Написание сообщения"] // 2
        logged_out_users_count = actions_per_day["Написание сообщения"] - logged_in_users_count

        # Генерация действий для дня
        for action, count in actions_per_day.items():
            for _ in range(count):
                log = generate_action_log(action, current_date, logged_in_users_count, logged_out_users_count)
                logs.append(log)

        # Переходим к следующему дню
        current_date += timedelta(days=1)

    return logs


# Функция для генерации одного действия
def generate_action_log(action, date, logged_in_users_count, logged_out_users_count):
    user_id = None
    response = "Успех"

    # Обработка различных типов действий
    if action == "Первый заход на сайт":
        user_id = random.randint(1, 100)
        response = "Успех"

    elif action == "Регистрация":
        user_id = random.randint(1, 100)
        response = "Успех"

    elif action == "Логин":
        user_id = random.randint(1, 100)
        response = "Успех"

    elif action == "Логаут":
        user_id = random.randint(1, 100)
        response = "Успех"

    elif action == "Создание темы":
        user_id = random.randint(1, 100)
        # 2 случая ошибки при отсутствии логина
        if user_id is None:
            response = "Ошибка: Нет логина"
        else:
            response = "Успех"

    elif action == "Заход на тему":
        user_id = random.randint(1, 100)
        response = "Успех"

    elif action == "Удаление темы":
        user_id = random.randint(1, 100)
        response = "Успех"

    elif action == "Написание сообщения":
        # 50% шанс для анонимных пользователей
        if random.random() < 0.5:
            user_id = None
        else:
            user_id = random.randint(1, 100)

        response = "Успех"

    return {
        "user_id": user_id,
        "action": action,
        "target_id": random.randint(1, 1000),  # Идентификатор объекта действия (например, темы/сообщения)
        "action_description": action,
        "response": response,
        "action_timestamp": date.strftime("%Y-%m-%d %H:%M:%S")
    }


# Генерация данных за месяц
start_date = datetime(2025, 4, 1)
logs = generate_logs(start_date, num_days=30)

# Печать первого десятка записей
for log in logs[:10]:
    print(log)