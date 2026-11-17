"""Small classroom examples with explicitly chosen iteration functions."""

EXAMPLES = {
    "Cubic polynomial": {
        "f": "x^3 + x - 1", "g": "1/(1 + x^2)",
        "x0": 0.5, "left": -1.0, "right": 2.0,
    },
    "Square root of two": {
        "f": "x^2 - 2", "g": "(x + 2)/(x + 1)",
        "x0": 1.0, "left": 0.0, "right": 2.5,
    },
    "Cosine equation": {
        "f": "cos(x) - x", "g": "cos(x)",
        "x0": 0.5, "left": -1.0, "right": 2.0,
    },
    "Fixed point divergence": {
        "f": "x^2 - 2", "g": "x^2 + x - 2",
        "x0": 1.5, "left": 0.0, "right": 2.5,
    },
    "Newton zero derivative": {
        "f": "x^2 - 2", "g": "(x + 2)/(x + 1)",
        "x0": 0.0, "left": -2.5, "right": 2.5,
    },
}
