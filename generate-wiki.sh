#!/bin/bash
set -e

# Path to the cloned wiki repo (sibling folder)
WIKI_DIR="../LiquiditySequencingLab.wiki"

echo "Using wiki directory: $WIKI_DIR"

mkdir -p "$WIKI_DIR"

echo "Generating Liquidity Sequencing Lab Wiki pages..."

#######################################
# Home.md
#######################################
cat > "$WIKI_DIR/Home.md" << 'PAGe'
# Liquidity Sequencing Lab (LSI)

This wiki documents the models, architecture, simulations, and research powering **Liquidity Sequencing Infrastructure (LSI)**.

LSI treats money as a sequence of timed liquidity commitments rather than isolated events. The aim is to reduce timing mismatch, liquidity stress, and settlement friction across corridors and rails.

## Start Here

- [[What is LSI?]]
- [[Architecture Overview]]
- [[Sequencing Graph]]
- [[Flow Optimization Engine]]
- [[Liquidity-Time Curve]]
- [[Simulations]]
- [[Research Templates]]
- [[Frameworks]]
- [[Lab Notes]]
- [[Contributing]]
- [[Glossary]]
- [[Getting Started]]
PAGe

#######################################
# What-is-LSI.md
#######################################
cat > "$WIKI_DIR/What-is-LSI.md" << 'PAGe'
# What is LSI?

**Liquidity Sequencing Infrastructure (LSI)** is a framework for organizing, sequencing, and settling money based on **time**, not only value.

Instead of treating payments as isolated events, LSI treats them as **timed liquidity commitments** that must be ordered across:

- incomes
- obligations
- transfers
- cross-border flows

## Why It Exists

Traditional rails fail at the micro-timing layer:
- incomes and bills collide out of order
- remittances arrive late relative to obligations
- liquidity is wasted in buffers and overfunding

LSI introduces:
- a **Sequencing Graph** to choose *when* events execute
- a **Flow Optimization Engine (FOE)** to choose *how/where* events execute
- a **Liquidity-Time Curve** to measure timing alignment and stress

LSI is the **sequencing layer of money**.
PAGe

#######################################
# Architecture-Overview.md
#######################################
cat > "$WIKI_DIR/Architecture-Overview.md" << 'PAGe'
# LSI Architecture Overview

The Liquidity Sequencing Infrastructure is organized into layered components.

## Layers

1. **Ingress Layer**
   - Accepts events (payroll, remittance, card, account movements).
   - Normalizes them into a canonical event schema.

2. **Sequencing Engine**
   - Builds sequencing graphs from events.
   - Uses timing windows, priorities, and dependencies.
   - Ensures liquidity constraints are respected over time.

3. **Flow Optimization Engine (FOE)**
   - Chooses *how* events execute across rails and routes.
   - Optimizes fees, FX, delay, risk, and liquidity usage.

4. **Settlement & Routing Layer**
   - Maps sequenced events to actual rails (ACH, card, wires, wallets, RTGS).
   - Handles FX rules, corridor specifics, and cut-off times.

5. **State & Ledger Layer**
   - Tracks balances, commitments, holds, and executed events.
   - May use ledgers, event stores, or hybrids.

6. **Interfaces**
   - Public APIs for products built on LSI.
   - Admin and analytics interfaces for monitoring and operations.

## Reference Files

- `src/architecture/lsi_architecture_overview.md`
- `src/architecture/components.md`
- `src/architecture/deployment.md`

## Diagrams

Core diagrams live under:

- `diagrams/core_architecture.*`
PAGe

#######################################
# Sequencing-Graph.md
#######################################
cat > "$WIKI_DIR/Sequencing-Graph.md" << 'PAGe'
# Sequencing Graph Model

The **Sequencing Graph** chooses *when* each liquidity event executes.

## Key Ideas

- **Nodes**: liquidity events (income, obligations, transfers).
- **Edges**: timing dependencies (e.g., disbursement before repayment).
- **Weights**: value × timing cost (distance from ideal time, priority, etc.).

## Formalization (v1)

- Set of accounts \( A \)
- Set of events \( E \)
- Time periods \( T = \{0, 1, \dots, T_{max}\} \)
- Binary decision variables \( z_{e,t} \) indicating execution of event \( e \) at time \( t \).

Constraints:
- Each event executes exactly once.
- Execution must stay within its allowed time window.
- Account balances must stay above a minimum liquidity level.
- Optional dependencies (event j cannot execute before event i).

Objective:
- Minimize total timing cost, based on deviation from ideal execution times and priorities.

## Reference Files

- `src/models/sequencing-graph/sequencing_graph_v1.md`
- `src/models/sequencing-graph/sequencing_graph_template.md`
PAGe

#######################################
# Flow-Optimization-Engine.md
#######################################
cat > "$WIKI_DIR/Flow-Optimization-Engine.md" << 'PAGe'
# Flow Optimization Engine (FOE)

The **Flow Optimization Engine (FOE)** chooses *how* and *where* events execute once the Sequencing Graph has chosen *when* they should occur.

## Purpose

Given:
- a sequenced set of events,
- multiple possible rails or routes,

FOE selects the execution route for each event to minimize a composite cost:

- fees + FX cost
- delay / time cost
- risk cost
- liquidity cost

subject to:
- capacity constraints,
- feasibility / policy constraints,
- regulatory or corridor restrictions.

## Reference Files

- `src/models/flow-optimization/foe_rules_v1.md`
PAGe

#######################################
# Liquidity-Time-Curve.md
#######################################
cat > "$WIKI_DIR/Liquidity-Time-Curve.md" << 'PAGe'
# Liquidity-Time Curve

The **Liquidity-Time Curve** measures alignment between:

- available liquidity over time, and
- the timing of obligations.

## Core Functions

For each account:
- Liquidity function \( L_a(t) \)
- Obligation intensity \( O_a(t) \)

Key metrics:
- **Timing mismatch**: when obligations exceed available liquidity.
- **Liquidity stress**: how far an account runs below a desired safety buffer.

These metrics can be compared between:
- Baseline processing, and
- LSI sequencing.

## Reference Files

- `src/models/timing-models/liquidity_time_curve_v1.md`
PAGe

#######################################
# Simulations.md
#######################################
cat > "$WIKI_DIR/Simulations.md" << 'PAGe'
# LSI Simulations

Simulations test how LSI behaves under realistic corridor and timing scenarios.

## Structure

- `scenarios/` — corridor and timing setups.
- `runners/` — code or pseudo-code for executing scenarios.
- `results/` — metrics and plots.

## Example Scenario

**Baseline US → KE Remittance**

- Corridor: US → Kenya
- Users: migrant workers sending salary-linked remittances
- Experiments:
  - Without sequencing (traditional processing)
  - With LSI sequencing
- Metrics:
  - liquidity usage
  - timing mismatch
  - settlement delays

## Reference Files

- `src/simulations/lsi_simulations_overview.md`
- `src/simulations/scenarios/baseline_us_to_ke_remittance.md`
- `src/simulations/runners/python_runner_notes.md`
PAGe

#######################################
# Research-Templates.md
#######################################
cat > "$WIKI_DIR/Research-Templates.md" << 'PAGe'
# Research Templates

The repository includes templates for structured LSI research.

## Abstract Template

Lives under:
- `papers/abstracts/lsi_abstract_template.md`

Defines:
- Problem statement
- Thesis
- Approach
- Key contribution
- Findings
- Implications
- Keywords

## Draft Paper Template

Lives under:
- `papers/drafts/lsi_draft_template.md`

Sections:
- Introduction
- Background & Motivation
- Conceptual Framework
- Model / System Design
- Results / Findings
- Implications
- Limitations
- Future Work
- Conclusion

## Final Paper Template

Lives under:
- `papers/final/lsi_final_paper_template.md`

Organized for publishable, journal-ready structure.
PAGe

#######################################
# Frameworks.md
#######################################
cat > "$WIKI_DIR/Frameworks.md" << 'PAGe'
# Frameworks

High-level conceptual and architectural frameworks for LSI.

## Files

- `frameworks/lsi-core-architecture.md`
- `frameworks/sequencing-layer.md`

These documents explain:
- how LSI fits into existing financial infrastructure,
- what the "sequencing layer" means conceptually,
- how timing-native infrastructure can be layered under products.
PAGe

#######################################
# Lab-Notes.md
#######################################
cat > "$WIKI_DIR/Lab-Notes.md" << 'PAGe'
# Lab Notes

The lab includes structured but flexible spaces for thinking.

## Notes Structure

- `notes/ideas/` — unrefined concepts and hooks.
- `notes/research-notes/` — notes on BIS, IMF, and other research.
- `notes/meeting-notes/` — discussions, planning sessions, feedback.
- `notes/scratch/` — equations, pseudo-code, corridor timing tests.

Additionally:
- `lab-notes/` — higher-level lab reflections and narrative notes.

These areas support rapid iteration. Mature ideas move into:
- `papers/`
- `src/models/`
- `src/architecture/`
PAGe

#######################################
# Contributing.md
#######################################
cat > "$WIKI_DIR/Contributing.md" << 'PAGe'
# Contributing to LSI

The Liquidity Sequencing Lab maintains high standards of:

- research rigor
- documentation clarity
- reproducibility

## Contribution Types

- Research: new concepts or LSI extensions
- Code: models, simulations, analytical tools
- Documentation: architecture, diagrams, clarifications

## Principles

- Precision > volume
- Reproducibility is mandatory
- No vague ideas
- Diagrams must be source-editable

See `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` in the main repo for full details.
PAGe

#######################################
# Glossary.md
#######################################
cat > "$WIKI_DIR/Glossary.md" << 'PAGe'
# Glossary

Key terms used across LSI.

- **Liquidity Sequencing Infrastructure (LSI)** — timing-native framework for organizing liquidity events.
- **Sequencing Graph** — optimization structure deciding when events execute.
- **Flow Optimization Engine (FOE)** — optimizer that chooses how/where events execute.
- **Liquidity-Time Curve** — function of available liquidity vs obligations across time.
- **Timing Mismatch** — misalignment between liquidity and obligations.
- **Liquidity Stress** — how far and how often liquidity falls below a safety buffer.
- **Corridor** — directional flow between monetary zones (e.g., US → KE).
- **Programmable Settlement Window** — configurable timing window for settlement.
PAGe

#######################################
# Getting-Started.md
#######################################
cat > "$WIKI_DIR/Getting-Started.md" << 'PAGe'
# Getting Started with LSI

## Who This Is For

- Researchers in payments, liquidity, and financial stability.
- Practitioners designing payment, remittance, or payroll systems.
- Builders exploring timing-native financial infrastructure.

## Recommended Reading Order

1. [[What is LSI?]]
2. [[Architecture Overview]]
3. [[Sequencing Graph]]
4. [[Liquidity-Time Curve]]
5. [[Flow Optimization Engine]]
6. [[Simulations]]
7. [[Research Templates]]

## Repository Tour

- `papers/` — abstracts, drafts, final papers.
- `src/models/` — core mathematical and algorithmic models.
- `src/architecture/` — system design and deployment notes.
- `src/simulations/` — scenarios, runners, and results.
- `notes/` and `lab-notes/` — working notes and scratch space.

Clone the main repo, then explore models and simulations step by step.
PAGe

#######################################
# _Sidebar.md
#######################################
cat > "$WIKI_DIR/_Sidebar.md" << 'PAGe'
* [[Home]]
* [[What is LSI?]]
* [[Getting Started]]
* [[Architecture Overview]]
* [[Sequencing Graph]]
* [[Flow Optimization Engine]]
* [[Liquidity-Time Curve]]
* [[Simulations]]
* [[Research Templates]]
* [[Frameworks]]
* [[Lab Notes]]
* [[Contributing]]
* [[Glossary]]
PAGe

echo "All wiki pages generated into $WIKI_DIR"
