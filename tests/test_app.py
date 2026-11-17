"""Exercise actual Streamlit form and result behavior without a browser."""

from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def run_calculation(app):
    next(button for button in app.button if button.label == "Run calculation").click()
    return app.run()


class ApplicationTests(unittest.TestCase):
    def start(self):
        app = AppTest.from_file(str(APP), default_timeout=20).run()
        self.assertFalse(app.exception)
        return app

    def test_compare_mode_displays_two_converged_results_and_tables(self):
        app = run_calculation(self.start())
        self.assertFalse(app.exception)
        self.assertEqual(len(app.success), 2)
        self.assertEqual(len(app.dataframe), 2)
        self.assertTrue(all(result.converged for result in app.session_state["run"]["results"]))

    def test_newton_mode_does_not_require_a_valid_g(self):
        app = self.start()
        app.radio(key="method").set_value("Newton–Raphson")
        app.text_input(key="g_source").set_value("invalid")
        app = run_calculation(app)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.success), 1)
        self.assertEqual(len(app.session_state["run"]["results"]), 1)

    def test_invalid_new_input_clears_old_results(self):
        app = run_calculation(self.start())
        app.text_input(key="f_source").set_value("__import__('os')")
        app = run_calculation(app)
        self.assertFalse(app.exception)
        self.assertGreater(len(app.error), 0)
        self.assertNotIn("run", app.session_state)

    def test_load_example_and_show_newton_failure(self):
        app = self.start()
        app.selectbox(key="example_name").select("Newton zero derivative")
        next(button for button in app.button if button.label == "Load example").click()
        app.run()
        app = run_calculation(app)
        self.assertFalse(app.exception)
        results = app.session_state["run"]["results"]
        self.assertTrue(results[0].converged)
        self.assertEqual(results[1].status, "zero_derivative")


if __name__ == "__main__":
    unittest.main()
