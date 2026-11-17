# ITERAROOT: AN INTERACTIVE ROOT-FINDING TOOL USING FIXED POINT ITERATION AND NEWTON–RAPHSON

## Team members

To be completed by the group in the required format: Last Name, First Name Middle Initial.

## Project overview

IteraRoot is an interactive application that approximates the real roots of user-defined functions using Fixed Point Iteration and Newton–Raphson. Fixed Point Iteration rewrites the equation `f(x)=0` as `x=g(x)` and repeatedly evaluates the iteration function. Newton–Raphson uses the function and its first derivative to update a starting estimate through the tangent-line formula.

The application automates repeated calculations while preserving a visible record of every iteration. Users provide the function, initial guess, tolerances, and maximum number of iterations; they also provide the rearranged function for Fixed Point Iteration. IteraRoot computes the Newton derivative symbolically, displays each method's result and stopping reason, and plots the original function and successive estimates. A comparison mode lets users examine both methods under the same starting conditions.

## Objectives

1. Implement Fixed Point Iteration and Newton–Raphson for approximating roots of polynomial and supported non-polynomial functions.
2. Accept user-defined functions, iteration functions, starting estimates, and stopping settings through an accessible interface.
3. Display the root estimate, residual, iteration count, and calculation history for each method.
4. Illustrate the function and progression of estimates through graphical output.
5. Compare convergence behavior and clearly report unsuccessful calculations.

## Features

- Individual-method and comparison modes.
- Polynomial expressions and common elementary functions.
- Automatic first derivative for Newton–Raphson.
- Explicit `g(x)` input and a local derivative diagnostic for Fixed Point Iteration.
- User-controlled step tolerance, residual tolerance, and iteration limit.
- Iteration tables with CSV download.
- Function and estimate-history graphs.
- Built-in examples showing successful and unsuccessful convergence.
- Clear handling of zero derivatives, domain errors, cycles, stagnation, and iteration limits.

## Implementation

Python provides the numerical routines, SymPy provides symbolic differentiation, Streamlit provides the interface, and Plotly provides interactive graphs. The numerical methods are implemented explicitly in the project's own solver module.
