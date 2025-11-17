# Scenario: Baseline US → KE Remittance

## Purpose
Baseline simulation of a US-to-Kenya remittance corridor under typical monthly flows.

## Inputs
- Corridor: US → KE
- Users: migrant workers sending salary-linked remittances
- Frequency: 1–4 transfers per month per user
- Rail mix: ACH/card → LSI → mobile money

## Parameters
- Number of senders: N
- Average ticket size: X USD
- FX spread: s
- Cut-off times: t_c
- Timing window: monthly salary cycle

## Experiments
1. Run without sequencing (traditional batch remit).
2. Run with LSI sequencing enabled.
3. Compare:
   - liquidity usage
   - timing mismatch
   - settlement delays

## Outputs
- corridor_liquidity_usage.csv
- timing_mismatch_metrics.csv
- charts in `/diagrams` (optional)
