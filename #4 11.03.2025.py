from table_data import TableData

# Подключаемся к таблице "presidents" в базе данных example.sqlite
presidents = TableData('example.sqlite', 'presidents')

# Проверяем количество записей
print(f"Количество президентов: {len(presidents)}")

# Проверяем, есть ли президент с именем 'Yeltsin'
print("Yeltsin" in presidents)  # Должно вернуть True или False

# Получаем данные о конкретном президенте
print(presidents["Yeltsin"])  # {'name': 'Yeltsin', ...}

# Итерация по таблице
for president in presidents:
    print(president['name'])