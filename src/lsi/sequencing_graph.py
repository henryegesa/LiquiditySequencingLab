from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class EventId:
    """
    Identifier for a financial event in the sequencing graph.

    Example: "household_1:salary:2025-01-31T09:00:00Z"
    """
    value: str


@dataclass
class Event:
    """
    A single financial event: income, obligation, transfer, etc.
    This is the core node type in the sequencing graph.
    """

    id: EventId
    actor_id: str            # household, firm, intermediary, etc.
    event_type: str          # "income", "obligation", "transfer", etc.
    amount: float
    currency: str
    scheduled_time: datetime

    # Optional fields for richer modeling later
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class Dependency:
    """
    Directed dependency between two events.
    Example: rent_payment depends on salary_being_received.
    """

    predecessor: EventId  # must happen before
    successor: EventId    # must not be executed before predecessor
    kind: str = "temporal"  # could later support "policy", "risk", etc.
    metadata: Dict[str, str] = field(default_factory=dict)


class SequencingGraph:
    """
    Core graph structure for Liquidity Sequencing Infrastructure (LSI).

    - Nodes are financial events.
    - Edges (dependencies) encode ordering and constraints.
    - This class does NOT optimize; it just holds structure and
      basic operations (add, validate, topological ordering).
    """

    def __init__(self) -> None:
        # Store events by ID
        self._events: Dict[EventId, Event] = {}
        # Adjacency lists for dependencies
        self._successors: Dict[EventId, List[EventId]] = {}
        self._predecessors: Dict[EventId, List[EventId]] = {}

    # ------------------------------------------------------------------
    # Event management
    # ------------------------------------------------------------------
    def add_event(self, event: Event) -> None:
        """
        Add a new event to the graph.
        Raises ValueError if the ID already exists.
        """
        if event.id in self._events:
            raise ValueError(f"Event with id {event.id.value!r} already exists")

        self._events[event.id] = event
        self._successors.setdefault(event.id, [])
        self._predecessors.setdefault(event.id, [])

    def get_event(self, event_id: EventId) -> Event:
        """
        Look up an event by ID. Raises KeyError if missing.
        """
        return self._events[event_id]

    # ------------------------------------------------------------------
    # Dependency management
    # ------------------------------------------------------------------
    def add_dependency(self, dep: Dependency) -> None:
        """
        Add a directed dependency edge between two existing events.

        Raises:
            KeyError   – if either event is missing.
            ValueError – if this would introduce a cycle (for v1 we can
                         leave cycle detection as a TODO or simple check).
        """
        if dep.predecessor not in self._events:
            raise KeyError(f"Unknown predecessor event: {dep.predecessor.value!r}")
        if dep.successor not in self._events:
            raise KeyError(f"Unknown successor event: {dep.successor.value!r}")

        self._successors.setdefault(dep.predecessor, []).append(dep.successor)
        self._predecessors.setdefault(dep.successor, []).append(dep.predecessor)

        # TODO: cycle detection and validation can be added later.

    # ------------------------------------------------------------------
    # Basic graph queries
    # ------------------------------------------------------------------
    @property
    def events(self) -> List[Event]:
        """Return all events in the graph."""
        return list(self._events.values())

    def predecessors(self, event_id: EventId) -> List[EventId]:
        """Return direct predecessors of the given event."""
        return self._predecessors.get(event_id, [])

    def successors(self, event_id: EventId) -> List[EventId]:
        """Return direct successors of the given event."""
        return self._successors.get(event_id, [])

    # ------------------------------------------------------------------
    # Topological ordering (naive)
    # ------------------------------------------------------------------
    def topological_order(self) -> List[EventId]:
        """
        Compute a topological ordering of the events.

        This is a naive Kahn-style implementation.
        Raises ValueError if it detects a cycle.
        """
        # Compute in-degrees
        in_degree: Dict[EventId, int] = {
            eid: len(preds) for eid, preds in self._predecessors.items()
        }

        # Nodes with no predecessors
        zero_in_degree: List[EventId] = [
            eid for eid in self._events.keys() if in_degree.get(eid, 0) == 0
        ]

        order: List[EventId] = []
        idx = 0

        while idx < len(zero_in_degree):
            current = zero_in_degree[idx]
            idx += 1
            order.append(current)

            for succ in self._successors.get(current, []):
                in_degree[succ] = in_degree.get(succ, 0) - 1
                if in_degree[succ] == 0:
                    zero_in_degree.append(succ)

        if len(order) != len(self._events):
            raise ValueError("Graph contains a cycle or disconnected dependency structure")

        return order

    # ------------------------------------------------------------------
    # Placeholders for integration with the Flow Optimization Engine
    # ------------------------------------------------------------------
    def compute_timing_costs(self) -> Dict[EventId, float]:
        """
        Placeholder for timing cost computation.

        In later versions, this will:
        - compare scheduled_time vs candidate execution time,
        - apply cost functions for delay, pre-emption, etc.,
        - feed into the Flow Optimization Engine.

        For v1, we return an empty mapping.
        """
        return {}
