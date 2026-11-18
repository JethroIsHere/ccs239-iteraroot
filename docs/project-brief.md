# CCS 239 Project Brief

## Chosen methods

- #3: Fixed Point Iteration
- #6: Newton–Raphson for Root-finding

The user confirmed this pair and reported that combining methods is permitted. The photographed assignment originally says to choose one method and does not explicitly document combined-method rules; the group should follow the instructor's actual approval.

## Source

Requirements transcribed from the assignment screenshots supplied on November 17, 2026. Only visible text is included; the bottom of the final screenshot cuts off additional notes. Screenshots of the meeting are not copied into this repository.

## Requirement mapping

| Assignment requirement | IteraRoot implementation |
| --- | --- |
| User interface for polynomial coefficients or a polynomial expression | Expression input for `f(x)` |
| Additional mathematical expressions encouraged | `sin`, `cos`, `tan`, `exp`, `log`, `sqrt` |
| Endpoints where applicable | Graph endpoints; neither selected method requires a root bracket |
| User-defined stopping tolerance | Absolute step and residual tolerances |
| Initial guesses and necessary method inputs | Shared `x0`; explicit `g(x)` for fixed point; automatic derivative for Newton |
| Number of iterations | Completed updates, excluding initial row 0 |
| Approximate root or minimizer | Approximate root on success, last valid estimate on failure |
| Iteration table if possible | Full table and CSV export |
| Function graph over a chosen interval | Sampled function plot and final-estimate markers |
| Clear, functional interface | Method selector, examples, explanations, separate result states |
| Project title in uppercase | Uppercase full title in README and overview |
| Team names in Last Name, First Name Middle Initial format | Pending group information |
| Brief project overview and objectives/features | `docs/project-overview.md` |

## Visible grading weights

| Criterion | Weight | Development priority |
| --- | --- | --- |
| Documentation and Presentation | 10% | Overview, objectives, instructions, demo |
| Functionality and Accuracy | 70% | Correct updates, tolerances, histories, input-dependent outputs |
| Design and Layout of the Excel | 20% | Clear interface and effective graphs; this is the rubric's wording although its task permits Python/web applications |

The assignment permits a preferred platform, including Python through Streamlit or Tkinter, Excel, or a website. The selected implementation is Python with Streamlit.

## Grouping

The screenshots specify 4–5 members per group, balanced composition, and no duplication of chosen methods. This repository does not invite collaborators automatically.

The [team assignments](../README.md#group-collaboration) link to each member’s tasks and demo checks. Jethro integrates the two plots with the redesigned interface and leads the final demo.

## Remaining decisions

- Full team names in the instructor’s required format.
- Instructor name, submission date, and any further instructions outside the visible screenshots.
- Whether the instructor requires a particular error formula, stopping convention, or hand-worked sample.
- Final visual customization and deployment, if requested.

## Starter scope

The starter includes both methods, a comparison mode, automatic first derivatives, explicit input validation, tables, graphs, examples, documentation, and automated checks. It does not attempt to invent a universally convergent rearrangement `g(x)`. It compares two methods independently; it is not a hybrid solver.
