from datetime import datetime, timezone, timedelta

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


def compute_liquidity_gap(graph: SequencingGraph, decisions):
    """
    Compute the liquidity balance over time and the liquidity gap.
    Gap = balance_before_event - event_amount (negative = stress)
    """

    # Sort events in execution order
    ordered_ids = graph.topological_order()

    # Convert IDs to event objects with execution times
    events_with_exec = []
    for eid in ordered_ids:
        event = graph.get_event(eid)
        exec_time = decisions[eid].execute_at
        events_with_exec.append((event, exec_time))

    # Sort again by actual execution time (important when delays occur)
    events_with_exec.sort(key=lambda pair: pair[1])

    balance = 0.0
    gaps = []

    for event, exec_time in events_with_exec:
        # Liquidity gap BEFORE executing the event
        gap = balance - event.amount if event.event_type == "obligation" else balance

        gaps.append({
            "event": event.id.value,
            "event_type": event.event_type,
            "scheduled_time": event.scheduled_time,
            "exec_time": exec_time,
            "balance_before": balance,
            "gap": gap,
        })

        # Update balance AFTER event executes
        if event.event_type == "income":
            balance += event.amount
        elif event.event_type == "obligation":
            balance -= event.amount

    return gaps


def run_simulation() -> None:
    graph = build_graph()
    foe = FlowOptimizationEngine(graph)

    # Baseline schedule
    baseline = foe.evaluate_schedule()

    print("\n=== BASELINE ===")
    print("Delay cost:", baseline.total_delay_cost)

    baseline_gaps = compute_liquidity_gap(graph, baseline.decisions)

    print("\nLiquidity Gaps (Baseline):")
    for g in baseline_gaps:
        print(g)

    # Delayed rent scenario
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

    delayed = foe.evaluate_schedule(decisions=decisions)

    print("\n=== DELAYED RENT (24h) ===")
    print("Delay cost:", delayed.total_delay_cost)

    delayed_gaps = compute_liquidity_gap(graph, delayed.decisions)

    print("\nLiquidity Gaps (Delayed Scenario):")
    for g in delayed_gaps:
        print(g)


if __name__ == "__main__":
    run_simulation()
