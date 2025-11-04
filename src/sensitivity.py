"""
sensitivity.py
================

This script answers the three sensitivity analysis questions posed in the
"Blue Ridge Hot Tubs" lecture.  It repeatedly solves the product‑mix
linear program with incremented resource limits to compute how much the
objective function (profit) changes per additional unit of each resource.

The questions are:

1. **Pumps** – If the company could acquire more pumps, should they?  What is
   the marginal profit for each additional pump until the constraint is no
   longer binding?
2. **Labour** – If the company could acquire more labour, how much does
   profit increase per additional hour until labour is no longer binding?
3. **Tubing** – If the company could acquire more tubing, does profit change
   (i.e., is tubing a binding constraint)?

The script prints the baseline solution and the marginal profit in the
region where the shadow price is constant.  It also reports the breakpoint
where the shadow price changes (approximate).  No fluff is included; it
focuses on directly computing and reporting the marginal values.
"""

from lp_model import Resources, solve_hot_tubs


def delta_profit(base_profit: float, new_profit: float) -> float:
    """Return the change in profit between successive solves."""
    return round(new_profit - base_profit, 2)


def q1_more_pumps(max_test: int = 220) -> None:
    """
    Compute marginal profit for additional pumps.

    Parameters
    ----------
    max_test : int
        Maximum number of pumps to test (must be >= baseline pumps).
    """
    base_res = Resources()
    base_sol = solve_hot_tubs(base_res)
    base_profit = base_sol.profit

    print("\nQ1 — Additional Pumps")
    print(f"Baseline profit @ {base_res.pumps} pumps: ${base_profit:,.2f}")

    last_profit = base_profit
    first_delta = None
    breakpoint_at = None

    for p in range(base_res.pumps + 1, max_test + 1):
        res = Resources(pumps=p, labor_hours=base_res.labor_hours, tubing_feet=base_res.tubing_feet)
        sol = solve_hot_tubs(res)
        d = delta_profit(last_profit, sol.profit)
        # record the first marginal value
        if first_delta is None:
            first_delta = d
        # detect break when marginal changes significantly
        elif abs(d - first_delta) > 1e-6 and breakpoint_at is None:
            breakpoint_at = p
        last_profit = sol.profit

    print(f"Marginal profit per additional pump: ${first_delta:,.2f}")
    if breakpoint_at:
        print(f"Constant marginal value until about {breakpoint_at - 1} pumps; breakpoint near {breakpoint_at}.")
    else:
        print("Constant marginal value in tested range; no breakpoint detected.")


def q2_more_labor(max_test: int = 1800) -> None:
    """
    Compute marginal profit for additional labour hours.

    Parameters
    ----------
    max_test : int
        Maximum number of labour hours to test (must be >= baseline hours).
    """
    base_res = Resources()
    base_sol = solve_hot_tubs(base_res)
    base_profit = base_sol.profit

    print("\nQ2 — Additional Labour Hours")
    print(f"Baseline profit @ {base_res.labor_hours} labour hours: ${base_profit:,.2f}")

    last_profit = base_profit
    first_delta = None
    breakpoint_at = None

    for h in range(base_res.labor_hours + 1, max_test + 1):
        res = Resources(pumps=base_res.pumps, labor_hours=h, tubing_feet=base_res.tubing_feet)
        sol = solve_hot_tubs(res)
        d = delta_profit(last_profit, sol.profit)
        if first_delta is None:
            first_delta = d
        elif abs(d - first_delta) > 1e-6 and breakpoint_at is None:
            breakpoint_at = h
        last_profit = sol.profit

    print(f"Marginal profit per additional labour hour: ${first_delta:,.2f}")
    if breakpoint_at:
        print(f"Constant marginal value until about {breakpoint_at - 1} hours; breakpoint near {breakpoint_at}.")
    else:
        print("Constant marginal value in tested range; no breakpoint detected.")


def q3_more_tubing(increment: int = 50) -> None:
    """
    Check whether additional tubing changes the objective (binding or not).

    Parameters
    ----------
    increment : int
        Number of feet of tubing to incrementally test.
    """
    base_res = Resources()
    base_sol = solve_hot_tubs(base_res)
    base_profit = base_sol.profit

    print("\nQ3 — Additional Tubing")
    print(f"Baseline profit @ {base_res.tubing_feet} feet of tubing: ${base_profit:,.2f}")

    last_profit = base_profit
    for t in range(base_res.tubing_feet + 1, base_res.tubing_feet + increment + 1):
        res = Resources(pumps=base_res.pumps, labor_hours=base_res.labor_hours, tubing_feet=t)
        sol = solve_hot_tubs(res)
        d = delta_profit(last_profit, sol.profit)
        if abs(d) > 1e-6:
            print(f"At {t} feet, profit changes by ${d:,.2f} (tubing becomes binding).")
            return
        last_profit = sol.profit
    print("Profit does not change with additional tubing in this tested region (tubing is non‑binding).")


def main() -> None:
    """Run baseline solution and all sensitivity questions."""
    base = solve_hot_tubs(Resources())
    print("Baseline optimal production plan:")
    print(f"  Aqua-Spas = {base.x_aqua:.2f}\n  Hydro-Luxes = {base.x_hydro:.2f}")
    print(f"  Maximum profit = ${base.profit:,.2f}")
    print(f"  Resource usage: {base.used}")
    print(f"  Slack: {base.slack}\n")

    # Answer the sensitivity questions
    q1_more_pumps()
    q2_more_labor()
    q3_more_tubing()


if __name__ == "__main__":
    main()