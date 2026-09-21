"""Eight queens translated from MySolution/queens.dats.

The board is represented as a right-nested pair of eight columns followed by
an unused integer terminator.  For example, a board is
    pair(c0, pair(c1, ... pair(c7, 0)...)).

All search and conflict checking below are represented as LAMBDA0 terms.
Python is used only to construct the AST and decode the resulting integer.
"""

import sys


# Substitution duplicates recursive terms; the eight-queens search therefore
# needs more Python stack space than the default recursion limit provides.
sys.setrecursionlimit(100_000)

try:
    from MySolution.lambda0 import (
        T0Mapp,
        T0Mbtf,
        T0Mfix,
        T0Mint,
        T0Mif0,
        T0Mlam,
        T0Mop1,
        T0Mop2,
        T0Mpair,
        T0Mpfst,
        T0Mpsnd,
        T0Mvar,
        t0erm_cbv_evaluate0,
    )
except ModuleNotFoundError:  # Direct execution: python MySolution/queens_lambda0.py
    from lambda0 import (
        T0Mapp,
        T0Mbtf,
        T0Mfix,
        T0Mint,
        T0Mif0,
        T0Mlam,
        T0Mop1,
        T0Mop2,
        T0Mpair,
        T0Mpfst,
        T0Mpsnd,
        T0Mvar,
        t0erm_cbv_evaluate0,
    )


def v(name):
    return T0Mvar(name)


def i(value):
    return T0Mint(value)


def lam(name, body):
    return T0Mlam(name, body)


def app(function, argument):
    return T0Mapp(function, argument)


def apps(function, *arguments):
    for argument in arguments:
        function = app(function, argument)
    return function


def fix(name, parameter, body):
    return T0Mfix(name, parameter, body)


def op1(operator, operand):
    return T0Mop1(operator, operand)


def op2(operator, left, right):
    return T0Mop2(operator, left, right)


def if0(condition, when_true, when_false):
    return T0Mif0(condition, when_true, when_false)


def let(name, value, body):
    return app(lam(name, body), value)


def board_term(columns):
    board = i(0)
    for column in reversed(columns):
        board = T0Mpair(i(column), board)
    return board


def board_get_term():
    # board_get(bd, index)
    body = if0(
        op2("==", v("index"), i(0)),
        T0Mpfst(v("bd")),
        apps(v("get"), T0Mpsnd(v("bd")), op2("-", v("index"), i(1))),
    )
    return fix("get", "bd", lam("index", body))


def board_set_term():
    # board_set(bd, index, column)
    body = if0(
        op2("==", v("index"), i(0)),
        T0Mpair(v("column"), T0Mpsnd(v("bd"))),
        T0Mpair(
            T0Mpfst(v("bd")),
            apps(
                v("set"),
                T0Mpsnd(v("bd")),
                op2("-", v("index"), i(1)),
                v("column"),
            ),
        ),
    )
    return fix("set", "bd", lam("index", lam("column", body)))


def absolute_term():
    # abs(x)
    return lam(
        "x",
        if0(op2("<", v("x"), i(0)), op1("-", v("x")), v("x")),
    )


def safety_test1_term():
    # safety_test1(i0, j0, i, j)
    row_difference = op2("-", v("i0"), v("i"))
    column_difference = op2("-", v("j0"), v("j"))
    diagonal_safe = op2(
        "!=", apps(v("abs"), row_difference), apps(v("abs"), column_difference)
    )
    return lam(
        "i0",
        lam(
            "j0",
            lam(
                "i",
                lam(
                    "j",
                    if0(op2("!=", v("j0"), v("j")), diagonal_safe, T0Mbtf(False)),
                ),
            ),
        ),
    )


def safety_test2_term():
    # safety_test2(i0, j0, bd, i)
    recursive_check = apps(
        v("safe"),
        v("i0"),
        v("j0"),
        v("bd"),
        op2("-", v("i"), i(1)),
    )
    current_check = apps(
        v("safe1"),
        v("i0"),
        v("j0"),
        v("i"),
        apps(v("get"), v("bd"), v("i")),
    )
    body = if0(
        op2(">=", v("i"), i(0)),
        if0(current_check, recursive_check, T0Mbtf(False)),
        T0Mbtf(True),
    )
    return fix(
        "safe",
        "i0",
        lam("j0", lam("bd", lam("i", body))),
    )


def search_term():
    # search(bd, i, j, nsol)
    next_column = op2("+", v("j"), i(1))
    next_solution_count = op2("+", v("nsol"), i(1))
    test = apps(v("safe2"), v("i"), v("j"), v("bd"), op2("-", v("i"), i(1)))
    placed_board = apps(v("set"), v("bd"), v("i"), v("j"))
    continue_after_solution = apps(
        v("search"), v("bd"), v("i"), next_column, next_solution_count
    )
    continue_with_next_row = apps(
        v("search"), placed_board, op2("+", v("i"), i(1)), i(0), v("nsol")
    )
    try_next_column = apps(v("search"), v("bd"), v("i"), next_column, v("nsol"))
    backtrack = if0(
        op2(">", v("i"), i(0)),
        apps(
            v("search"),
            v("bd"),
            op2("-", v("i"), i(1)),
            op2("+", apps(v("get"), v("bd"), op2("-", v("i"), i(1))), i(1)),
            v("nsol"),
        ),
        v("nsol"),
    )
    try_candidate = if0(
        op2("==", op2("+", v("i"), i(1)), i(8)),
        continue_after_solution,
        continue_with_next_row,
    )
    body = if0(
        op2("<", v("j"), i(8)),
        if0(test, try_candidate, try_next_column),
        backtrack,
    )
    return fix(
        "search",
        "bd",
        lam("i", lam("j", lam("nsol", body))),
    )


def build_queens_term():
    """Construct a closed term that evaluates to the number of solutions."""

    initial_board = board_term([0] * 8)
    run_search = apps(v("search"), initial_board, i(0), i(0), i(0))
    return let(
        "abs",
        absolute_term(),
        let(
            "safe1",
            safety_test1_term(),
            let(
                "get",
                board_get_term(),
                let(
                    "safe2",
                    safety_test2_term(),
                    let(
                        "set",
                        board_set_term(),
                        let("search", search_term(), run_search),
                    ),
                ),
            ),
        ),
    )


def count_solutions():
    result = t0erm_cbv_evaluate0(build_queens_term())
    if not isinstance(result, T0Mint):
        raise TypeError(f"expected an integer solution count, got {result}")
    return result.arg1


if __name__ == "__main__":
    print(count_solutions())
