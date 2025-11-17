# LSI Sequencing Graph — Version 1 Formalization

This document defines the **v1 mathematical formulation** of the Liquidity Sequencing Infrastructure (LSI) sequencing graph.

The goal:  
Given a set of **liquidity events** (income, obligations, transfers) with time windows and priorities, find an **execution schedule** that **minimizes timing cost** subject to **liquidity and dependency constraints**.

---

## 1. Sets and Indices

- \( A \) — set of accounts (households, wallets, ledgers), indexed by \( a \)
- \( E \) — set of liquidity events, indexed by \( e \)
- \( T = \{0, 1, \dots, T_{\max}\} \) — discrete time periods, indexed by \( t \)

Each event is something like:
- salary inflow
- bill/loan repayment
- remittance send
- internal transfer

---

## 2. Event Data (Parameters)

For each event \( e \in E \):

- \( a_e \in \mathbb{R} \)  
  Signed amount:
  - \( a_e > 0 \): inflow (credit)
  - \( a_e < 0 \): outflow (debit)

- \( \tau_e^- \in T \)  
  Earliest allowed execution time.

- \( \tau_e^+ \in T \)  
  Latest allowed execution time.

- \( p_e \ge 0 \)  
  Priority weight (higher = more important to place “well” in time).

- \( a(e) \in A \)  
  The account whose liquidity is affected by event \( e \).

- \( t_e^\star \in T \) (optional but useful)  
  “Ideal” execution time (e.g., due date, payday, or user preference).

For each account \( a \in A \):

- \( B_{a,0} \in \mathbb{R} \)  
  Initial balance at time \( t = 0 \).

- \( L_a^{\min} \in \mathbb{R} \)  
  Minimum allowed liquidity level (e.g., cannot go below this).

---

## 3. Decision Variables

We model execution as choosing **exactly one time slot** for each event.

- \( z_{e,t} \in \{0,1\} \) for all \( e \in E, t \in T \)  

  \( z_{e,t} = 1 \) if event \( e \) is executed at time \( t \), and 0 otherwise.

From this we can define the realized execution time:

\[
\hat{t}_e = \sum_{t \in T} t \cdot z_{e,t}
\]

---

## 4. Feasibility Constraints

### 4.1. Each event executes exactly once

\[
\sum_{t \in T} z_{e,t} = 1 \quad \forall e \in E
\]

### 4.2. Respect event time windows

For times outside the allowed window, the event cannot be scheduled:

\[
z_{e,t} = 0 \quad \forall e \in E,\ \forall t \notin [\tau_e^-, \tau_e^+]
\]

(Practically: we only allow \( z_{e,t} \) over that window.)

---

## 5. Liquidity Dynamics

We define the **cumulative balance** for each account \( a \) at each time \( t \).

Let

\[
B_{a,t} = B_{a,0} + \sum_{e \in E: a(e) = a} a_e \cdot \sum_{u=0}^{t} z_{e,u}
\]

Interpretation:
- Start from initial balance \( B_{a,0} \)
- Add all event amounts belonging to account \( a \) that have executed at or before time \( t \)

### 5.1. Liquidity constraint

Each account must maintain a minimum liquidity buffer:

\[
B_{a,t} \ge L_a^{\min} \quad \forall a \in A,\ \forall t \in T
\]

This is where **sequencing** starts to matter: executing too many outflows before inflows may violate this constraint.

---

## 6. Dependency Constraints (Optional Layer)

Sometimes event \( j \) cannot execute before event \( i \) (e.g., repayment cannot precede disbursement).

Let \( \mathcal{D} \subseteq E \times E \) be a set of ordered pairs \( (i, j) \) such that **event \( j \) depends on event \( i \)**.

We enforce:

\[
\hat{t}_j \ge \hat{t}_i \quad \forall (i,j) \in \mathcal{D}
\]

Using \( z \)-variables:

\[
\sum_{t \in T} t \cdot z_{j,t} \ge \sum_{t \in T} t \cdot z_{i,t} \quad \forall (i,j) \in \mathcal{D}
\]

---

## 7. Timing Cost Function

We define a **timing cost** for each event \( e \) at each time \( t \).

Basic version:

\[
c_{e,t} = p_e \cdot |t - t_e^\star|
\]

Interpretation:
- Cost grows the further an event is from its ideal time \( t_e^\star \)
- Priority \( p_e \) scales how painful this deviation is

To keep this linear for solvers, we can replace absolute value with a standard linearization, or use separate earliness/lateness terms (to be expanded in v2 if needed).

Total timing cost:

\[
\text{Cost} = \sum_{e \in E} \sum_{t \in T} c_{e,t} \cdot z_{e,t}
\]

---

## 8. Optimization Problem (Sequencing Graph Problem)

**Objective:**

\[
\min_{z} \quad \sum_{e \in E} \sum_{t \in T} c_{e,t} \cdot z_{e,t}
\]

**Subject to:**

1. Event executes exactly once:
\[
\sum_{t \in T} z_{e,t} = 1 \quad \forall e \in E
\]

2. Time windows:
\[
z_{e,t} = 0 \quad \forall e \in E,\ \forall t \notin [\tau_e^-, \tau_e^+]
\]

3. Liquidity constraints:
\[
B_{a,t} \ge L_a^{\min} \quad \forall a \in A,\ \forall t \in T
\]
with
\[
B_{a,t} = B_{a,0} + \sum_{e: a(e)=a} a_e \cdot \sum_{u=0}^{t} z_{e,u}
\]

4. Dependency constraints (if any):
\[
\sum_{t \in T} t \cdot z_{j,t} \ge \sum_{t \in T} t \cdot z_{i,t} \quad \forall (i,j) \in \mathcal{D}
\]

5. Binary execution variables:
\[
z_{e,t} \in \{0,1\} \quad \forall e \in E,\ \forall t \in T
\]

This is a **binary optimization problem** (a scheduling-like problem with liquidity constraints).  
The **sequencing graph** is implicit in:
- the events \( E \),
- the dependency pairs \( \mathcal{D} \),
- and the liquidity propagation across time.

---

## 9. Graph Interpretation

We can interpret this as a graph \( G = (V, \mathcal{E}) \):

- **Vertices \( V \)**:  
  - one node for each event \( e \),  
  - optionally, time-layered nodes \((e, t)\) for richer visualizations.

- **Edges \( \mathcal{E} \)**:
  - dependency edges \( (i, j) \in \mathcal{D} \)
  - implicit temporal feasibility edges derived from time windows and liquidity constraints

- **Edge / node weights**:
  - reflect timing cost and liquidity impact via \( c_{e,t} \), \( a_e \), and priorities \( p_e \).

The optimization chooses a **time assignment** for each event that corresponds to a **feasible path** through this sequencing graph.

---

## 10. Next Steps (v2 Extensions)

Future refinements may add:

- Separate earliness vs. lateness penalties:
  \[
  c_{e,t} = p_e^{\text{early}} \cdot \max(0, t_e^\star - t) + p_e^{\text{late}} \cdot \max(0, t - t_e^\star)
  \]

- Multi-rail execution choices (assigning events to specific rails with their own timing).

- Stochastic variations in inflows/outflows.

These will be documented as **v2+** specifications.

