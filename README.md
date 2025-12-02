# Liquidity Sequencing Lab

**Designing the timing layer of money.**

Liquidity Sequencing Lab is a research and engineering practice building **Liquidity Sequencing Infrastructure (LSI)** – a “global liquidity brain” that orchestrates cash, collateral, and credit across products, entities, and currencies through a single policy engine.

- 🌐 Website: https://henryegesa.github.io/ (Liqudity Sequencing Lab profile / landing page)
- 📖 Wiki (technical docs): https://github.com/henryegesa/LiquiditySequencingLab/wiki
- 📂 This repo: research scaffold, models, architecture, simulations, and notes

---

## What is Liquidity Sequencing Infrastructure (LSI)?

**LSI is the layer that decides _when_ and in what order money moves.**

Instead of treating payments, credit, and collateral as separate products, LSI models them as **interdependent flows over time**. It:

- Ingests events from banks, wallets, payroll engines, and markets  
- Builds a **sequencing graph** of incomes, obligations, and constraints  
- Applies a **policy engine** and **flow optimization** to decide:
  - who gets paid,
  - in what order,
  - from which liquidity source,

subject to risk, regulation, and stability constraints.

The aim is to reduce avoidable liquidity stress for households, firms, and institutions and to make systems more resilient by design.

For a narrative overview, see the website.  
For deeper technical detail, start here in the wiki:

- 👉 [What is LSI?](https://github.com/henryegesa/LiquiditySequencingLab/wiki/What-is-LSI)
- 👉 [Architecture Overview](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Architecture-Overview)
- 👉 [Sequencing Graph](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Sequencing-Graph)

---

## Repository Structure

This repository is the **research backbone** of the lab. The main directories:

- `docs/` – high-level documentation (e.g. glossary, frameworks, architecture notes)
- `frameworks/` – core conceptual frameworks like the LSI architecture and sequencing layer
- `papers/` – abstracts, drafts, and final versions of research papers
- `src/` – code for models, simulations, and tooling (when implemented)
- `simulations/` – scenario definitions, configuration files, and runner notes
- `notes/` – lab notes, ideas, meeting notes, scratch work / derivations
- `lab-notes/` – templates and scaffolding for structured note-taking
- `scratchpad/` or `scratch/` – free-form calculations, pseudocode, and experiments
- `README.md` (this file) – high-level entry point
- `CONTRIBUTING.md` – contribution rules, process, and quality expectations
- `SECURITY.md` – security policy and handling of sensitive research

For more detail on how to navigate notes and research artifacts, see:

- [Lab Notes](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Lab-Notes)
- [Research Templates](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Research-Templates)
- [Simulations](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Simulations)

---

## Core Technical Components

The lab’s work is organized around a small set of core components:

- **Sequencing Graph**  
  Graph-based model of events (incomes, obligations, transfers), dependencies, and timing costs.  
  Wiki: [Sequencing Graph](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Sequencing-Graph)

- **Flow Optimization Engine (FOE)**  
  Optimization layer that chooses ordering, sizing, and liquidity sources for payments under constraints.  
  Wiki: [Flow Optimization Engine](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Flow-Optimization-Engine)

- **Liquidity–Time Curve**  
  Describes how liquidity availability and obligations evolve over time and under stress.  
  Wiki: [Liquidity–Time Curve](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Liquidity-Time-Curve)

- **Simulations**  
  Corridor experiments (e.g., US → Kenya remittances), stress tests, and scenario analysis of candidate LSI designs.  
  Wiki: [Simulations](https://github.com/henryegesa/LiquiditySequencingLab/wiki/Simulations)

---

## Research Agenda

The research agenda is structured around three pillars:

1. **Liquidity Sequencing**  
   Timing as a form of capital; how the ordering of incomes and obligations amplifies or dampens liquidity stress.

2. **Cross-Border Infrastructure**  
   Wallet- and ledger-based architectures that reduce friction and improve transparency across currencies and regulatory zones.

3. **System Design for Economic Stability**  
   Aligning technology, policy, and institutional incentives so that resilience is engineered into the system, rather than outsourced during crises.

Selected papers and writings are linked from the website and will be mirrored here under `papers/` as they evolve.

---

## How to Use This Repository

- If you want **the narrative and high-level framing**:  
  → Start with the website.

- If you want **technical architecture and models**:  
  → Start with the wiki (`What is LSI?`, `Architecture Overview`, `Sequencing Graph`, `Flow Optimization Engine`).

- If you want **artifacts and code**:  
  → Explore `frameworks/`, `papers/`, `simulations/`, and `src/` (as models and runners are implemented).

---

## Contributing

At this stage, the lab is primarily a **single-author research environment** with a structured contribution pathway.

- See **[CONTRIBUTING.md](./CONTRIBUTING.md)** for:
  - Allowed contribution types (research, code, documentation)
  - Process and review expectations
  - Formatting and reproducibility requirements

- See **[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)** for behavior, integrity, and collaboration standards.

Security and responsible disclosure are handled under **[SECURITY.md](./SECURITY.md)**.

---

## Versioning

- **Repo + wiki baseline:** `v0.1.1-lab-sync`  
  First synchronized snapshot of repo and wiki structure.

- **Website narrative:** `v0.2.1-website`  
  LSI framing, research agenda, and “Inside the Lab” links wired to the wiki.

Future versions will track:

- New models and simulations  
- New or updated papers  
- Changes to the LSI architecture or core components
