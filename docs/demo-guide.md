# Demonstration Guide

## 1. Introduce the problem

"Our project approximates roots of equations using Fixed Point Iteration and Newton–Raphson. It shows each calculation so users can inspect how the estimate changes."

## 2. Run the polynomial example

1. Load **Cubic polynomial**.
2. Explain `f(x)=x^3+x-1` and its rearrangement `g(x)=1/(1+x^2)`.
3. Use the shared initial guess `x0=0.5` and default tolerances.
4. Run **Compare both**.
5. Confirm that both estimates approach approximately `0.6823278038`.
6. Explain that the update rule, rather than the graph interval, controls the iterations.

The first fixed point update is `g(0.5)=0.8`. The first Newton update is `0.5 - (-0.375/1.75) = 0.7142857142857143`.

## 3. Explain the outputs

- The approximate root is the final estimate after successful stopping.
- The residual is the magnitude of the original `f(x)` at that estimate.
- The absolute step is the change from the preceding estimate; it is not the true root error.
- Row 0 is the starting guess, so it is excluded from the iteration count.
- Both stopping tolerances normally need to be met, or a computed function value must equal zero.

## 4. Inspect tables and graphs

Open **Iteration tables**, identify the first updates, and download a CSV. In **Graphs**, show the function's zero crossing and each method's progression.

## 5. Demonstrate a failure clearly

Load **Newton zero derivative**. The initial guess is zero for `f(x)=x^2-2`, so Newton's derivative is zero and the method stops with a clear explanation. Fixed Point Iteration uses its separate update function and can still converge in this example.

Optionally load **Fixed point divergence** to show that equivalent rearrangements can behave differently. Do not imply every rearrangement or starting point converges.

## Questions to prepare for

- Why do we need `g(x)` for fixed point iteration?
- Why is Newton's method a special type of fixed point iteration?
- What happens when the derivative is zero?
- Can an iteration stop changing without finding a root?
- What is the difference between residual, approximate step, and true root error?
- Why does a derivative magnitude below one at a single point not prove convergence on an interval?
- Can different starting guesses lead to different roots?
