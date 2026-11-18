# Christine | Fixed Point Iteration cobweb plot

Build a step-through plot that shows how applying `g(x)` to the current estimate produces the next one.

## Tasks

- [ ] Draw the iteration function `y = g(x)` and the diagonal `y = x` on the same axes. Label both curves.
- [ ] Use successive entries in `SolveResult.history`. For the first update, start at `(x₀, 0)`, move vertically to `(x₀, x₁)`, then horizontally to `(x₁, x₁)`. Each later step starts on the diagonal.
- [ ] Let the viewer move forward and backward through completed updates. Label the selected step and its two estimates so Jazylle can check them against the iteration table. If there are zero updates, show the starting state.
- [ ] Put the plot in its own module, such as `iteraroot/cobweb.py`. Use the fixed point style agreed with Kurt. Give Jethro the module and a short example of how to display it.

## Demo and handoff

Load **Cubic polynomial** with `g(x) = 1/(1 + x^2)` and `x₀ = 0.5`. Step 1 must travel from `(0.5, 0)` to `(0.5, 0.8)` and then to `(0.8, 0.8)`. Step forward once more and check the displayed estimate against row 2 of the table. During the demo, explain why each horizontal segment ends on the diagonal.

Start with the [solver history](../../../iteraroot/solvers.py) and [classroom examples](../../../iteraroot/examples.py). [Team assignments](../../../README.md#group-collaboration)
