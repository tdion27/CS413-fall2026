import unittest
from pathlib import Path

from MySolution.lambda0 import (
    T0Mbtf,
    T0Mint,
    T0Mpair,
    T0Mvar,
    t0erm_cbv_evaluate0,
    t0erm_fvset,
)
from MySolution.queens_lambda0 import (
    absolute_term,
    apps,
    board_get_term,
    board_set_term,
    board_term,
    build_queens_term,
    count_solutions,
    let,
    safety_test1_term,
    v,
    i,
)


class TestQueensTranslation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The substitution-based interpreter evaluates the complete search;
        # cache the result so the expensive run happens only once.
        cls.solution_count = count_solutions()

    def test_original_ats_source_is_in_submission(self):
        source = Path(__file__).parents[1] / "queens.dats"
        self.assertTrue(source.is_file())

    def test_translated_program_is_closed(self):
        self.assertEqual(t0erm_fvset(build_queens_term()), frozenset())

    def test_translated_program_finds_92_solutions(self):
        self.assertEqual(self.solution_count, 92)

    def test_board_get_and_set_terms(self):
        board = board_term([0] * 8)
        updated_board = apps(board_set_term(), board, i(3), i(6))
        get_updated_column = apps(board_get_term(), updated_board, i(3))
        self.assertEqual(t0erm_cbv_evaluate0(get_updated_column), T0Mint(6))

    def test_board_is_nested_pair_data(self):
        board = t0erm_cbv_evaluate0(board_term([0, 1, 2, 3, 4, 5, 6, 7]))
        self.assertIsInstance(board, T0Mpair)
        self.assertEqual(board.arg1, T0Mint(0))

    def evaluate_safety_test1(self, i0, j0, i_value, j):
        term = let(
            "abs",
            absolute_term(),
            apps(safety_test1_term(), i(i0), i(j0), i(i_value), i(j)),
        )
        result = t0erm_cbv_evaluate0(term)
        self.assertIsInstance(result, T0Mbtf)
        return result.arg1

    def test_conflict_check_same_column(self):
        self.assertFalse(self.evaluate_safety_test1(2, 4, 5, 4))

    def test_conflict_check_diagonal(self):
        self.assertFalse(self.evaluate_safety_test1(2, 4, 5, 7))
        self.assertFalse(self.evaluate_safety_test1(5, 7, 2, 4))

    def test_conflict_check_safe_position(self):
        self.assertTrue(self.evaluate_safety_test1(2, 4, 5, 0))


if __name__ == "__main__":
    unittest.main()
