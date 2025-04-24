import mysql.connector
import random
import datetime
import uuid

# Параметры подключения к базе данных MySQL
DATABASE_HOST = "mysql"  # Имя контейнера, указано в docker-compose.yml
DATABASE_PORT = 3306  # Внутренний порт MySQL в контейнере
DATABASE_USER = "root"
DATABASE_PASSWORD = "root"
DATABASE_NAME = "mydatabase"

# Подключение к базе данных
conn = mysql.connector.connect(
    host=DATABASE_HOST,
    port=DATABASE_PORT,  # Внутренний порт MySQL контейнера
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    database=DATABASE_NAME
)

cursor = conn.cursor()

# Список типов действий
action_types = [
    "first_visit",  # первый заход на сайт
    "registration",  # регистрация
    "login",  # логин
    "logout",  # логаут
    "create_topic",  # создание темы
    "visit_topic",  # заход на тему
    "delete_topic",  # удаление темы
    "post_message"  # написание сообщения
]

# Список пользователей (для примера)
users = ["user1", "user2", "user3", "user4", "user5"]


# Генерация случайных данных для логов
def generate_logs(num_logs):
    logs = []
    for _ in range(num_logs):
        action = random.choice(action_types)  # случайный тип действия
        user = random.choice(users) if action != "post_message" else None  # сообщение может быть анонимным

        # Если действие — создание темы, проверяем залогинен ли пользователь
        if action == "create_topic" and user is None:
            action = "create_topic_error"  # ошибка, если пользователь не залогинен

        # Генерация случайных данных
        log_id = str(uuid.uuid4())  # уникальный ID для лога
        timestamp = datetime.datetime.now() - datetime.timedelta(
            days=random.randint(0, 30))  # случайная дата в пределах последнего месяца
        response = "success" if action != "create_topic_error" else "error"  # если ошибка - то response error
        topic_id = random.randint(1, 100) if action in ["create_topic", "delete_topic", "visit_topic"] else None
        message_id = random.randint(1, 1000) if action == "post_message" else None

        log = {
            "log_id": log_id,
            "action": action,
            "user": user,
            "topic_id": topic_id,
            "message_id": message_id,
            "response": response,
            "timestamp": timestamp
        }
        logs.append(log)
    return logs


# Вставка данных в таблицу logs
def insert_logs(logs):
    for log in logs:
        cursor.execute("""
            INSERT INTO user_logs (log_id, action, user, topic_id, message_id, response, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (log["log_id"], log["action"], log["user"], log["topic_id"], log["message_id"], log["response"],
              log["timestamp"]))
    conn.commit()


# Генерация логов
logs = generate_logs(100)  # генерируем 100 логов для примера

# Вставка сгенерированных логов в базу данных
insert_logs(logs)

# Закрытие соединения
cursor.close()
conn.close()

print("Data successfully inserted into the database!")