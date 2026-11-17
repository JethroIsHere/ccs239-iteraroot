import math
import unittest

from iteraroot.expressions import EvaluationError, ExpressionError, parse_expression


class ExpressionTests(unittest.TestCase):
    def test_polynomial_and_automatic_derivative(self):
        expression = parse_expression("x^3 + 2*x - 1")
        self.assertEqual(expression(2), 11)
        self.assertEqual(expression.derivative()(2), 14)

    def test_supported_functions_and_constants(self):
        cases = {
            "sin(pi/2)": 1, "cos(0)": 1, "tan(0)": 0,
            "exp(0)": 1, "log(e)": 1, "ln(E)": 1, "sqrt(4)": 2,
            "x**2": 9,
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertAlmostEqual(parse_expression(source)(3), expected)

    def test_unary_and_scientific_notation(self):
        self.assertAlmostEqual(parse_expression("-x + 1e-3")(2), -1.999)

    def test_rejects_non_math_constructs(self):
        for source in (
            "__import__('os').getcwd()", "x.real", "[x]", "True", "y+1",
            "lambda x:x", "sum([1,2])", "x//2", "x%2", "2x", "sin(x, 2)",
            "x^1000", "1e999", "x if x else 1", "",
        ):
            with self.subTest(source=source), self.assertRaises(ExpressionError):
                parse_expression(source)

    def test_real_domain_and_overflow_are_reported(self):
        for source, point in (("sqrt(x)", -1), ("1/x", 0), ("log(x)", -1), ("exp(x)", 1000)):
            with self.subTest(source=source), self.assertRaises(EvaluationError):
                parse_expression(source)(point)

    def test_zero_function_derivative(self):
        self.assertEqual(parse_expression("0*x").derivative()(1), 0)


if __name__ == "__main__":
    unittest.main()
