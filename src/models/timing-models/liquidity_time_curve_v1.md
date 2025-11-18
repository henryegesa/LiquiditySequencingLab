# Liquidity-Time Curve — Version 1 Formalization

This document defines the **v1 mathematical formulation** of the Liquidity-Time Curve used in Liquidity Sequencing Infrastructure (LSI).

The goal:  
Describe how **available liquidity** and **obligations** evolve over time, and define a **timing mismatch metric** that sequencing should minimize.

---

## 1. Time Horizon

- Discrete time periods:  
  \[
  T = \{0, 1, \dots, T_{\max}\}
  \]

- Resolution can be:
  - minutes  
  - hours  
  - days  
  depending on the use case.

---

## 2. Liquidity Function

For each account \( a \in A \):

- **Liquidity availability function**:
  \[
  L_a(t) \quad \forall t \in T
  \]

Interpretation:
- \( L_a(t) \) is the *maximum spendable liquidity* for account \( a \) at time \( t \), before new events are executed.
- It reflects current balance, holds, and reserved amounts.

Baseline (without LSI sequencing), we can define:

\[
L_a^{\text{baseline}}(t) = B_{a,0} + \sum_{e: a(e) = a} a_e \cdot \mathbb{1}\{t_e^{\text{baseline}} \le t\}
\]

Where:
- \( t_e^{\text{baseline}} \) is the naive or traditional execution time (no sequencing).
- \( \mathbb{1}\{\cdot\} \) is the indicator function.

Under LSI, the actual liquidity path becomes:

\[
L_a^{\text{LSI}}(t) = B_{a,0} + \sum_{e: a(e) = a} a_e \cdot \sum_{u=0}^{t} z_{e,u}
\]

Where \( z_{e,u} \) comes from the **sequencing graph solution**.

---

## 3. Obligations Function

For each account \( a \in A \), define an **obligation intensity** over time:

\[
O_a(t) \quad \forall t \in T
\]

Interpretation:
- Aggregate “pressure” of obligations that are due or effective at time \( t \).
- Captures bills, loans, remittances, recurring payments, etc.

One simple discrete formulation:

\[
O_a(t) = \sum_{e \in E_a^{\text{out}}} \omega_e \cdot \mathbb{1}\{t_e^\star = t\}
\]

Where:
- \( E_a^{\text{out}} = \{e \in E \mid a(e) = a,\ a_e < 0\} \) is the set of outflow events for account \( a \).
- \( t_e^\star \) is the **ideal due time** for event \( e \).
- \( \omega_e \ge 0 \) is a weight reflecting the seriousness of missing this event (e.g., rent vs. small subscription).

We can also smooth this over a window if desired (v2).

---

## 4. Timing Mismatch

The **central concept**: we want *available liquidity* and *obligation pressure* to be aligned over time.

For each account \( a \), define the **timing mismatch** at time \( t \):

\[
M_a(t) = \max\big(0, O_a(t) - L_a^{\text{LSI}}(t)\big)
\]

Interpretation:
- If \( L_a^{\text{LSI}}(t) \ge O_a(t) \), mismatch is 0 (liquidity is sufficient).
- If \( L_a^{\text{LSI}}(t) < O_a(t) \), mismatch is the shortfall.

Total timing mismatch over the horizon:

\[
\text{Mismatch}_a = \sum_{t \in T} M_a(t)
\]

For all accounts:

\[
\text{Mismatch}_{\text{total}} = \sum_{a \in A} \text{Mismatch}_a
\]

This is a **high-level health metric** for LSI.

---

## 5. Liquidity Stress Metric

We can also define a **stress function** to capture how close an account runs to its minimum buffer.

Define a target safety buffer \( S_a \ge 0 \) (desired minimum liquidity level).

For each account:

\[
S\_a(t) = \max\big(0, S_a - L_a^{\text{LSI}}(t)\big)
\]

Total **liquidity stress**:

\[
\text{Stress}_a = \sum_{t \in T} S_a(t), \quad
\text{Stress}_{\text{total}} = \sum_{a \in A} \text{Stress}_a
\]

This measures how often and how severely accounts operate below the desired comfort threshold.

---

## 6. Objective Link to Sequencing

The sequencing graph optimization (defined separately) can be augmented to minimize:

- timing cost (event-by-event deviation), and
- timing mismatch, and/or
- liquidity stress.

Example composite objective:

\[
\min \quad \alpha \cdot \text{Cost}_{\text{timing}} + \beta \cdot \text{Mismatch}_{\text{total}} + \gamma \cdot \text{Stress}_{\text{total}}
\]

Where:
- \( \alpha, \beta, \gamma \ge 0 \) are weights expressing trade-offs.

This connects the **Liquidity-Time Curve** directly into the **sequencing optimizer**.

---

## 7. Baseline vs. LSI Comparison

For empirical or simulation comparison, compute:

\[
\Delta \text{Mismatch} = \text{Mismatch}_{\text{baseline}} - \text{Mismatch}_{\text{LSI}}
\]

\[
\Delta \text{Stress} = \text{Stress}_{\text{baseline}} - \text{Stress}_{\text{LSI}}
\]

Where:
- baseline metrics use \( L_a^{\text{baseline}}(t) \)
- LSI metrics use \( L_a^{\text{LSI}}(t) \)

Positive values imply **improvement** due to sequencing.

---

## 8. Visual Interpretation

For each account or corridor, we can plot:

- curve of \( L_a^{\text{LSI}}(t) \) over time
- curve of \( O_a(t) \) over time
- highlighted regions where \( O_a(t) > L_a^{\text{LSI}}(t) \)

These visuals should live under `/diagrams/models/liquidity_time_curve_diagram.*`.

---

## 9. Next Steps (v2+)

Future refinements can include:

- continuous-time formulations  
- stochastic liquidity shocks  
- probabilistic obligations (e.g., random expenses)  
- more advanced stress functions (e.g., convex penalties for deeper shortfalls)  

