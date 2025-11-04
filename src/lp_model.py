"""
lp_model.py
================

This module defines a simple linear programming model for the Blue Ridge Hot Tubs
product‑mix problem.  It uses the `pulp` library to formulate and solve a
continuous linear program, returning both the optimal production plan and
resource utilisation details.

Two hot tub models are produced:

* **Aqua‑Spa** (x1): requires 1 pump, 9 hours of labour, 12 feet of tubing and
  yields \$350 profit.
* **Hydro‑Lux** (x2): requires 1 pump, 6 hours of labour, 16 feet of tubing and
  yields \$300 profit.

Resources are limited to a given number of pumps, labour hours and feet of
tubing.  The objective is to maximise profit subject to these resource
constraints.  All decision variables are continuous and non‑negative.

The `solve_hot_tubs` function accepts a `Resources` dataclass specifying the
available quantities of pumps, labour and tubing.  It returns a `Solution`
dataclass containing the optimal production quantities, the maximum profit,
resources used and remaining slack.
"""


from dataclasses import dataclass
from typing import Dict
import pulp


@dataclass
class Resources:
    """Available quantities of each resource."""

    pumps: int = 200
    labor_hours: int = 1566
    tubing_feet: int = 2880


@dataclass
class Solution:
    """Results of solving the product‑mix LP."""

    x_aqua: float
    x_hydro: float
    profit: float
    used: Dict[str, float]
    slack: Dict[str, float]


def solve_hot_tubs(res: Resources) -> Solution:
    """
    Solve the Blue Ridge Hot Tubs product‑mix linear program.

    Parameters
    ----------
    res : Resources
        The available amounts of pumps, labour hours and tubing feet.

    Returns
    -------
    Solution
        Optimal production quantities, profit, resource usage and slack.

    Notes
    -----
    The decision variables are continuous.  If integer solutions are required
    you can set `cat='Integer'` when creating the variables.
    """
    # Define the LP problem (maximise profit)
    model = pulp.LpProblem("BlueRidgeHotTubs", pulp.LpMaximize)

    # Decision variables for Aqua‑Spa and Hydro‑Lux
    x1 = pulp.LpVariable("Aqua_Spa", lowBound=0)
    x2 = pulp.LpVariable("Hydro_Lux", lowBound=0)

    # Objective function
    model += 350 * x1 + 300 * x2

    # Resource constraints
    model += x1 + x2 <= res.pumps          # Pumps constraint
    model += 9 * x1 + 6 * x2 <= res.labor_hours  # Labour hours constraint
    model += 12 * x1 + 16 * x2 <= res.tubing_feet  # Tubing feet constraint

    # Solve the LP using CBC (default for pulp)
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # Retrieve optimal values; handle None by defaulting to 0.0
    xa = x1.value() or 0.0
    xh = x2.value() or 0.0
    profit = pulp.value(model.objective) or 0.0

    # Calculate used resources
    used = {
        "pumps": xa + xh,
        "labor": 9 * xa + 6 * xh,
        "tubing": 12 * xa + 16 * xh,
    }

    # Calculate slack (remaining resources)
    slack = {
        "pumps": res.pumps - used["pumps"],
        "labor": res.labor_hours - used["labor"],
        "tubing": res.tubing_feet - used["tubing"],
    }

    return Solution(xa, xh, profit, used, slack)


if __name__ == "__main__":
    # Example: run the model with default resource amounts
    sol = solve_hot_tubs(Resources())
    print(f"Optimal plan: Aqua-Spas = {sol.x_aqua:.2f}, Hydro-Luxes = {sol.x_hydro:.2f}")
    print(f"Maximum profit: ${sol.profit:,.2f}")
    print("Used resources:", sol.used)
    print("Slack:", sol.slack)

