# Kurt | Interface redesign

Give a first-time visitor a way to see both methods in action before filling out the equation form. Own the Streamlit layout and theme. Jethro will connect Christine’s cobweb plot and Duke’s tangent plot to the finished interface.

## Tasks

- [ ] Put a **Try the cubic example** action on the opening screen. One click should load the example, run both methods, and show their results. Keep a clear path for users who want to enter their own equation.
- [ ] Make the graph the focus of the results view. Give each method a consistent color plus a written label or distinct marker. Show the root estimate, iteration count, and convergence status together for each method.
- [ ] Show the two results side by side on desktop and stack them on a phone. Keep the equation, graph axes, iteration controls, and table readable at both sizes.
- [ ] Check that custom inputs, single-method runs, error messages, and CSV downloads are still easy to find. Share the method colors and labels with Christine and Duke so the three views match.

## Demo and handoff

From a fresh session, click **Try the cubic example**. The comparison should show a root near `0.6823278`, with **39 fixed point updates** and **4 Newton updates** at the example’s default tolerances. Send Jethro the implemented layout and one desktop and one phone-width screenshot of that result.

Start with the [current interface](../../../app.py), [theme settings](../../../.streamlit/config.toml), and [app tests](../../../tests/test_app.py). [Team assignments](../../../README.md#group-collaboration)
