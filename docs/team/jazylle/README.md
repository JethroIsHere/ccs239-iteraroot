# Jazylle | Numerical validation and class demo

Check that the numbers the class sees in the tables and graphs agree with an independent calculation. Use those checks to prepare the group’s walkthrough.

## Tasks

- [ ] Independently work out the first three **updates** of each method for `f(x) = x^3 + x - 1`, starting at `x₀ = 0.5`. Use `g(x) = 1/(1 + x^2)` for Fixed Point Iteration and `f′(x) = 3x^2 + 1` for Newton–Raphson. Keep extra digits between updates. Row 0 is the starting guess.
- [ ] Run **Compare both** with step tolerance `1e-6`, residual tolerance `1e-8`, and an iteration limit of `100`. Record the method, update number, hand-calculated estimate, app estimate, and difference. Check both final estimates and update counts. After integration, check the new plots against the same rows.
- [ ] Run one failure case per method. **Fixed point divergence** should stop without claiming a root. **Newton zero derivative** should stop at the initial guess with zero updates. Record what the app actually displays for each case.
- [ ] Add your comparison and findings to the [validation record](../../validation.md). Update the [demo guide](../../demo-guide.md) with the final button names and a short walkthrough from loading the cubic to showing a failure case.

## Demo and handoff

Give Jethro the completed comparison and walkthrough. A group member should be able to reproduce both methods approaching `0.6823278`, explain the **39 versus 4** updates for these settings, and demonstrate a failure using the guide alone. If a value differs, include the inputs and row number so the team can reproduce it.

See the [classroom examples](../../../iteraroot/examples.py) and [team assignments](../../../README.md#group-collaboration).
