# Duke | Newton–Raphson tangent plot

Build a step-through plot that shows why Newton’s next estimate is the point where a tangent crosses the x-axis.

## Tasks

- [ ] Plot `y = f(x)` and the x-axis. At the selected estimate `xₙ`, mark `(xₙ, f(xₙ))` and draw the tangent using the derivative already calculated by the app.
- [ ] Mark the tangent’s x-intercept as `(xₙ₊₁, 0)`. Use the current and next entries in `SolveResult.history` to keep the step labels and iteration table in sync.
- [ ] Let the viewer move forward and backward through completed updates. When a zero derivative stops the method, show the point, horizontal tangent, and stopping reason. Only draw a next-estimate marker when the solver produced an update.
- [ ] Put the plot in its own module, such as `iteraroot/newton_plot.py`. Use the Newton style agreed with Kurt. Give Jethro the module and a short example of how to display it.

## Demo and handoff

For **Cubic polynomial** with `f(x) = x^3 + x - 1` and `x₀ = 0.5`, the first tangent touches the curve at `(0.5, -0.375)`, has slope `1.75`, and crosses the x-axis near `0.7142857143`. Then load **Newton zero derivative**. At `x₀ = 0` the tangent to `x^2 - 2` is horizontal at `y = -2`, and the table reports zero updates.

Start with the [solver history](../../../iteraroot/solvers.py), [expression and derivative code](../../../iteraroot/expressions.py), and [classroom examples](../../../iteraroot/examples.py). [Team assignments](../../../README.md#group-collaboration)
