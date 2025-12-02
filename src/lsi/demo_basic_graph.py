from datetime import datetime, timezone

from .sequencing_graph import EventId
from .sequencing_graph import Event
from .sequencing_graph import Dependency
from .sequencing_graph import SequencingGraph
from .flow_optimization_engine import FlowOptimizationEngine


def build_simple_household_graph() -> SequencingGraph:
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
        metadata={},  # kept empty on purpose to avoid paste issues
    )
    g.add_dependency(dep)

    return g


def main() -> None:
    graph = build_simple_household_graph()

    print("Topological order:")
    order = graph.topological_order()
    for eid in order:
        event = graph.get_event(eid)
        print(f"- {eid.value} ({event.event_type}, {event.amount})")

    foe = FlowOptimizationEngine(graph)
    result = foe.evaluate_schedule()

    print("\nFlow Optimization Engine result:")
    print(f"- total_delay_cost: {result.total_delay_cost}")
    print(f"- decisions: {len(result.decisions)} events scheduled")


if __name__ == "__main__":
    main()
