# ITERAROOT: AN INTERACTIVE ROOT-FINDING TOOL USING FIXED POINT ITERATION AND NEWTON–RAPHSON

CCS 239 — Optimization Theory and Application · Final-term group project

IteraRoot is a Python and Streamlit application for learning and comparing **Fixed Point Iteration (#3)** and **Newton–Raphson for Root-finding (#6)**. It accepts a function, starting guess, and tolerances, computes the iterations explicitly, and displays root estimates, tables, and graphs.

## Current starter

- Run either method individually or compare both on the same original equation.
- Enter polynomial expressions or supported functions such as `sin(x)`, `cos(x)`, and `exp(x)`.
- Provide an explicit iteration function `g(x)` for Fixed Point Iteration.
- Calculate `f'(x)` symbolically for Newton–Raphson.
- Set the initial guess, separate step/residual tolerances, and iteration limit.
- Display iteration count, approximate root or last valid estimate, residual, and stopping reason.
- Inspect iteration tables and download them as CSV.
- Plot the function and final estimates, and follow the estimates across iterations.
- Try convergent examples, fixed-point divergence, and Newton's zero-derivative case.

## Run locally

Use Python **3.11 or 3.12**. Python 3.12 is used by the automated checks.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# WSL / Linux / macOS
source .venv/bin/activate
```

Then install and start:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address printed by Streamlit. A hosted app has not been deployed as part of this starter.

If PowerShell blocks activation, use the virtual environment directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## First demonstration

Choose **Cubic polynomial**, press **Load example**, then **Run calculation**.

| Input | Value |
| --- | --- |
| Original function | `x^3 + x - 1` |
| Fixed point function | `1/(1 + x^2)` |
| Initial guess | `0.5` |
| Step tolerance | `1e-6` |
| Residual tolerance | `1e-8` |
| Iteration limit | `100` |
| Expected root | Approximately `0.6823278038` |

The iteration function is a deliberate rearrangement of this equation. IteraRoot does not claim that an arbitrary `g(x)` is equivalent to the original `f(x)`.

## Calculation policy

Ordinary Fixed Point Iteration uses `x[n+1] = g(x[n])`. Newton–Raphson uses `x[n+1] = x[n] - f(x[n])/f'(x[n])`. The method implementations are in `iteraroot/solvers.py`; they do not call an off-the-shelf root solver.

The normal stopping criteria are **both**:

1. `abs(x[n] - x[n-1]) <= step_tolerance`
2. `abs(f(x[n])) <= residual_tolerance`

If `f(x)` evaluates to exactly zero in floating-point arithmetic, the iteration also stops successfully. Row 0 is the initial guess and is not counted as a completed iteration. An initially exact root takes zero iterations.

The displayed absolute step is an approximate change in successive estimates, not a bound on the true root error. A small residual alone cannot guarantee a small root error for an ill-conditioned equation.

The program reports zero derivatives, invalid real-domain values, non-finite calculations, repeating cycles, stagnation, and the iteration limit. Unsuccessful results are labeled **last valid estimate**, not approximate root.

For Fixed Point Iteration, `|g'(x0)|` is displayed only as a local hint. A convergence guarantee requires suitable assumptions on a whole interval, including an invariant interval and a contraction bound. Neither solver is guaranteed to converge from every initial guess.

## Expression syntax

Use explicit multiplication (`2*x`) and either `^` or `**` for powers. Supported names are `x`, `pi`, `e`, `E`, `sin`, `cos`, `tan`, `exp`, `log`, `ln`, and `sqrt`. Only real finite values are accepted. Negative arguments to fractional powers may be outside the supported real evaluation domain.

A restricted AST parser constructs the mathematics explicitly. Raw user input is not passed to `eval`, `sympify`, or `parse_expr`. Input complexity is bounded. This is a classroom starter, not a resource-isolated service for hostile public workloads.

## Checks

```bash
python -m unittest discover -s tests -v
```

The suite checks known roots, initial roots, actual update values, iteration counts, incorrect iteration functions, cycles, failed convergence, zero derivatives, real-domain errors, restricted expression parsing, and the Streamlit form/results flow.

## Layout

```text
app.py                     Streamlit interface and graphs
iteraroot/expressions.py     Restricted parser and symbolic differentiation
iteraroot/solvers.py         Fixed point and Newton–Raphson iterations
iteraroot/examples.py        Classroom examples
tests/                    Numerical, parser, and application checks
docs/project-brief.md      Requirements and rubric mapping
docs/project-overview.md   Overview and objectives draft
docs/demo-guide.md         Suggested demonstration
docs/validation.md         Recorded local checks
```

## Group collaboration

Jethro coordinates integration and the final demo. Each member’s README lists the work they own, a check they can run, and what to hand over.

| Member | Assignment |
| --- | --- |
| Kurt | [Redesign the Streamlit interface for desktop and mobile](docs/team/kurt/README.md) |
| Christine | [Build the step-through Fixed Point Iteration cobweb plot](docs/team/christine/README.md) |
| Duke | [Build the step-through Newton–Raphson tangent plot](docs/team/duke/README.md) |
| Jazylle | [Verify numerical results and prepare the class demo](docs/team/jazylle/README.md) |

## References

- [Berkeley numerical analysis notes: fixed point and Newton's method](https://persson.berkeley.edu/math128a/lecture_notes/math128a_lecture_notes_chapter_2.html)
- [Streamlit documentation](https://docs.streamlit.io/)
- [SymPy differentiation documentation](https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html)

This starter implements the selected methods for root-finding. Newton–Raphson for optimization (#7) is outside the chosen pair.
