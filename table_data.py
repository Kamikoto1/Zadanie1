import sqlite3
from collections.abc import Collection, Iterable, Iterator


class TableData(Collection):
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def _connect(self):
        """Создает соединение с базой данных и возвращает курсор."""
        conn = sqlite3.connect(self.database_name)
        conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        return conn, conn.cursor()

    def __len__(self):
        """Возвращает количество строк в таблице."""
        conn, cursor = self._connect()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def __getitem__(self, name: str):
        """Возвращает строку из таблицы по имени."""
        conn, cursor = self._connect()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)  # Преобразуем результат в словарь
        else:
            raise KeyError(f"No entry with name '{name}'")

    def __contains__(self, name: str):
        """Проверяет, существует ли запись с данным именем в таблице."""
        conn, cursor = self._connect()
        cursor.execute(f"SELECT 1 FROM {self.table_name} WHERE name = ?", (name,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def __iter__(self) -> Iterator:
        """Итерирует по всем строкам в таблице, не загружая их все в память."""
        conn, cursor = self._connect()
        cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY name")
        while row := cursor.fetchone():
            yield dict(row)
        conn.close()