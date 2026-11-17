# Starter Validation

Local validation performed November 17, 2026. This record describes the prepared starter, not a deployed service or a remote GitHub Actions run.

## Environment

| Component | Version |
| --- | --- |
| Python | 3.12.14 |
| Streamlit | 1.67.0 |
| SymPy | 1.14.0 |
| NumPy | 2.3.5 |
| pandas | 2.2.3 |
| Plotly | 6.9.0 |

Direct dependencies are pinned to these tested versions in `requirements.txt`. Transitive dependencies are resolved by pip.

## Automated checks

Command: `python -m unittest discover -s tests -v`

Result: **25 tests passed**, including four Streamlit AppTest scenarios. The application tests run the actual form submission and inspect resulting states and tables; they do not replace live visual review on the group's own devices.

The Streamlit server was also started in headless mode; its local health endpoint returned **HTTP 200, `ok`**, after which the smoke-test server was stopped. Python compilation and the staged Git whitespace check passed.

Coverage includes known roots, actual first updates, row-0 counting, exact initial roots, small nonzero derivatives, zero derivatives, cycles, incorrect iteration functions, small steps with a large residual, domain errors, non-finite values, iteration limits, parser restrictions, comparison results, example loading, and clearing stale results after invalid input.

## Numerical examples

Settings: absolute step tolerance `1e-6`, residual tolerance `1e-8`, maximum `100` iterations. Counts exclude row 0. The exact-zero floating-point stopping rule can end a run even when the final step is larger than the step tolerance.

| Function | g(x) | x0 | Method | Updates | Final estimate | Residual |
| --- | --- | --- | --- | --- | --- | --- |
| `x^3+x-1` | `1/(1+x^2)` | 0.5 | Fixed Point | 39 | 0.6823278075761247 | 8.9831e-9 |
| `x^3+x-1` | — | 0.5 | Newton–Raphson | 4 | 0.6823278038283471 | 7.8559e-13 |
| `x^2-2` | `(x+2)/(x+1)` | 1.0 | Fixed Point | 11 | 1.4142135642135643 | 5.2056e-9 |
| `x^2-2` | — | 1.0 | Newton–Raphson | 5 | 1.4142135623730951 | 4.4409e-16 |
| `cos(x)-x` | `cos(x)` | 0.5 | Fixed Point | 44 | 0.7390851272464174 | 9.9894e-9 |
| `cos(x)-x` | — | 0.5 | Newton–Raphson | 4 | 0.7390851332151607 | 0 in floating-point arithmetic |

## Failure demonstrations

- Newton applied to `x^2-2` from `x0=0` reports a zero derivative and performs zero updates.
- Newton applied to `x^3-2*x+2` from `x0=0` detects the cycle `0 → 1 → 0`.
- Fixed point with `f(x)=x-1`, `g(x)=0`, and `x0=2` stops as stagnated rather than falsely accepting the unrelated fixed point.
- A non-converging update reaches the iteration limit without labeling its last estimate as a root.
- The divergent built-in polynomial iteration eventually exceeds real finite numeric evaluation limits and reports failure.

## Pending review

The group still needs to confirm the instructor's preferred error convention, add team member details, and review the interface on its presentation device. The test results above are from the local starter. Results for later commits are available in [GitHub Actions](https://github.com/JethroIsHere/ccs239-iteraroot/actions).
