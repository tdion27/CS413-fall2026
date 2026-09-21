# Assignment 2: LAMBDA0 Pairs and Eight Queens

## Files

- `lambda0.py` contains the extended interpreter.
- `TEST/test02_lambda0.py` tests pairs and projections.
- `queens.dats` is the ATS2 source used for the translation. It was copied
  from `assigns/01/queens.dats`.
- `queens_lambda0.py` constructs and evaluates the translated LAMBDA0 term.
- `TEST/test03_queens.py` tests the translated program.

## Pair and projection extensions

The following constructors are supported by the AST operations and the
call-by-value evaluator:

- `T0Mpair(t1, t2)` constructs a pair.
- `T0Mpfst(t1)` selects the first component.
- `T0Mpsnd(t1)` selects the second component.

Pair construction evaluates the first component and then the second
component. Both components must finish evaluation before the pair is a
value. A projection evaluates its operand first and raises `TypeError` if the
result is not a pair. This means that a projection evaluates an unselected
component as well.

The size, free-variable, and substitution operations recurse through both
components or through the projection operand. Pairs and projections do not
bind variables. The existing closed-substitution assumption and the binding
rules for `T0Mlam` and `T0Mfix` are unchanged.

## ATS2 translation

The original ATS2 program searches row by row and counts all solutions. Its
standard eight-queens run produces 92 solutions.

The LAMBDA0 translation uses these representations:

- A board is a right-nested pair containing eight integer columns and a final
  integer terminator. For example, the columns are represented as
  `pair(c0, pair(c1, ... pair(c7, 0)...))`.
- `board_get` recursively follows second projections until it reaches the
  requested index.
- `board_set` recursively rebuilds the nested pairs while replacing one
  column.
- `safety_test1` checks that two queens have different columns and are not on
  the same diagonal.
- `safety_test2` recursively checks a candidate against all earlier rows.
- `search` is a `T0Mfix` term that tries columns from left to right, advances
  to the next row after a safe placement, counts complete boards, and
  backtracks when a row has no remaining candidate.

The Python code in `queens_lambda0.py` only constructs the AST, starts the
interpreter, and reads the resulting integer. The search and conflict checks
execute inside the LAMBDA0 interpreter.

The starter interpreter already supported integer comparisons and produced
`T0Mbtf` values for them, so no additional primitive operators were needed.
The queens driver raises Python's recursion limit because substitution-based
evaluation expands recursive terms deeply during the full search.

## Running the program and tests

Run these commands from the assignment directory:

```text
python3 MySolution/queens_lambda0.py
python3 -m unittest discover -s MySolution/TEST -p 'test02_lambda0.py'
python3 -m unittest discover -s MySolution/TEST -p 'test03_queens.py'
```

The translation prints:

```text
92
```

The pair/projection suite contains 11 tests, and the queens suite contains 8
tests. Both suites pass. The queens translation is specialized to the fixed
eight-queens problem from the ATS2 source; smaller board sizes and returning
individual boards are not exposed by this implementation.

## Review of AI-generated code

The implementation was manually reviewed after it was generated. I looked
over the code myself, checked that the AST operations preserve the intended
binding behavior, verified the left-to-right call-by-value rules, and
confirmed that the queens search and conflict checks are executed by the
interpreter. The automated tests and the matching result of 92 solutions were
used together with that manual review to validate the code.
