
"""Interactive Fixed Point Iteration cobweb visualization.

Uses the existing SolveResult.history so the graphical steps
match the numerical iteration table exactly.
"""

import math
from typing import Callable

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from iteraroot.solvers import SolveResult


# Default colors, adjustable to Kurt's final interface design.
CURVE_COLOR = "#087e8b"
DIAGONAL_COLOR = "#8796a5"
STEP_COLOR = "#d67b21"
PREVIOUS_COLOR = "#b3c7cd"


def cobweb_segments(result: SolveResult, step: int):
    """Return the path coordinates through the selected update.

    Each update contains:
    - A vertical move to y = g(x)
    - A horizontal move to the diagonal y = x

    The first update begins at (x0, 0).
    """
    completed = min(max(int(step), 0), result.iterations)
    segments = []

    for n in range(1, completed + 1):
        previous_x = result.history[n - 1].x
        next_x = result.history[n].x

        starting_y = 0.0 if n == 1 else previous_x

        x_points = [previous_x, previous_x, next_x]
        y_points = [starting_y, next_x, next_x]

        segments.append((x_points, y_points))

    return segments


def make_cobweb_figure(
    g: Callable[[float], float],
    result: SolveResult,
    step: int,
    left: float,
    right: float,
) -> go.Figure:
    """Create the cobweb graph for the selected number of updates."""

    completed = min(max(int(step), 0), result.iterations)

    # Include the selected estimates in the visible plotting range.
    estimates = [row.x for row in result.history[:completed + 1]]
    extent = [float(left), float(right), 0.0, *estimates]

    lower = min(extent)
    upper = max(extent)
    padding = max((upper - lower) * 0.07, 0.1)

    lower -= padding
    upper += padding

    # Sample the user's iteration function.
    xs = np.linspace(lower, upper, 600)
    ys = []

    for x in xs:
        try:
            value = float(g(float(x)))
            ys.append(value if math.isfinite(value) else None)
        except (ArithmeticError, ValueError, TypeError):
            ys.append(None)

    fig = go.Figure()

    # Curve 1: y = g(x)
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            name="y = g(x)",
            line=dict(color=CURVE_COLOR, width=3),
            connectgaps=False,
        )
    )

    # Curve 2: y = x
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=xs,
            mode="lines",
            name="y = x",
            line=dict(
                color=DIAGONAL_COLOR,
                width=2,
                dash="dash",
            ),
        )
    )

    if result.history:
        x0 = result.history[0].x

        # Show the initial guess on the x-axis.
        fig.add_trace(
            go.Scatter(
                x=[x0],
                y=[0.0],
                mode="markers",
                name="Initial guess",
                marker=dict(
                    color=STEP_COLOR,
                    size=11,
                    symbol="circle",
                ),
            )
        )

    segments = cobweb_segments(result, completed)

    # Draw earlier updates as a single faint trace.
    if len(segments) > 1:
        old_x = []
        old_y = []

        for x_points, y_points in segments[:-1]:
            old_x.extend(x_points + [None])
            old_y.extend(y_points + [None])

        fig.add_trace(
            go.Scatter(
                x=old_x,
                y=old_y,
                mode="lines",
                name="Previous updates",
                line=dict(color=PREVIOUS_COLOR, width=2),
                connectgaps=False,
            )
        )

    # Highlight the currently selected update.
    if segments:
        current_x, current_y = segments[-1]

        fig.add_trace(
            go.Scatter(
                x=current_x,
                y=current_y,
                mode="lines+markers",
                name=f"Step {completed}",
                line=dict(color=STEP_COLOR, width=4),
                marker=dict(color=STEP_COLOR, size=9),
            )
        )

    fig.update_layout(
        title=f"Fixed Point Cobweb — Step {completed}",
        template="plotly_white",
        height=520,
        xaxis=dict(
            title="x",
            range=[lower, upper],
            zeroline=False,
        ),
        yaxis=dict(
            title="y",
            range=[lower, upper],
            scaleanchor="x",
            scaleratio=1,
        ),
        legend=dict(orientation="h"),
        margin=dict(l=30, r=20, t=60, b=30),
        hovermode="closest",
    )

    return fig


def render_cobweb(
    g: Callable[[float], float],
    result: SolveResult,
    left: float,
    right: float,
    key: str = "fixed_point_cobweb",
) -> None:
    """Display the interactive cobweb plot in Streamlit."""

    if not result.history:
        st.warning(
            "No valid initial estimate is available to visualize."
        )
        return

    maximum = result.iterations
    state_key = f"{key}_selected_step"

    selected = int(st.session_state.get(state_key, 0))
    selected = min(max(selected, 0), maximum)

    previous_col, next_col = st.columns(2)

    with previous_col:
        if st.button(
            "← Previous step",
            disabled=selected == 0,
            key=f"{key}_previous",
        ):
            selected -= 1

    with next_col:
        if st.button(
            "Next step →",
            disabled=selected >= maximum,
            key=f"{key}_next",
        ):
            selected += 1

    st.session_state[state_key] = selected

    st.markdown(f"**Completed updates: {selected} of {maximum}**")

    if selected == 0:
        initial = result.history[0].x

        st.info(
            f"Starting state: x₀ = {initial:.10f}. "
            "No updates have been displayed yet."
        )

    else:
        previous_x = result.history[selected - 1].x
        current_x = result.history[selected].x

        st.write(
            f"**Step {selected}:** "
            f"x_{selected - 1} = {previous_x:.10f} → "
            f"x_{selected} = {current_x:.10f}"
        )

        st.latex(
            rf"x_{{{selected}}} = "
            rf"g(x_{{{selected - 1}}}) = "
            rf"{current_x:.10g}"
        )

        st.caption(
            "Vertical: evaluate g(x) at the previous estimate. "
            "Horizontal: move to y = x so the result becomes "
            "the input for the next update."
        )

    figure = make_cobweb_figure(
        g=g,
        result=result,
        step=selected,
        left=left,
        right=right,
    )

    st.plotly_chart(figure, width="stretch")
