# Test Cases and Results

The translated program does not read user input. Therefore, the normal input
case is a normal invocation of the program, while the boundary case exercises
the helper functions with values just outside the valid eight-row board.

## Test cases

| Test | Category | Expected result |
| --- | --- | --- |
| Run `main()` normally | Normal case | Prints the initial board, prints 92 solution headers, and passes the `nsol == 92` assertion. |
| Call `board_get` with `-1` and `8`; call `board_set` with `-1` and `8` | Boundary/unusual case | Invalid indices return `0` or leave the board unchanged, matching the ATS helper behavior. |
| Check safety for a directly conflicting column and diagonal | Additional edge case | Both conflicts are rejected. |
| Generate and inspect every solution | Additional case | There are 92 unique boards; each has one queen per row and column and no diagonal conflicts. |

## Results

Command run from the repository root:

```text
python3 -m unittest discover -s assigns/01 -p 'test_*.py' -v
```

Result:

```text
Ran 3 tests in 0.020s
OK
```

The suite also verifies that the generated output contains exactly 92
solutions and that all generated boards are valid and unique.
