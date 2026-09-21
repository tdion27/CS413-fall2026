import unittest

from MySolution.lambda0 import (
    T0Mapp,
    T0Mbtf,
    T0Mfix,
    T0Mint,
    T0Mlam,
    T0Mop2,
    T0Mpair,
    T0Mpfst,
    T0Mpsnd,
    T0Mstr,
    T0Mvar,
    t0erm_cbv_evaluate0,
    t0erm_fvset,
    t0erm_size,
    t0erm_subst0,
)


class TestPairProjectionASTOperations(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual(t0erm_size(T0Mpair(T0Mint(1), T0Mint(2))), 3)
        self.assertEqual(
            t0erm_size(T0Mpfst(T0Mpair(T0Mint(1), T0Mpsnd(T0Mint(2))))), 5
        )

    def test_free_variables(self):
        term = T0Mpfst(T0Mpair(T0Mvar("x"), T0Mvar("y")))
        self.assertEqual(t0erm_fvset(term), frozenset({"x", "y"}))

        nested = T0Mlam(
            "x",
            T0Mpair(T0Mvar("x"), T0Mpfst(T0Mpair(T0Mvar("y"), T0Mvar("z")))),
        )
        self.assertEqual(t0erm_fvset(nested), frozenset({"y", "z"}))

    def test_substitution_in_both_components_and_projection(self):
        term = T0Mpsnd(T0Mpair(T0Mvar("x"), T0Mvar("y")))
        expected = T0Mpsnd(T0Mpair(T0Mint(10), T0Mint(20)))
        self.assertEqual(t0erm_subst0(t0erm_subst0(term, "x", T0Mint(10)), "y", T0Mint(20)), expected)

    def test_substitution_respects_lambda_and_fix_binders(self):
        under_lambda = T0Mlam("x", T0Mpair(T0Mvar("x"), T0Mvar("y")))
        self.assertEqual(
            t0erm_subst0(under_lambda, "y", T0Mint(1)),
            T0Mlam("x", T0Mpair(T0Mvar("x"), T0Mint(1))),
        )
        self.assertEqual(t0erm_subst0(under_lambda, "x", T0Mint(1)), under_lambda)

        under_fix = T0Mfix("f", "x", T0Mpair(T0Mvar("f"), T0Mvar("y")))
        self.assertEqual(
            t0erm_subst0(under_fix, "y", T0Mbtf(True)),
            T0Mfix("f", "x", T0Mpair(T0Mvar("f"), T0Mbtf(True))),
        )
        self.assertEqual(t0erm_subst0(under_fix, "f", T0Mint(1)), under_fix)
        self.assertEqual(t0erm_subst0(under_fix, "x", T0Mint(1)), under_fix)


class TestPairProjectionEvaluation(unittest.TestCase):
    def test_pair_components_are_evaluated(self):
        term = T0Mpair(
            T0Mop2("+", T0Mint(1), T0Mint(2)),
            T0Mop2("*", T0Mint(3), T0Mint(4)),
        )
        self.assertEqual(t0erm_cbv_evaluate0(term), T0Mpair(T0Mint(3), T0Mint(12)))

    def test_both_projections(self):
        pair = T0Mpair(T0Mint(1), T0Mop2("+", T0Mint(2), T0Mint(3)))
        self.assertEqual(t0erm_cbv_evaluate0(T0Mpfst(pair)), T0Mint(1))
        self.assertEqual(t0erm_cbv_evaluate0(T0Mpsnd(pair)), T0Mint(5))

    def test_nested_pairs_and_mixed_values(self):
        pair = T0Mpair(
            T0Mpair(T0Mint(1), T0Mstr("hello")),
            T0Mlam("x", T0Mvar("x")),
        )
        value = t0erm_cbv_evaluate0(pair)
        self.assertEqual(value.arg1, T0Mpair(T0Mint(1), T0Mstr("hello")))
        self.assertEqual(value.arg2, T0Mlam("x", T0Mvar("x")))
        self.assertEqual(t0erm_cbv_evaluate0(T0Mpfst(pair)), value.arg1)

    def test_functions_accept_and_return_pairs(self):
        first = T0Mlam("p", T0Mpfst(T0Mvar("p")))
        argument = T0Mpair(T0Mint(7), T0Mbtf(False))
        self.assertEqual(t0erm_cbv_evaluate0(T0Mapp(first, argument)), T0Mint(7))

        make_pair = T0Mlam("x", T0Mpair(T0Mvar("x"), T0Mint(2)))
        application = T0Mapp(make_pair, T0Mop2("+", T0Mint(3), T0Mint(4)))
        self.assertEqual(
            t0erm_cbv_evaluate0(T0Mpsnd(application)), T0Mint(2)
        )

    def test_projection_of_non_pair_raises_type_error(self):
        with self.assertRaises(TypeError):
            t0erm_cbv_evaluate0(T0Mpfst(T0Mint(1)))
        with self.assertRaises(TypeError):
            t0erm_cbv_evaluate0(T0Mpsnd(T0Mbtf(True)))

    def test_pair_evaluation_is_left_to_right(self):
        first_error = T0Mpfst(T0Mint(0))
        second_error = T0Mop2("/", T0Mint(1), T0Mint(0))
        with self.assertRaises(TypeError):
            t0erm_cbv_evaluate0(T0Mpair(first_error, second_error))

    def test_unselected_projection_component_is_still_evaluated(self):
        term = T0Mpfst(
            T0Mpair(T0Mint(1), T0Mop2("/", T0Mint(1), T0Mint(0)))
        )
        with self.assertRaises(ZeroDivisionError):
            t0erm_cbv_evaluate0(term)


if __name__ == "__main__":
    unittest.main()
