import string
from typing import List, Dict


def get_longest_diverse_words(file_path: str) -> List[str]:
    """Находит 10 самых длинных слов с наибольшим количеством уникальных символов."""
    words = set()
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            for word in line.split():
                word = word.strip(string.punctuation)
                words.add(word)

    words = sorted(words, key=lambda w: (-len(set(w)), -len(w)))
    return words[:10]


def get_rarest_char(file_path: str) -> str:
    """Находит самый редкий символ в файле."""
    char_count: Dict[str, int] = {}
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            for char in line:
                char_count[char] = char_count.get(char, 0) + 1

    return min(char_count, key=char_count.get)


def count_punctuation_chars(file_path: str) -> int:
    """Подсчитывает количество знаков пунктуации в файле."""
    punctuation_count = 0
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            punctuation_count += sum(1 for char in line if char in string.punctuation)

    return punctuation_count


def count_non_ascii_chars(file_path: str) -> int:
    """Подсчитывает количество не-ASCII символов (например, буквы с умляутами)."""
    non_ascii_count = 0
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            non_ascii_count += sum(1 for char in line if ord(char) > 127)

    return non_ascii_count


if __name__ == "__main__":
    file_path = "data.txt"  # Убедись, что этот файл есть в папке проекта
    print("10 самых длинных слов с уникальными буквами:", get_longest_diverse_words(file_path))
    print("Самый редкий символ:", get_rarest_char(file_path))
    print("Количество знаков пунктуации:", count_punctuation_chars(file_path))
    print("Количество не-ASCII символов:", count_non_ascii_chars(file_path))
    print("Самый частый не-ASCII символ:", get_most_common_non_ascii_char(file_path))