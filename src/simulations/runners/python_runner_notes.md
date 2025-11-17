# Simulation Runner (Python-Oriented Notes)

This file documents how a Python-based runner would execute LSI simulations.

## Steps

1. Load scenario configuration
   - corridor parameters
   - user count, ticket sizes
   - timing windows and shocks

2. Generate events
   - income events
   - remittance requests
   - obligations (bills, debt payments)

3. Build sequencing graph
   - use `/src/models/sequencing-graph`
   - attach timing and value attributes

4. Apply LSI sequencing
   - compute optimal execution order
   - apply Flow Optimization Engine rules

5. Execute settlement
   - simulate mapping to rails
   - apply FX and cut-off rules

6. Record outputs
   - write metrics to `/src/simulations/results`
   - generate plots referenced by `/diagrams`

This file is documentation; actual code can be added later in separate `.py` files.
