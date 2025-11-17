# LSI Deployment Considerations

## Environments
- Local / Dev  
- Staging / Pre-production  
- Production  

## Core Decisions
- Data store for ledger and events (SQL vs. NoSQL vs. event store).
- Message bus / queue for events (e.g., Kafka-style).
- Separation between sequencing engine and settlement executors.

## Resilience
- Idempotent event handling.
- Replayable event logs.
- Circuit breakers and backpressure for rail outages.

## Observability
- Tracing per sequence.
- Metrics: latency, liquidity usage, timing mismatch.
- Alerts on corridor stress and failed sequences.

