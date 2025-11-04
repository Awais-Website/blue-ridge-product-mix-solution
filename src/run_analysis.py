# run_analysis.py

# Runs baseline LP, sensitivity for pumps & labor, reports highest profit,
# and saves + shows graphs with calculated breakpoints.

from lp_model import Resources, solve_hot_tubs

import matplotlib.pyplot as plt

def sensitivity_curve_pumps(start=200, stop=220, labor=1566, tubing=2880):
    xs = list(range(start, stop + 1))
    profits = []
    
    for p in xs:
        sol = solve_hot_tubs(Resources(pumps=p, labor_hours=labor, tubing_feet=tubing))
        profits.append(sol.profit)
    
    # marginal deltas
    deltas = [profits[i+1] - profits[i] for i in range(len(profits)-1)]
    
    # detect breakpoint where marginal changes
    if deltas:
        first = deltas[0]
        bp = None
        for i, d in enumerate(deltas[1:], start=1):
            if abs(d - first) > 1e-6:
                bp = xs[i]  # last constant is xs[i]
                break
        breakpoint_at = bp if bp is not None else xs[-1]
    else:
        breakpoint_at = xs[-1]
    
    # highest profit in range
    max_profit = max(profits)
    max_at = xs[profits.index(max_profit)]
    
    return xs, profits, breakpoint_at, max_profit, max_at

def sensitivity_curve_labor(start=1566, stop=1820, pumps=200, tubing=2880):
    xs = list(range(start, stop + 1))
    profits = []
    
    for h in xs:
        sol = solve_hot_tubs(Resources(pumps=pumps, labor_hours=h, tubing_feet=tubing))
        profits.append(sol.profit)
    
    deltas = [profits[i+1] - profits[i] for i in range(len(profits)-1)]
    
    if deltas:
        first = deltas[0]
        bp = None
        for i, d in enumerate(deltas[1:], start=1):
            if abs(d - first) > 1e-6:
                bp = xs[i]
                break
        breakpoint_at = bp if bp is not None else xs[-1]
    else:
        breakpoint_at = xs[-1]
    
    max_profit = max(profits)
    max_at = xs[profits.index(max_profit)]
    
    return xs, profits, breakpoint_at, max_profit, max_at

def plot_curve(xs, ys, breakpoint_at, xlabel, title, outpath):
    plt.figure(figsize=(7,5))
    plt.plot(xs, ys, marker='o')
    # draw breakpoint line if inside range
    if xs[0] <= breakpoint_at <= xs[-1]:
        plt.axvline(breakpoint_at, linestyle='--', color='red', label=f'Breakpoint at {breakpoint_at}')
    plt.xlabel(xlabel)
    plt.ylabel("Profit ($)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.show()

def main():
    # 1) Baseline optimal product mix and profit
    base = solve_hot_tubs(Resources(pumps=200, labor_hours=1566, tubing_feet=2880))
    print("Baseline optimal plan")
    print(f"  Aqua-Spa:  {base.x_aqua:.2f}")
    print(f"  Hydro-Lux: {base.x_hydro:.2f}")
    print(f"  Profit:    ${base.profit:,.2f}")
    print(f"  Used:      {base.used}")
    print(f"  Slack:     {base.slack}")
    
    # 2) Sensitivity: Pumps
    px, py, p_break, p_max_profit, p_max_at = sensitivity_curve_pumps()
    print("\nPumps sensitivity")
    print(f"  Breakpoint (calculated): ~{p_break} pumps")
    print(f"  Highest profit in tested range: ${p_max_profit:,.2f} at {p_max_at} pumps")
    plot_curve(
        px, py, p_break,
        xlabel="Number of Pumps Available",
        title="Profit vs Pumps (Breakpoint marked)",
        outpath="profit_vs_pumps.png"
    )
    
    # 3) Sensitivity: Labor
    lx, ly, l_break, l_max_profit, l_max_at = sensitivity_curve_labor()
    print("\nLabor sensitivity")
    print(f"  Breakpoint (calculated): ~{l_break} hours")
    print(f"  Highest profit in tested range: ${l_max_profit:,.2f} at {l_max_at} hours")
    plot_curve(
        lx, ly, l_break,
        xlabel="Labor Hours Available",
        title="Profit vs Labor (Breakpoint marked)",
        outpath="profit_vs_labor.png"
    )

if __name__ == "__main__":
    main()

