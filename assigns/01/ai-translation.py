#!/usr/bin/env python3
"""Python 3 translation of queens.dats.

This program prints the initial board, then prints all solutions to the
eight-queens puzzle and verifies that there are 92 of them.
"""


N = 8


def print_dots(i: int) -> None:
    if i > 0:
        print(". ", end="")
        print_dots(i - 1)


def print_row(i: int) -> None:
    print_dots(i)
    print("Q ", end="")
    print_dots(N - i - 1)
    print()


def print_board(board: tuple[int, ...]) -> None:
    for row in board:
        print_row(row)
    print()


def board_get(board: tuple[int, ...], i: int) -> int:
    if 0 <= i < N:
        return board[i]
    return 0


def board_set(board: tuple[int, ...], i: int, j: int) -> tuple[int, ...]:
    if 0 <= i < N:
        updated = list(board)
        updated[i] = j
        return tuple(updated)
    return board


def safety_test1(i0: int, j0: int, i: int, j: int) -> bool:
    return j0 != j and abs(i0 - i) != abs(j0 - j)


def safety_test2(i0: int, j0: int, board: tuple[int, ...], i: int) -> bool:
    if i >= 0:
        if safety_test1(i0, j0, i, board_get(board, i)):
            return safety_test2(i0, j0, board, i - 1)
        return False
    return True


def search(board: tuple[int, ...], i: int, j: int, nsol: int) -> int:
    if i == N:
        print(f"Solution #{nsol + 1}:\n")
        print_board(board)
        return nsol + 1

    for column in range(j, N):
        if safety_test2(i, column, board, i - 1):
            board1 = board_set(board, i, column)
            nsol = search(board1, i + 1, 0, nsol)
    return nsol


def main() -> None:
    print_board((0, 1, 2, 3, 4, 5, 6, 7))
    nsol = search((0, 0, 0, 0, 0, 0, 0, 0), 0, 0, 0)
    assert nsol == 92


if __name__ == "__main__":
    main()
