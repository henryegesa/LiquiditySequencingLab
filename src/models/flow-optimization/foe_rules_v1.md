# Flow Optimization Engine (FOE) — Version 1 Rules

The Flow Optimization Engine (FOE) sits on top of the **sequencing graph** and **Liquidity-Time Curve**.  
Its purpose: choose **how** and **where** to execute events (rails, corridors, paths) while respecting timing and liquidity constraints.

---

## 1. Core Idea

Given:
- a sequenced set of events over time, and
- multiple possible **execution options** (rails / routes),

FOE selects the combination of options that:
- satisfies constraints, and
- minimizes a composite cost function (time, liquidity, FX, fees, risk).

---

## 2. Sets and Indices

- \( E \) — set of events (from sequencing graph).
- \( R \) — set of available **routes/rails**, indexed by \( r \).
  - Example: ACH, card, instant rail, wallet, internal netting.
- \( T \) — time periods, as before.

For each event \( e \), there may be one or more feasible routes \( R_e \subseteq R \).

---

## 3. Route-Level Parameters

For each event–route pair \( (e, r) \):

- \( \kappa_{e,r} \) — **base fee** (fixed or percentage).
- \( \phi_{e,r} \) — **FX cost** (if cross-currency).
- \( \delta_{e,r} \) — **expected settlement delay** (time units).
- \( \rho_{e,r} \) — **operational risk weight** (e.g., failure probability, dispute risk).
- \( \lambda_{e,r} \) — **liquidity impact factor**, how much liquidity is locked or required.
- Feasibility indicator:
  \[
  f_{e,r} \in \{0,1\} \quad (\text{1 if route } r \text{ can execute event } e)
  \]

---

## 4. Decision Variables

For each event–route pair \( (e, r) \):

- \( x_{e,r} \in \{0,1\} \)

Interpretation:
- \( x_{e,r} = 1 \) if event \( e \) is executed via route \( r \).
- Each event must be assigned exactly one route among its feasible options.

---

## 5. Assignment Constraints

### 5.1. One route per event

\[
\sum_{r \in R_e} x_{e,r} = 1 \quad \forall e \in E
\]

### 5.2. Route feasibility

\[
x_{e,r} \le f_{e,r} \quad \forall e \in E,\ \forall r \in R
\]

If a route isn’t feasible for a given event, it cannot be chosen.

---

## 6. Cost Components

Define route-specific cost components, which FOE will trade off.

### 6.1. Fee + FX cost

\[
C^{\text{fee+fx}} = \sum_{e \in E} \sum_{r \in R_e} (\kappa_{e,r} + \phi_{e,r}) \cdot x_{e,r}
\]

### 6.2. Delay / Time cost

We can express delay as:

\[
C^{\text{delay}} = \sum_{e \in E} \sum_{r \in R_e} \eta_e \cdot \delta_{e,r} \cdot x_{e,r}
\]

Where:
- \( \eta_e \) is a sensitivity weight for event \( e \) (e.g., urgent rent vs. non-urgent transfer).

### 6.3. Risk cost

\[
C^{\text{risk}} = \sum_{e \in E} \sum_{r \in R_e} \rho_{e,r} \cdot x_{e,r}
\]

### 6.4. Liquidity cost

Link to liquidity usage (e.g., how much liquidity is locked and for how long):

\[
C^{\text{liq}} = \sum_{e \in E} \sum_{r \in R_e} \lambda_{e,r} \cdot x_{e,r}
\]

Parameters \( \lambda_{e,r} \) are derived from how the route interacts with the Liquidity-Time Curve.

---

## 7. Composite FOE Objective

FOE minimizes a **weighted sum** of the above components:

\[
\min_{x} \quad \alpha \cdot C^{\text{fee+fx}}
              + \beta \cdot C^{\text{delay}}
              + \gamma \cdot C^{\text{risk}}
              + \theta \cdot C^{\text{liq}}
\]

Where:
- \( \alpha, \beta, \gamma, \theta \ge 0 \) are tunable weights that encode platform preferences or policy.

Subject to:
- assignment constraints
- route feasibility
- any capacity or regulatory constraints (below).

---

## 8. Capacity and Policy Constraints (Optional v1 Extensions)

### 8.1. Route capacity

If route \( r \) has a maximum volume capacity \( \text{Cap}_r \):

\[
\sum_{e \in E} |a_e| \cdot x_{e,r} \le \text{Cap}_r \quad \forall r \in R
\]

### 8.2. Regulatory / policy constraints

Examples:
- Certain events must use specific routes (e.g., large-value, high-KYC events).
- Certain jurisdictions disallow specific routes.

Encode via:

\[
x_{e,r} = 0 \quad \text{if route } r \text{ is disallowed for event } e
\]

This is handled by \( f_{e,r} \) or separate constraint sets.

---

## 9. Integration with Sequencing Graph

Sequence first, then optimize routes:

1. **Sequencing graph** selects \( \hat{t}_e \) for each event \( e \).
2. This defines the timing dimension for all events.
3. FOE then optimizes **how** to execute each event given its scheduled time.

In future versions, a joint model can be explored, but v1 keeps them **separable**:
- Sequencing = timing optimization  
- FOE = route optimization conditioned on timing  

---

## 10. Output

FOE outputs:
- \( x_{e,r} \) for all event–route pairs
- Implied:
  - selected rail per event
  - implied fee, FX, delay, risk, and liquidity profile
- Aggregated corridor-level metrics:
  - total fees
  - average delay
  - risk score
  - liquidity efficiency

These outputs can be consumed by:
- simulations in `/src/simulations`
- reporting for `/papers`
- diagrams in `/diagrams/models` and `/diagrams/simulations`

---

## 11. Next Steps (v2+)

Potential enhancements:
- stochastic route failures and robustness optimization  
- dynamic re-routing when a rail fails or is congested  
- multi-hop routing across corridors  
- game-theoretic extensions (competing rails or providers)  

