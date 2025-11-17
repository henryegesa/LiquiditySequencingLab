# LSI Components

## Ingress Adapters
- Translate external formats (payroll files, API calls, remittance messages) into normalized events.

## Event Normalizer
- Enforces a canonical event schema (amount, currency, source, destination, time window, priority).

## Sequencing Engine
- Consumes normalized events.
- Builds sequencing graphs (see `/src/models/sequencing-graph`).
- Produces an ordered execution plan.

## Flow Optimization Engine (FOE)
- Applies optimization rules across corridors, currencies, and time windows.
- Minimizes liquidity usage and timing cost.

## Settlement & Routing
- Maps planned executions to concrete rails.
- Handles FX, corridor rules, cut-off times.

## Ledger / State Store
- Tracks balances, holds, commitments, and executed events.

## Interfaces
- Public API for products built on top of LSI.
- Internal tools for operations, monitoring, and analytics.

