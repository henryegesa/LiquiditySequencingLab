# LSI Architecture Overview

This folder documents the system architecture for Liquidity Sequencing Infrastructure (LSI).

## Layers

1. **Ingress Layer**
   - Accepts events (payroll, remittance, card, account movement).
   - Normalizes into a common event schema.

2. **Sequencing Engine**
   - Applies the models in `/src/models`.
   - Builds sequencing graphs and computes optimal execution order.
   - Interfaces with the Flow Optimization Engine (FOE).

3. **Settlement & Routing Layer**
   - Maps sequenced events into specific rails (ACH, wires, card networks, wallets, RTGS).
   - Handles currency conversion and corridor-specific rules.

4. **State & Ledger Layer**
   - Stores balances, commitments, holds, and pending events.
   - Could be implemented using ledgers, event stores, or hybrid.

5. **Interfaces**
   - API (REST/GraphQL/gRPC) for partners and applications.
   - Admin and analytics interfaces.

## Files
- `core_diagram.md` — text description of the main architecture diagram.
- `components.md` — major components, responsibilities, and dependencies.
- `deployment.md` — environments and deployment topologies.

