from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

# Import each class separately to avoid line-wrapping issues
from .sequencing_graph import EventId
from .sequencing_graph import Event
from .sequencing_graph import SequencingGraph


@dataclass
class ExecutionDecision:
    execute_at: datetime
    use_liquidity_source: str = "default"


@dataclass
class ScheduleResult:
    decisions: Dict[EventId, ExecutionDecision]
    total_delay_cost: float
    details: Dict[str, float]


class FlowOptimizationEngine:
    """
    v1 skeleton of the Flow Optimization Engine (FOE).
    """

    def __init__(self, graph: SequencingGraph) -> None:
        self.graph = graph

    def _baseline_schedule(self) -> Dict[EventId, ExecutionDecision]:
        decisions: Dict[EventId, ExecutionDecision] = {}
        for event in self.graph.events:
            decisions[event.id] = ExecutionDecision(
                execute_at=event.scheduled_time,
                use_liquidity_source="baseline",
            )
        return decisions

    def evaluate_schedule(
        self,
        decisions: Optional[Dict[EventId, ExecutionDecision]] = None,
        delay_penalty_per_hour: float = 1.0,
    ) -> ScheduleResult:

        if decisions is None:
            decisions = self._baseline_schedule()

        total_delay_cost = 0.0

        for event in self.graph.events:
            decision = decisions.get(event.id)
            if decision is None:
                continue

            scheduled = event.scheduled_time
            actual = decision.execute_at

            delay_seconds = (actual - scheduled).total_seconds()

            if delay_seconds > 0:
                delay_hours = delay_seconds / 3600.0
                total_delay_cost += delay_hours * delay_penalty_per_hour

        details = {
            "delay_penalty_per_hour": delay_penalty_per_hour,
        }

        return ScheduleResult(
            decisions=decisions,
            total_delay_cost=total_delay_cost,
            details=details,
        )
