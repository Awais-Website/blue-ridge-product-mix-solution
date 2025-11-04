# Blue Ridge – product mix and Sensitivity Analysis using Python (LP Optimisation) (mymoo)

This repository contains a succinct implementation of the classic **Blue Ridge Hot Tubs**
product‑mix problem and a **sensitivity analysis** performed in Python.  The
goal of the problem is to determine how many of each hot tub model the firm
should produce to maximise profit, given limited resources (pumps, labour and
tubing).  After finding the optimal mix, we explore how profit changes when
additional resources are made available.

## Problem summary

Blue Ridge produces two hot tub models:

| Model     | Profit per unit | Pumps | Labour (hrs) | Tubing (ft) |
|-----------|----------------:|------:|-------------:|------------:|
| **Aqua‑Spa**  | \$350           |     1 |            9 |          12 |
| **Hydro‑Lux** | \$300           |     1 |            6 |          16 |

The firm has **200 pumps**, **1,566 labour hours** and **2,880 feet of tubing** available.
Let \(x_1\) be the number of Aqua‑Spas and \(x_2\) the number of Hydro‑Luxes to produce.
The linear programme is:

\[
\begin{aligned}
\max \quad & 350\,x_1 \; + \; 300\,x_2 \\
\text{s.t.}\quad & x_1 + x_2 \le 200 && \text{(pumps)}\\
& 9 x_1 + 6 x_2 \le 1{,}566 && \text{(labour hours)}\\
& 12 x_1 + 16 x_2 \le 2{,}880 && \text{(tubing feet)}\\
& x_1, x_2 \ge 0.
\end{aligned}
\]

## Baseline optimal solution

The lecture notes report that the optimal continuous solution is **122 Aqua‑Spas and
78 Hydro‑Luxes**, yielding a maximum profit of **\$66,100**.  This solution uses
all pumps and labour hours while leaving tubing slack (2,712 feet used)
【199953774780426†L460-L470】.  Our `src/lp_model.py` solves the same LP using
PuLP and reproduces these values exactly.

## Sensitivity analysis

In practice we may want to know how valuable an additional unit of a resource
would be.  The lecture slides ask three questions (with answers shown in
bold):

1. **Pumps** – If the company could acquire more pumps, should they?  The
   lecture notes state that **profit increases by \$200 for each additional pump up
   to about 207 pumps**【199953774780426†L523-L536】.
2. **Labour** – If more labour hours could be acquired, how much profit would be gained?
   The notes state that **profit increases by \$16.67 for each additional hour of
   labour up to roughly 1,800 hours**【199953774780426†L523-L536】.
3. **Tubing** – If more tubing could be acquired, how much does profit increase?
   The slides explain that **additional tubing does not change profit; tubing is a
   non‑binding constraint**【199953774780426†L523-L536】.

Our script `src/sensitivity.py` reproduces these results programmatically.  It
solves the LP repeatedly while incrementing the right‑hand side of each
constraint and computes the change in profit.  In the region where the shadow
price is constant, the marginal values match the lecture results exactly.

Additionally, `src/run_analysis.py` provides a graphical sensitivity analysis
that generates plots showing profit curves and calculated breakpoints for pumps
and labor resources.

### Running the analysis

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the sensitivity analysis:

   ```bash
   python src/sensitivity.py
   ```

3. Run the graphical analysis (generates plots):

   ```bash
   python src/run_analysis.py
   ```

   The script prints the baseline solution and answers the three questions.  For
   example, you should see output similar to:

   ```text
   Baseline optimal production plan:
     Aqua-Spas = 122.00
     Hydro-Luxes = 78.00
     Maximum profit = $66,100.00
     Resource usage: {'pumps': 200.0, 'labor': 1566.0, 'tubing': 2712.0}
     Slack: {'pumps': 0.0, 'labor': 0.0, 'tubing': 168.0}

   Q1 — Additional Pumps
   Baseline profit @ 200 pumps: $66,100.00
   Marginal profit per additional pump: $200.00
   Constant marginal value until about 207 pumps; breakpoint near 208.

   Q2 — Additional Labour Hours
   Baseline profit @ 1566 labour hours: $66,100.00
   Marginal profit per additional labour hour: $16.67
   Constant marginal value until about 1800 hours; breakpoint near 1801.

   Q3 — Additional Tubing
   Baseline profit @ 2880 feet of tubing: $66,100.00
   Profit does not change with additional tubing in this tested region (tubing is non‑binding).
   ```

## Project files

* **`src/lp_model.py`** – Defines the linear programme and solves it for any
  resource limits.
* **`src/sensitivity.py`** – Runs the LP repeatedly to compute marginal profit
  changes for pumps, labour and tubing.
* **`src/run_analysis.py`** – Runs baseline LP, performs sensitivity analysis
  for pumps and labor, reports highest profit, and generates graphs with
  calculated breakpoints.
* **`images/sensitivity_analysis.png`** – A snapshot from the lecture slide
  summarising the sensitivity analysis questions and answers.
* **`slides/Blue_Ridge_Sensitivity_Analysis.pptx`** – A companion slide deck
  created with `python-pptx` summarising the problem, the model, the baseline
  solution and the sensitivity analysis results.

## How to build the slides

The PowerPoint in `slides` was generated using the Python script
`slides/create_ppt.py`.  To recreate the slides yourself, install
`python-pptx` and run:

```bash
pip install python-pptx
python slides/create_ppt.py
```

The script assembles six concise slides: title, problem statement, model
formulation, baseline solution, sensitivity results and conclusions.

## Licence

This project is provided for educational purposes.  All code is released
under the MIT licence.  Lecture slides remain the property of the course
owner and are referenced here for commentary and analysis.