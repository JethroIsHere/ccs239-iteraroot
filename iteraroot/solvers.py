"""Transparent implementations of ordinary fixed point and Newton iterations.

The steps are written explicitly so the class can inspect and explain them.
Neither algorithm delegates the solution to a library root finder.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

ScalarFunction = Callable[[float], float]


class _ZeroDerivativeError(ArithmeticError):
    """A Newton update has no usable tangent slope."""


@dataclass(frozen=True)
class Iteration:
    iteration: int
    x: float
    fx: float
    absolute_step: float | None
    relative_step_percent: float | None

    @property
    def residual(self) -> float:
        return abs(self.fx)


@dataclass(frozen=True)
class SolveResult:
    method: str
    status: str
    message: str
    history: tuple[Iteration, ...]

    @property
    def converged(self) -> bool:
        return self.status == "converged"

    @property
    def iterations(self) -> int:
        return max(0, len(self.history) - 1)

    @property
    def estimate(self) -> float | None:
        return self.history[-1].x if self.history else None

    @property
    def residual(self) -> float | None:
        return self.history[-1].residual if self.history else None


def _finite_call(function: ScalarFunction, x: float) -> float:
    result = float(function(x))
    if not math.isfinite(result):
        raise ValueError("The calculation produced a non-finite number.")
    return result


def _validate(x0: float, x_tolerance: float, residual_tolerance: float, max_iterations: int) -> None:
    if not math.isfinite(x0):
        raise ValueError("The initial guess must be finite.")
    if not math.isfinite(x_tolerance) or x_tolerance <= 0:
        raise ValueError("The step tolerance must be positive and finite.")
    if not math.isfinite(residual_tolerance) or residual_tolerance <= 0:
        raise ValueError("The residual tolerance must be positive and finite.")
    if type(max_iterations) is not int or not 1 <= max_iterations <= 1000:
        raise ValueError("The iteration limit must be an integer from 1 to 1000.")


def _iterate(
    f: ScalarFunction,
    update: Callable[[float, float], float],
    x0: float,
    x_tolerance: float,
    residual_tolerance: float,
    max_iterations: int,
    method: str,
) -> SolveResult:
    _validate(x0, x_tolerance, residual_tolerance, max_iterations)
    rows: list[Iteration] = []

    def finish(status: str, message: str) -> SolveResult:
        return SolveResult(method, status, message, tuple(rows))

    try:
        fx = _finite_call(f, x0)
    except (ArithmeticError, ValueError, TypeError) as exc:
        return finish("domain_error", f"Cannot evaluate the starting point: {exc}")
    rows.append(Iteration(0, float(x0), fx, None, None))
    if fx == 0.0:
        return finish("converged", "The initial guess already evaluates to a root.")

    x = float(x0)
    seen = {x}
    for n in range(1, max_iterations + 1):
        try:
            next_x = float(update(x, fx))
            if not math.isfinite(next_x):
                return finish("numerical_limit", "The update produced a non-finite estimate.")
            next_fx = _finite_call(f, next_x)
            step = abs(next_x - x)
            if not math.isfinite(step):
                return finish("numerical_limit", "The change in estimates exceeded numeric limits.")
        except _ZeroDerivativeError as exc:
            return finish("zero_derivative", str(exc))
        except (ArithmeticError, ValueError, TypeError) as exc:
            return finish("domain_error", f"Iteration {n} could not be completed: {exc}")
        relative = abs(1.0 - x / next_x) * 100.0 if next_x != 0.0 else None
        if relative is not None and not math.isfinite(relative):
            relative = None
        rows.append(Iteration(n, next_x, next_fx, step, relative))

        if next_fx == 0.0:
            return finish("converged", "The estimate evaluates to zero in floating-point arithmetic.")
        if step <= x_tolerance and abs(next_fx) <= residual_tolerance:
            return finish("converged", "Both step and residual meet the requested tolerances.")
        if next_x == x:
            return finish(
                "stagnated",
                "The estimate stopped changing, but the residual is still too large. "
                "For Fixed Point Iteration, check that g(x)=x corresponds to f(x)=0.",
            )
        if next_x in seen:
            return finish("cycle", "The estimates entered a repeating cycle before convergence.")
        seen.add(next_x)
        x, fx = next_x, next_fx
    return finish("iteration_limit", "The iteration limit was reached before the stopping criteria were met.")


def fixed_point(
    f: ScalarFunction,
    g: ScalarFunction,
    x0: float,
    *,
    x_tolerance: float = 1e-6,
    residual_tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> SolveResult:
    """Apply x[n+1] = g(x[n]); check the residual against the original f."""
    return _iterate(
        f, lambda x, _: _finite_call(g, x), x0,
        x_tolerance, residual_tolerance, max_iterations, "Fixed Point Iteration",
    )


def newton_raphson(
    f: ScalarFunction,
    derivative: ScalarFunction,
    x0: float,
    *,
    x_tolerance: float = 1e-6,
    residual_tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> SolveResult:
    """Apply x[n+1] = x[n] - f(x[n])/f'(x[n])."""
    def update(x: float, fx: float) -> float:
        slope = _finite_call(derivative, x)
        if slope == 0.0:
            raise _ZeroDerivativeError("Newton–Raphson cannot continue because f'(x) is zero.")
        return x - fx / slope

    return _iterate(
        f, update, x0,
        x_tolerance, residual_tolerance, max_iterations, "Newton–Raphson",
    )
