# Liquidity Sequencing Lab — Roadmap

This roadmap is intentionally simple: it tracks how LSI moves from concept → models → simulations → publishable research.

---

## Phase 0 — Repository Scaffold ✅

- [x] Core folder structure: `/papers`, `/src`, `/notes`, `/diagrams`
- [x] Root docs: `README`, `LICENSE`, `CONTRIBUTING`, `CODE_OF_CONDUCT`, `SECURITY`, `AUTHORS`
- [x] Simulation + architecture placeholders

Status: **Complete**

---

## Phase 1 — Core LSI Models

Goal: Encode the core LSI mechanics in `/src/models`.

- [ ] Finalize **Sequencing Graph** model
- [ ] Define **Liquidity-Time Curve** formalism
- [ ] Specify **Flow Optimization Engine (FOE)** core rules
- [ ] Document all assumptions and constraints

Output:
- Model specs + pseudo-code
- Diagrams in `/diagrams/models`

---

## Phase 2 — Corridor Simulations

Goal: Run timing-aware simulations for key corridors in `/src/simulations`.

- [ ] Baseline US → KE remittance scenario
- [ ] With vs. without LSI sequencing comparison
- [ ] Metrics: liquidity usage, timing mismatch, settlement delays
- [ ] Store results in `/src/simulations/results`

Output:
- Reproducible scenarios
- CSV/JSON metrics
- Visuals in `/diagrams/simulations`

---

## Phase 3 — Papers & Publication

Goal: Turn models + simulations into publishable work in `/papers`.

- [ ] Fill out abstract(s) using `papers/abstracts/lsi_abstract_template.md`
- [ ] Draft working paper(s) in `papers/drafts/`
- [ ] Produce final paper(s) in `papers/final/`
- [ ] Ensure diagrams are stored under `/diagrams/papers`

Output:
- At least one submission-ready paper

---

## Phase 4 — Implementation Sketches (Optional)

Goal: Sketch how LSI would map into real-world systems.

- [ ] Implementation notes (language-agnostic)
- [ ] Deployment patterns for production environments
- [ ] Security and risk considerations extension

Output:
- Implementation guidance (still research-oriented)

