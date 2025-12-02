from datetime import datetime, timezone, timedelta

# Safe imports: one class per line so the terminal never wraps them
from src.lsi.sequencing_graph import EventId
from src.lsi.sequencing_graph import Event
from src.lsi.sequencing_graph import Dependency
from src.lsi.sequencing_graph import SequencingGraph

from src.lsi.flow_optimization_engine import FlowOptimizationEngine
from src.lsi.flow_optimization_engine import ExecutionDecision


def build_graph() -> SequencingGraph:
    g = SequencingGraph()

    salary = Event(
        id=EventId("salary_event"),
        actor_id="household_1",
        event_type="income",
        amount=3000.0,
        currency="USD",
        scheduled_time=datetime(2025, 1, 31, 9, 0, 0, tzinfo=timezone.utc),
    )

    rent = Event(
        id=EventId("rent_event"),
        actor_id="household_1",
        event_type="obligation",
        amount=1200.0,
        currency="USD",
        scheduled_time=datetime(2025, 2, 1, 10, 0, 0, tzinfo=timezone.utc),
    )

    g.add_event(salary)
    g.add_event(rent)

    dep = Dependency(
        predecessor=salary.id,
        successor=rent.id,
        kind="temporal",
        metadata={},
    )
    g.add_dependency(dep)

    return g


def run_simulation() -> None:
    graph = build_graph()
    foe = FlowOptimizationEngine(graph)

    # Baseline schedule
    baseline = foe.evaluate_schedule()
    print("Baseline delay cost:", baseline.total_delay_cost)

    # Delayed scenario: rent delayed by 24 hours
    decisions = {}
    for event in graph.events:
        if event.id.value == "rent_event":
            exec_time = event.scheduled_time + timedelta(hours=24)
        else:
            exec_time = event.scheduled_time

        decisions[event.id] = ExecutionDecision(
            execute_at=exec_time,
            use_liquidity_source="default",
        )

    delayed = foe.evaluate_schedule(decisions=decisions, delay_penalty_per_hour=1.0)
    print("Delayed schedule delay cost:", delayed.total_delay_cost)


if __name__ == "__main__":
    run_simulation()
