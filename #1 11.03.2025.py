from typing import Sequence

def check_fibonacci(data: Sequence[int]) -> bool:
    if len(data) < 2:
        return False  # Последовательность Фибоначчи должна содержать хотя бы два элемента

    # Проверка, является ли последовательность Фибоначчи
    for i in range(2, len(data)):
        if data[i] != data[i - 1] + data[i - 2]:
            return False

    return True

# Пример использования:
print(check_fibonacci([0, 1, 1, 2, 3, 5, 8]))  # True
print(check_fibonacci([2, 4, 6, 10]))  # False