"""Run with: python -m streamlit run app.py"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from iteraroot.examples import EXAMPLES
from iteraroot.expressions import EvaluationError, ExpressionError, X, parse_expression
from iteraroot.solvers import SolveResult, fixed_point, newton_raphson
from iteraroot.cobweb import render_cobweb  

st.set_page_config(page_title="IteraRoot | CCS 239", page_icon="📐", layout="wide")


def load_example() -> None:
    example = EXAMPLES[st.session_state["example_name"]]
    for key, value in {
        "f_source": example["f"], "g_source": example["g"],
        "x0": example["x0"], "plot_left": example["left"], "plot_right": example["right"],
    }.items():
        st.session_state[key] = value
    st.session_state.pop("run", None)


for key, value in {
    "f_source": EXAMPLES["Cubic polynomial"]["f"],
    "g_source": EXAMPLES["Cubic polynomial"]["g"],
    "x0": 0.5, "plot_left": -1.0, "plot_right": 2.0,
}.items():
    st.session_state.setdefault(key, value)

st.caption("CCS 239 · OPTIMIZATION THEORY AND APPLICATION")
st.title("IteraRoot")
st.markdown("**Fixed Point Iteration and Newton–Raphson**, step by step.")
st.write("Enter an equation, follow the iterations, and compare how the two methods approach a root.")

with st.expander("Load a classroom example"):
    st.selectbox("Example", list(EXAMPLES), key="example_name")
    st.button("Load example", on_click=load_example)

with st.form("solver_form"):
    method = st.radio(
        "Method", ["Compare both", "Fixed Point Iteration", "Newton–Raphson"],
        horizontal=True, key="method",
    )
    function_col, settings_col = st.columns([1.5, 1])
    with function_col:
        st.text_input("Function f(x)", key="f_source", help="Enter the expression whose root you want: f(x)=0.")
        st.text_input(
            "Iteration function g(x)", key="g_source",
            help="Used for Fixed Point Iteration. Rearrange f(x)=0 into x=g(x). Enter g(x) only.",
        )
        st.caption("Use explicit multiplication: 2*x. Powers: x^2 or x**2. Functions: sin, cos, tan, exp, log, sqrt.")
        st.number_input("Initial guess x₀", key="x0", format="%.8f")
        left_col, right_col = st.columns(2)
        left_col.number_input("Graph left endpoint", key="plot_left", format="%.4f")
        right_col.number_input("Graph right endpoint", key="plot_right", format="%.4f")
        st.caption("The graph interval controls the plot; these methods start from x₀ and do not require a bracket.")
    with settings_col:
        x_tolerance = st.number_input(
            "Absolute step tolerance", min_value=1e-12, max_value=1.0,
            value=1e-6, format="%.1e", key="x_tolerance",
        )
        residual_tolerance = st.number_input(
            "Residual tolerance |f(x)|", min_value=1e-12, max_value=1.0,
            value=1e-8, format="%.1e", key="residual_tolerance",
        )
        max_iterations = st.number_input(
            "Maximum iterations", min_value=1, max_value=1000,
            value=100, step=1, key="max_iterations",
        )
        st.info("Normally, both tolerances must be met. A computed f(x)=0 also ends the iteration.")
    submitted = st.form_submit_button("Run calculation", type="primary")

if submitted:
    st.session_state.pop("run", None)
    try:
        if not st.session_state.plot_left < st.session_state.plot_right:
            raise ValueError("The graph left endpoint must be less than the right endpoint.")
        if not all(math.isfinite(st.session_state[k]) for k in ("plot_left", "plot_right")):
            raise ValueError("Graph endpoints must be finite.")
        f = parse_expression(st.session_state.f_source)
        if X not in f.expression.free_symbols:
            raise ValueError("The function f(x) must contain the variable x.")
        g = parse_expression(st.session_state.g_source) if method != "Newton–Raphson" else None
        derivative = f.derivative() if method != "Fixed Point Iteration" else None
        settings = dict(
            x_tolerance=x_tolerance, residual_tolerance=residual_tolerance,
            max_iterations=int(max_iterations),
        )
        results = []
        if g is not None:
            results.append(fixed_point(f, g, st.session_state.x0, **settings))
        if derivative is not None:
            results.append(newton_raphson(f, derivative, st.session_state.x0, **settings))
        st.session_state.run = {
            "f": f, "g": g, "derivative": derivative, "results": results,
            "left": st.session_state.plot_left, "right": st.session_state.plot_right,
            "x0": st.session_state.x0, "settings": settings,
        }
    except (ExpressionError, EvaluationError, ArithmeticError, ValueError, TypeError) as exc:
        st.error(str(exc))


def history_frame(result: SolveResult) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "Iteration": row.iteration, "xₙ": row.x, "f(xₙ)": row.fx,
            "Residual |f(xₙ)|": row.residual, "Absolute step": row.absolute_step,
            "Relative step (%)": row.relative_step_percent,
        }
        for row in result.history
    ])


if "run" in st.session_state:
    run = st.session_state.run
    st.divider()
    st.subheader("Results")
    st.latex(r"f(x)=" + run["f"].latex)
    if run["g"] is not None:
        st.latex(r"g(x)=" + run["g"].latex)
    if run["derivative"] is not None:
        st.latex(r"f'(x)=" + run["derivative"].latex)
    st.caption(
        f"Submitted x₀ = {run['x0']:g} · step tolerance = {run['settings']['x_tolerance']:.1e} · "
        f"residual tolerance = {run['settings']['residual_tolerance']:.1e}. "
        "Press Run calculation after changing the form to update these results."
    )

    for column, result in zip(st.columns(len(run["results"])), run["results"]):
        with column:
            st.markdown(f"#### {result.method}")
            if result.converged:
                st.success("Converged")
            else:
                st.warning("Stopped without convergence")
            st.metric(
                "Approximate root" if result.converged else "Last valid estimate",
                f"{result.estimate:.10g}" if result.estimate is not None else "Unavailable",
            )
            a, b = st.columns(2)
            a.metric("Iterations", result.iterations)
            b.metric("Residual |f(x)|", f"{result.residual:.3e}" if result.residual is not None else "Unavailable")
            st.caption(result.message)

    if run["g"] is not None:
        with st.expander("Fixed point convergence check"):
            try:
                dg = run["g"].derivative()
                slope = abs(dg(run["x0"]))
                st.latex(r"g'(x)=" + dg.latex)
                st.write(f"At the starting point, |g′(x₀)| = {slope:.6g}.")
                st.caption(
                    "A value below 1 at one point is a local hint, not a convergence guarantee. "
                    "A contraction guarantee needs a derivative bound below 1 throughout an invariant interval. "
                    "The residual is always checked against your original f(x)."
                )
            except (ExpressionError, EvaluationError, ArithmeticError, ValueError, TypeError):
                st.info("The derivative of g(x) could not be evaluated at this starting point. The iteration results remain available.")

    graph_tab, table_tab, guide_tab = st.tabs(["Graphs", "Iteration tables", "Method guide"])
    with graph_tab:

         # ==============================================
    # CHRISTINE: FIXED POINT COBWEB VISUALIZATION
    # ==============================================

        fixed_result = next(
        (
            result
            for result in run["results"]
            if result.method == "Fixed Point Iteration"
        ),
        None,
    )

    if fixed_result is not None and run["g"] is not None:
        st.markdown("### Fixed Point Iteration — Cobweb Visualization")

        render_cobweb(
            g=run["g"],
            result=fixed_result,
            left=run["left"],
            right=run["right"],
        )

        xs = np.linspace(run["left"], run["right"], 600)
        ys = []
        for value in xs:
            try:
                ys.append(run["f"](float(value)))
            except (EvaluationError, ArithmeticError, ValueError, TypeError):
                ys.append(None)
        figure = go.Figure(go.Scatter(x=xs, y=ys, name="f(x)", line=dict(color="#087e8b", width=3), connectgaps=False))
        figure.add_hline(y=0, line_color="#8796a5", line_dash="dot")
        figure.add_vline(x=run["x0"], line_color="#b0b9c2", line_dash="dash")
        colors = ["#d67b21", "#6b52ae"]
        for color, result in zip(colors, run["results"]):
            if result.history and run["left"] <= result.history[-1].x <= run["right"]:
                final = result.history[-1]
                figure.add_trace(go.Scatter(
                    x=[final.x], y=[final.fx], mode="markers", name=result.method,
                    marker=dict(size=12, color=color, symbol="circle" if result.converged else "x"),
                ))
        figure.update_layout(
            title="Function and final estimates", xaxis_title="x", yaxis_title="f(x)",
            template="plotly_white", margin=dict(l=20, r=20, t=60, b=20),
            xaxis_range=[run["left"], run["right"]], legend=dict(orientation="h"),
        )
        st.plotly_chart(figure, width="stretch")
        if any(r.estimate is not None and not run["left"] <= r.estimate <= run["right"] for r in run["results"]):
            st.info("A final estimate lies outside the graph interval. Adjust the graph endpoints and run again to see it.")
        progress = go.Figure()
        for color, result in zip(colors, run["results"]):
            progress.add_trace(go.Scatter(
                x=[r.iteration for r in result.history], y=[r.x for r in result.history],
                mode="lines+markers", name=result.method, line=dict(color=color),
            ))
        progress.update_layout(
            title="Estimate at each iteration", xaxis_title="Iteration", yaxis_title="xₙ",
            template="plotly_white", margin=dict(l=20, r=20, t=60, b=20),
            legend=dict(orientation="h"),
        )
        st.plotly_chart(progress, width="stretch")
        st.caption("The graph samples 600 points. Domain errors appear as gaps; sampling may miss discontinuities.")
    with table_tab:
        st.caption(
            "Row 0 is the initial guess and is not counted as an iteration. Absolute step is |xₙ−xₙ₋₁|, "
            "not the unknown true root error. Relative step is unavailable when xₙ=0."
        )
        for result in run["results"]:
            st.markdown(f"#### {result.method}")
            frame = history_frame(result)
            st.dataframe(frame, hide_index=True, width="stretch")
            st.download_button(
                f"Download {result.method} table", frame.to_csv(index=False).encode("utf-8"),
                file_name="fixed-point-iterations.csv" if result.method == "Fixed Point Iteration" else "newton-raphson-iterations.csv",
                mime="text/csv",
            )
    with guide_tab:
        st.markdown("**Fixed Point Iteration** rewrites an equation as x=g(x), then uses the previous estimate as the next input.")
        st.latex(r"x_{n+1}=g(x_n)")
        st.markdown("**Newton–Raphson** uses the tangent at the current estimate to produce the next estimate. Its derivative is calculated symbolically.")
        st.latex(r"x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}")
        st.write(
            "Each solver stops when both the absolute step and residual tolerances are met, "
            "or when f(x) evaluates to zero. A zero derivative, repeating cycle, invalid real-domain "
            "value, or iteration limit produces an explicit non-convergence result."
        )
        st.caption(
            "Neither method is guaranteed to converge from every starting point. "
            "Different iteration functions or starting guesses can produce different outcomes. "
            "A small residual does not by itself bound the distance to the true root."
        )
else:
    st.info("Start with the cubic example above, or enter your own function and iteration function, then run the calculation.")

st.divider()
st.caption("ITERAROOT · CCS 239 FINAL-TERM PROJECT · Fixed Point Iteration + Newton–Raphson for Root-finding")
