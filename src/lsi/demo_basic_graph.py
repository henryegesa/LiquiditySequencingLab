from datetime import datetime, timezone
from .sequencing_graph import EventId, Event, Dependency, SequencingGraph


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


if __name__ == "__main__":
    graph = build_simple_household_graph()
    order = graph.topological_order()

    print("Topological order:")
    for eid in order:
        event = graph.get_event(eid)
        print(f"- {eid.value} ({event.event_type}, {event.amount})")
