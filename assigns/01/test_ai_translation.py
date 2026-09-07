#!/usr/bin/env python3
"""Tests for ai-translation.py."""

import contextlib
import importlib.util
import io
import unittest
from pathlib import Path


TRANSLATION = Path(__file__).with_name("ai-translation.py")
SPEC = importlib.util.spec_from_file_location("ai_translation", TRANSLATION)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Unable to load {TRANSLATION}")
ai_translation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ai_translation)


class QueensTranslationTests(unittest.TestCase):
    def test_normal_execution_finds_92_solutions(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            ai_translation.main()

        text = output.getvalue()
        self.assertIn("Q . . . . . . .", text)
        self.assertEqual(text.count("Solution #"), 92)

    def test_boundary_and_unusual_helper_inputs(self):
        board = (0, 1, 2, 3, 4, 5, 6, 7)

        self.assertEqual(ai_translation.board_get(board, -1), 0)
        self.assertEqual(ai_translation.board_get(board, 8), 0)
        self.assertEqual(ai_translation.board_set(board, -1, 4), board)
        self.assertEqual(ai_translation.board_set(board, 8, 4), board)
        self.assertEqual(ai_translation.board_set(board, 3, 6),
                         (0, 1, 2, 6, 4, 5, 6, 7))
        self.assertTrue(ai_translation.safety_test2(0, 0, board, -1))
        self.assertFalse(ai_translation.safety_test1(0, 2, 1, 2))
        self.assertFalse(ai_translation.safety_test1(0, 0, 1, 1))

    def test_all_generated_boards_are_valid_and_unique(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            count = ai_translation.search((0,) * ai_translation.N, 0, 0, 0)

        self.assertEqual(count, 92)
        blocks = output.getvalue().split("Solution #")[1:]
        boards = []
        for block in blocks:
            rows = block.splitlines()[2:10]
            positions = []
            for row in rows:
                cells = row.split()
                self.assertEqual(len(cells), ai_translation.N)
                self.assertEqual(cells.count("Q"), 1)
                positions.append(cells.index("Q"))
            self.assertEqual(len(set(positions)), ai_translation.N)
            self.assertEqual(
                len({row + column for row, column in enumerate(positions)}),
                ai_translation.N,
            )
            self.assertEqual(
                len({row - column for row, column in enumerate(positions)}),
                ai_translation.N,
            )
            boards.append(tuple(positions))

        self.assertEqual(len(boards), 92)
        self.assertEqual(len(set(boards)), 92)


if __name__ == "__main__":
    unittest.main()
