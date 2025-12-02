# Liquidity Sequencing Lab – Research Agenda

**Principal:** Henry Maloba  
**Lab:** Liquidity Sequencing Lab (LSI Lab)  
**Focus:** Designing the timing layer of money through Liquidity Sequencing Infrastructure (LSI)

---

## 1. Motivation

Modern financial systems are optimized for *movement* of value, not for the *timing* and *ordering* of that movement.

Households, firms, and institutions routinely experience liquidity stress not because they are insolvent in aggregate, but because:

- incomes and obligations are misaligned in time,
- intermediaries batch, delay, or reorder flows for operational reasons,
- cross-border corridors introduce additional frictions, FX windows, and regulatory lags.

The lab’s core claim:  
> **The micro-timing and sequencing of flows is an independent design surface for financial stability.**

Liquidity Sequencing Infrastructure (LSI) is the proposed layer that explicitly models and optimizes this timing dimension.

---

## 2. High-Level Research Questions

1. **Liquidity Sequencing**
   - How should we model incomes, obligations, and transfers as a time-indexed graph of events?
   - Under what conditions does re-ordering flows materially reduce liquidity stress for a given agent or system?
   - How do small timing changes propagate through a network of interconnected balance sheets?

2. **Cross-Border Infrastructure**
   - How can we design wallet- and ledger-based architectures that minimize unnecessary settlement and FX lags?
   - What corridor patterns (e.g., US → Kenya) are most sensitive to timing improvements versus raw price improvements?
   - How can LSI coexist with, and overlay on, existing rails (ACH, card networks, RTGS, mobile money)?

3. **System Design for Stability**
   - How should policy constraints (prudential rules, risk limits, supervisory expectations) be encoded as *policy engine* constraints?
   - What metrics best capture “timing-based resilience” at the household, firm, and system levels?
   - How do we design incentives so that intermediaries adopt sequencing-aware architectures?

---

## 3. Workstreams

### 3.1 Sequencing Graph Formalization

**Objective:**  
Develop a robust graph-based representation of financial events (incomes, obligations, transfers) with timing, dependencies, and costs.

**Key tasks:**

- Define event types, node/edge structure, and temporal indexing.
- Formalize dependency and precedence constraints (who must be paid before whom, under what rules).
- Introduce cost functions for:
  - delay,
  - pre-emption,
  - re-routing,
  - partial settlement.

**Outputs:**

- Sequencing graph specification (v1, v2, …) in `frameworks/`
- Worked examples and small synthetic graphs in `simulations/`
- Wiki alignment: *Sequencing Graph* page.

---

### 3.2 Flow Optimization Engine (FOE)

**Objective:**  
Build an optimization layer that chooses ordering, sizing, and liquidity sources for payments, subject to constraints.

**Key tasks:**

- Translate graph structure into optimization problems (LP / MILP or heuristic rules).
- Define feasible decision variables:
  - execution time,
  - partial execution,
  - source selection (wallet, credit line, float, buffer).
- Integrate policy and risk constraints (e.g., caps, buffers, exposure limits).
- Compare naive vs optimized sequencing policies.

**Outputs:**

- FOE v1 formalization in `frameworks/`
- Prototype solver code in `src/` (when implemented)
- Wiki alignment: *Flow Optimization Engine* page.

---

### 3.3 Liquidity–Time Curve

**Objective:**  
Describe how available liquidity and obligations evolve over time under different rules and shocks.

**Key tasks:**

- Define liquidity-time functions for:
  - households,
  - small firms,
  - intermediaries.
- Model timing mismatch between inflows and outflows.
- Introduce stress metrics (e.g., max liquidity gap, duration in negative zone).
- Compare baseline vs LSI-managed curves.

**Outputs:**

- Liquidity–time formulations in `frameworks/`
- Scenario plots produced by simulations
- Wiki alignment: *Liquidity–Time Curve* page.

---

### 3.4 Corridor Simulations (e.g., US → Kenya)

**Objective:**  
Test LSI concepts in concrete corridors with realistic flows and constraints.

**Key tasks:**

- Define corridor parameters (volumes, fees, delays, FX windows, typical use cases).
- Generate synthetic but realistic flow data for households and small businesses.
- Run comparative simulations:
  - existing rails vs LSI sequencing,
  - different policy engine settings,
  - stress and shock scenarios.
- Measure:
  - liquidity gap reduction,
  - delay reduction,
  - volatility in available balances.

**Outputs:**

- Corridor configs in `simulations/`
- Simulation runner scripts in `src/` (when implemented)
- Results summaries in `papers/` and wiki *Simulations* page.

---

### 3.5 Applied System Patterns

**Objective:**  
Map research into reusable design patterns for real systems: payment networks, payroll engines, remittance platforms, and credit products.

**Key tasks:**

- Identify archetypal systems (e.g., payroll-linked remittance, card-based cross-border spend, mobile-money style wallets).
- For each, define:
  - event types,
  - key constraints,
  - candidate sequencing policies.
- Evaluate implementation feasibility and regulatory friction.

**Outputs:**

- Pattern write-ups in `docs/` or `frameworks/`
- Case-study style sections in papers
- Refined talking points for industry conversations (e.g., JP Morgan, fintech partners).

---

## 4. Time Horizon and Versioning

This agenda is deliberately **multi-year** and versioned:

- **v0.1.x** – Repository and wiki scaffold, conceptual frameworks, and narrative alignment.
- **v0.2.x** – First complete definitions of Sequencing Graph, FOE, and Liquidity–Time Curve + baseline simulations.
- **v0.3.x+** – Code implementations, richer corridor simulations, and empirical papers.

Each workstream can move at its own pace, but changes should:

- update the relevant wiki pages,
- be reflected in `frameworks/` and `simulations/`,
- and, when mature, be integrated into papers under `papers/`.

---

## 5. Intended Audiences

- **Academic:**  
  Researchers in payments, financial economics, operations research, and system design interested in timing, liquidity, and network effects.

- **Industry:**  
  Banks, payment networks, fintechs, and infrastructure providers exploring new operating models for cross-border flows and liquidity management.

- **Policy / Regulatory:**  
  Central banks and supervisors considering how sequencing-aware infrastructure can complement existing prudential frameworks.

---

## 6. Positioning Statement

The lab’s core through-line is simple:

> **Timing is the new capital.**  
> Liquidity Sequencing Infrastructure is an attempt to engineer that timing explicitly—so that borderless, programmable money systems remain stable not by accident, but by design.
