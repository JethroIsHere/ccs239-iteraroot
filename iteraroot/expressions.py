"""Turn a restricted mathematical expression into a real scalar function.

Raw user input is parsed as an AST; it is never passed to Python eval,
SymPy sympify, or parse_expr. Only explicit mathematical constructs are built.
"""

from __future__ import annotations

import ast
import math
from dataclasses import dataclass
from typing import Callable

import sympy as sp

X = sp.Symbol("x", real=True)
FUNCTIONS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "sqrt": sp.sqrt,
}
CONSTANTS = {"pi": sp.pi, "e": sp.E, "E": sp.E}


class ExpressionError(ValueError):
    """An expression is unsupported or malformed."""


class EvaluationError(ValueError):
    """An expression cannot be evaluated as a finite real number."""


@dataclass(frozen=True)
class RealExpression:
    expression: sp.Expr
    _function: Callable[[float], float]

    @property
    def latex(self) -> str:
        return sp.latex(self.expression)

    def __call__(self, value: float) -> float:
        try:
            result = float(self._function(value))
        except (ArithmeticError, TypeError, ValueError) as exc:
            raise EvaluationError(
                f"Expression is undefined or outside the real domain at x={value:.8g}."
            ) from exc
        if not math.isfinite(result):
            raise EvaluationError(f"Expression is not finite at x={value:.8g}.")
        return result

    def derivative(self) -> RealExpression:
        return _compile(sp.diff(self.expression, X))


def _compile(expression: sp.Expr) -> RealExpression:
    try:
        function = sp.lambdify(X, expression, modules="math", cse=False)
    except (ArithmeticError, TypeError, ValueError, KeyError) as exc:
        raise ExpressionError("This expression cannot be evaluated numerically.") from exc
    return RealExpression(expression, function)


def parse_expression(source: str) -> RealExpression:
    """Accept explicit operators, x, pi, e, and a small set of functions."""
    if not isinstance(source, str) or not source.strip():
        raise ExpressionError("Enter a mathematical expression.")
    if len(source) > 300:
        raise ExpressionError("Keep expressions within 300 characters.")
    try:
        tree = ast.parse(source.strip().replace("^", "**"), mode="eval")
    except (SyntaxError, ValueError, RecursionError) as exc:
        raise ExpressionError("Use syntax such as x^3 + x - 1 or cos(x) - x.") from exc
    if sum(1 for _ in ast.walk(tree)) > 100:
        raise ExpressionError("This expression has too many operations.")

    def build(node: ast.AST, depth: int = 0) -> sp.Expr:
        if depth > 20:
            raise ExpressionError("This expression is nested too deeply.")
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if not math.isfinite(node.value) or abs(node.value) > 1e12:
                raise ExpressionError("Use finite numeric constants with magnitude at most 10^12.")
            return sp.Integer(node.value) if type(node.value) is int else sp.Float(node.value)
        if isinstance(node, ast.Name):
            if node.id == "x":
                return X
            if node.id in CONSTANTS:
                return CONSTANTS[node.id]
            raise ExpressionError(f"Unknown name '{node.id}'. Use x as the variable.")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = build(node.operand, depth + 1)
            return value if isinstance(node.op, ast.UAdd) else sp.Mul(-1, value, evaluate=False)
        if isinstance(node, ast.BinOp):
            left, right = build(node.left, depth + 1), build(node.right, depth + 1)
            if isinstance(node.op, ast.Add):
                return sp.Add(left, right, evaluate=False)
            if isinstance(node.op, ast.Sub):
                return sp.Add(left, sp.Mul(-1, right, evaluate=False), evaluate=False)
            if isinstance(node.op, ast.Mult):
                return sp.Mul(left, right, evaluate=False)
            if isinstance(node.op, ast.Div):
                return sp.Mul(left, sp.Pow(right, -1, evaluate=False), evaluate=False)
            if isinstance(node.op, ast.Pow):
                if right.is_number:
                    try:
                        numeric_power = float(right)
                    except (ArithmeticError, ValueError, TypeError) as exc:
                        raise ExpressionError("Use a finite real exponent.") from exc
                    if not math.isfinite(numeric_power) or abs(numeric_power) > 100:
                        raise ExpressionError("Constant exponents must have magnitude at most 100.")
                return sp.Pow(left, right, evaluate=False)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name in FUNCTIONS and len(node.args) == 1 and not node.keywords:
                return FUNCTIONS[name](build(node.args[0], depth + 1), evaluate=False)
        raise ExpressionError(
            "Use +, -, *, /, ^, parentheses, and sin, cos, tan, exp, log, or sqrt. "
            "Write multiplication explicitly, for example 2*x."
        )

    try:
        return _compile(build(tree.body))
    except (RecursionError, OverflowError) as exc:
        raise ExpressionError("This expression is too complex to process.") from exc
