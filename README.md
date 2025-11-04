# Blue Ridge Product Mix and Sensitivity Analysis (Linear Programming in Python)

This project applies linear programming to optimize Blue Ridge’s production mix of Aqua-Spa and Hydro-Lux hot tubs. It identifies the most profitable allocation of limited resources (pumps, labor hours, and tubing) and conducts sensitivity analysis to measure how profit changes with resource availability.

---

## Project Overview

The optimization model maximizes profit given the company’s production constraints. After solving the baseline model, sensitivity analysis is performed by incrementally increasing pump and labor availability to identify breakpoints where profit growth stops. These breakpoints highlight the limits of resource utility and the transition of binding constraints.

---

## Model Summary

**Decision Variables**

* (x_1): Number of Aqua-Spa units produced
* (x_2): Number of Hydro-Lux units produced

**Objective Function**
[
\text{Maximize: } Z = 350x_1 + 300x_2
]

**Constraints**
[
\begin{aligned}
x_1 + x_2 &\le 200 \quad &\text{(pumps)} \
9x_1 + 6x_2 &\le 1566 \quad &\text{(labor)} \
12x_1 + 16x_2 &\le 2880 \quad &\text{(tubing)} \
x_1, x_2 &\ge 0
\end{aligned}
]

---

## Baseline Optimization Results

| Variable   | Optimal Quantity |
| ---------- | ---------------: |
| Aqua-Spa   |              122 |
| Hydro-Lux  |               78 |
| **Profit** |      **$66,100** |

Both the **pump** and **labor** constraints are binding, while tubing has slack, confirming it is non-limiting in this scenario.

---

## Sensitivity Analysis

The model was re-solved multiple times with incremental increases in resource limits. Each run measured the change in maximum achievable profit.

| Resource    |  Breakpoint | Marginal Profit Before Breakpoint |
| ----------- | ----------: | --------------------------------: |
| Pumps       |  ~207 units |                     $200 per pump |
| Labor Hours | ~1800 hours |                   $16.67 per hour |
| Tubing      | Non-binding |                                $0 |

The analysis confirms that increasing pumps or labor improves profit only up to a certain limit, after which other constraints dominate. Tubing remains non-critical across all tested scenarios.

---

## Visual Results

**Profit vs. Pump Availability**
![Profit vs Pumps](images/profit_vs_pumps.png)

**Profit vs. Labor Hours**
![Profit vs Labor](images/profit_vs_labor.png)

The slope of each curve represents marginal profit. The flattening beyond 207 pumps and 1800 labor hours indicates that further resource additions yield no economic gain.

---

## Implementation

| File                  | Purpose                                                                                                               |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `lp_model.py`         | Defines the linear programming model using PuLP and returns optimal results.                                          |
| `run_analysis.py`     | Executes the baseline optimization, performs sensitivity tests, identifies breakpoints, and generates visualizations. |
| `images/profit_vs_pumps.png` | Profit variation with pump availability.                                                                         |
| `images/profit_vs_labor.png` | Profit variation with labor availability.                                                                        |

---

## Execution Instructions

1. **Install dependencies**

   ```bash
   pip install pulp matplotlib
   ```

2. **Run the analysis**

   ```bash
   python run_analysis.py
   ```

3. **Expected Output**

   ```
   Baseline optimal plan
     Aqua-Spa:  122.00
     Hydro-Lux: 78.00
     Profit:    $66,100.00
   Pumps sensitivity
     Breakpoint: ~207 pumps
     Highest profit: $67,500
   Labor sensitivity
     Breakpoint: ~1800 hours
     Highest profit: $70,000
   ```

---

## Summary

The model validates that the existing production plan is near-optimal under current constraints. Pumps and labor are the key limiting factors, with clear diminishing returns after specific thresholds. The project demonstrates the use of linear programming for operational decision support and the application of sensitivity analysis to evaluate resource allocation efficiency.


