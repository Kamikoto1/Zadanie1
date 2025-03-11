from typing import List


def tic_tac_toe_checker(board: List[List[str]]) -> str:
    # Проверяем строки и столбцы
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "-":
            return f"{board[i][0]} wins!"
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "-":
            return f"{board[0][i]} wins!"

    # Проверяем диагонали
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "-":
        return f"{board[0][0]} wins!"
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-":
        return f"{board[0][2]} wins!"

    # Проверяем, есть ли свободные клетки
    if any("-" in row for row in board):
        return "unfinished!"

    return "draw!"


# Тесты
boards = [
    [["-", "-", "o"],
     ["-", "x", "o"],
     ["x", "o", "x"]],  # unfinished

    [["-", "-", "o"],
     ["-", "o", "o"],
     ["x", "x", "x"]],  # x wins!

    [["o", "o", "o"],
     ["x", "x", "-"],
     ["-", "-", "x"]],  # o wins!

    [["x", "o", "x"],
     ["x", "o", "o"],
     ["o", "x", "x"]],  # draw!
]

for b in boards:
    print(tic_tac_toe_checker(b))