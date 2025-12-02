from datetime import datetime, timezone, timedelta

from src.lsi.sequencing_graph import EventId
from src.lsi.sequencing_graph import Event
from src.lsi.sequencing_graph import Dependency
from src.lsi.sequencing_graph import SequencingGraph

from src.lsi.flow_optimization_engine import FlowOptimizationEngine
from src.lsi.flow_optimization_engine import ExecutionDecision


def build_graph() -> SequencingGraph:
    g = SequencingGraph()

    # Income: salary
    salary = Event(
        id=EventId("salary_event"),
        actor_id="household_1",
        event_type="income",
        amount=3000.0,
        currency="USD",
        scheduled_time=datetime(2025, 1, 31, 9, 0, 0, tzinfo=timezone.utc),
    )

    # Early obligation: electricity bill BEFORE salary
    electricity = Event(
        id=EventId("electricity_bill_event"),
        actor_id="household_1",
        event_type="obligation",
        amount=200.0,
        currency="USD",
        scheduled_time=datetime(2025, 1, 30, 9, 0, 0, tzinfo=timezone.utc),
    )

    # Obligation: rent AFTER salary
    rent = Event(
        id=EventId("rent_event"),
        actor_id="household_1",
        event_type="obligation",
        amount=1200.0,
        currency="USD",
        scheduled_time=datetime(2025, 2, 1, 10, 0, 0, tzinfo=timezone.utc),
    )

    g.add_event(electricity)
    g.add_event(salary)
    g.add_event(rent)

    # Dependency: salary must come before rent
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
    Liquidity gap v1:
    For obligations: gap = balance_before_event - event.amount
    Negative gap = liquidity stress.
    """

    ordered_ids = graph.topological_order()

    events_with_exec = []
    for eid in ordered_ids:
        event = graph.get_event(eid)
        exec_time = decisions[eid].execute_at
        events_with_exec.append((event, exec_time))

    events_with_exec.sort(key=lambda pair: pair[1])

    balance = 0.0
    gaps = []

    for event, exec_time in events_with_exec:
        if event.event_type == "obligation":
            gap = balance - event.amount
        else:
            gap = balance

        gaps.append(
            {
                "event": event.id.value,
                "event_type": event.event_type,
                "scheduled_time": event.scheduled_time,
                "exec_time": exec_time,
                "balance_before": balance,
                "gap": gap,
            }
        )

        if event.event_type == "income":
            balance += event.amount
        elif event.event_type == "obligation":
            balance -= event.amount

    return gaps


def summarize_gaps(label: str, gaps):
    min_gap = min(g["gap"] for g in gaps)
    stressed = [g for g in gaps if g["gap"] < 0]

    print(f"\n[{label}] Liquidity gap summary:")
    print(f"- min_gap: {min_gap}")
    print(f"- stressed_events_count: {len(stressed)}")
    print("- stressed_events:")
    for g in stressed:
        print(f"  * {g['event']} ({g['event_type']}) gap={g['gap']}")


def run_simulation() -> None:
    graph = build_graph()
    foe = FlowOptimizationEngine(graph)

    # Baseline schedule (events at scheduled_time)
    baseline = foe.evaluate_schedule()

    print("\n=== BASELINE ===")
    print("Delay cost:", baseline.total_delay_cost)

    baseline_gaps = compute_liquidity_gap(graph, baseline.decisions)
    summarize_gaps("BASELINE", baseline_gaps)

    # Delayed rent (24h later)
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
    summarize_gaps("DELAYED", delayed_gaps)


if __name__ == "__main__":
    run_simulation()
