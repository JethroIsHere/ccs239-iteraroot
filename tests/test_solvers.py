import math
import unittest

from iteraroot.expressions import parse_expression
from iteraroot.solvers import fixed_point, newton_raphson


class SolverTests(unittest.TestCase):
    def test_both_methods_reach_known_roots(self):
        cases = [
            ("x^2 - 2", "(x+2)/(x+1)", 1.0, math.sqrt(2)),
            ("x^3 + x - 1", "1/(1+x^2)", 0.5, 0.6823278038280193),
            ("cos(x) - x", "cos(x)", 0.5, 0.7390851332151607),
        ]
        for f_source, g_source, x0, expected in cases:
            f, g = parse_expression(f_source), parse_expression(g_source)
            for result in (fixed_point(f, g, x0), newton_raphson(f, f.derivative(), x0)):
                with self.subTest(function=f_source, method=result.method):
                    self.assertTrue(result.converged, result.message)
                    self.assertAlmostEqual(result.estimate, expected, delta=1e-7)
                    self.assertLessEqual(result.residual, 1e-8)
                    self.assertEqual(result.iterations, len(result.history) - 1)

    def test_records_actual_first_updates(self):
        f = parse_expression("x^3 + x - 1")
        fixed = fixed_point(f, parse_expression("1/(1+x^2)"), 0.5, max_iterations=1)
        newton = newton_raphson(f, f.derivative(), 0.5, max_iterations=1)
        self.assertEqual(fixed.history[1].x, 0.8)
        self.assertAlmostEqual(newton.history[1].x, 0.5 - (-0.375 / 1.75))
        self.assertEqual(fixed.history[0].iteration, 0)
        self.assertIsNone(fixed.history[0].absolute_step)

    def test_exact_starting_root_needs_no_updates_or_derivative(self):
        result = newton_raphson(lambda x: x*x, lambda x: 0, 0)
        self.assertTrue(result.converged)
        self.assertEqual(result.iterations, 0)

    def test_zero_derivative_is_not_convergence(self):
        result = newton_raphson(lambda x: x*x - 2, lambda x: 2*x, 0)
        self.assertFalse(result.converged)
        self.assertEqual(result.status, "zero_derivative")
        self.assertEqual(result.iterations, 0)

    def test_tiny_nonzero_derivative_can_be_valid(self):
        result = newton_raphson(lambda x: 1e-20*(x-1), lambda x: 1e-20, 0)
        self.assertTrue(result.converged)
        self.assertEqual(result.estimate, 1.0)

    def test_fixed_point_cycle_is_reported(self):
        result = fixed_point(lambda x: x-1, lambda x: -x, 2)
        self.assertEqual(result.status, "cycle")
        self.assertEqual(result.iterations, 2)

    def test_newton_cycle_is_reported(self):
        f = parse_expression("x^3 - 2*x + 2")
        result = newton_raphson(f, f.derivative(), 0)
        self.assertEqual(result.status, "cycle")

    def test_wrong_iteration_function_does_not_create_false_root(self):
        result = fixed_point(lambda x: x-1, lambda x: 0, 2)
        self.assertEqual(result.status, "stagnated")
        self.assertFalse(result.converged)
        self.assertEqual(result.residual, 1)

    def test_small_steps_without_small_residual_do_not_converge(self):
        result = fixed_point(lambda x: x-10, lambda x: x+1e-10, 0, max_iterations=2)
        self.assertEqual(result.status, "iteration_limit")
        self.assertFalse(result.converged)

    def test_domain_error_at_initial_point(self):
        f = parse_expression("log(x)")
        result = newton_raphson(f, f.derivative(), -1)
        self.assertEqual(result.status, "domain_error")
        self.assertIsNone(result.estimate)

    def test_domain_error_during_fixed_iteration_is_not_zero_derivative(self):
        result = fixed_point(lambda x: x-1, lambda x: 1/x, 0)
        self.assertEqual(result.status, "domain_error")

    def test_nonfinite_function_is_rejected(self):
        result = fixed_point(lambda x: math.inf, lambda x: x, 1)
        self.assertEqual(result.status, "domain_error")
        self.assertIsNone(result.residual)

    def test_relative_step_at_zero_is_unavailable(self):
        result = fixed_point(lambda x: x, lambda x: 0, 1)
        self.assertTrue(result.converged)
        self.assertIsNone(result.history[-1].relative_step_percent)

    def test_divergence_reaches_limit_without_claiming_root(self):
        result = fixed_point(lambda x: x-1, lambda x: 2*x, 2, max_iterations=5)
        self.assertEqual(result.status, "iteration_limit")
        self.assertEqual(result.iterations, 5)

    def test_invalid_solver_settings(self):
        for setting in (
            {"x_tolerance": 0}, {"residual_tolerance": -1},
            {"max_iterations": 0}, {"max_iterations": 1.5}, {"max_iterations": True},
        ):
            with self.subTest(setting=setting), self.assertRaises(ValueError):
                fixed_point(lambda x: x-1, lambda x: x, 1, **setting)
        with self.assertRaises(ValueError):
            fixed_point(lambda x: x-1, lambda x: x, math.nan)


if __name__ == "__main__":
    unittest.main()
