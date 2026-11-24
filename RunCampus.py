"""
Project 2: USI Pathfinder -- simulator + verification.

Do not modify this supplied simulator. Complete
pathfinder.py instead.

Run: python RunCampus.py
Prints a Final Token after the tests and schedule checks pass.
"""

import base64
import hashlib
import sys
import unittest

from CampusMap import EDGES, WAYPOINTS
from pathfinder import Graph, campus_route

ASSIGNMENT_ID = "PROJECT2"

# 10 simulated student schedules, each 3+ stops across a day.
SCHEDULES = [
    ["RH1", "BEC", "LIB", "RH1"],
    ["RH2", "UC", "SCI", "RH2"],
    ["RH1", "HP", "SCI", "REC"],
    ["RH2", "REC", "PAC", "RH2"],
    ["RH1", "UC", "LIB", "PAC"],
    ["RH2", "SCI", "HP", "PARK"],
    ["RH1", "REC", "UC", "BEC"],
    ["RH2", "LIB", "PARK", "RH2"],
    ["RH1", "BEC", "SCI", "UC", "RH1"],
    ["RH2", "PAC", "LIB", "SCI", "RH2"],
]

# Close SCI–UC after schedule 5, then check the earlier routes again.
CLOSURE_EDGE = ("SCI", "UC")


def get_student_id() -> str:
    """Ask for the USI username to include in the run's token."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print("  ALL SIMULATED STUDENTS ROUTED SUCCESSFULLY")
    print(f"  STUDENT: {student_id}")
    print(f"  FINAL TOKEN (paste this into Blackboard, and screenshot this output):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def route_schedule(graph: Graph, schedule: list):
    """Route every leg of a multi-stop schedule. Return the full leg list, or None if any leg fails."""
    legs = []
    for a, b in zip(schedule, schedule[1:]):
        result = campus_route(graph, a, b)
        if result is None:
            return None
        legs.append(result)
    return legs


def path_uses_edge(path: list, a: str, b: str) -> bool:
    for u, v in zip(path, path[1:]):
        if {u, v} == {a, b}:
            return True
    return False


def main() -> int:
    from TestPathfinder import PathfinderChecks
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PathfinderChecks)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        print("Behavioral checks failed. No token issued.")
        return 1

    failures: list = []

    graph = Graph()
    for node in WAYPOINTS:
        graph.add_node(node)
    for a, b, weight in EDGES:
        graph.add_edge(a, b, weight)

    print(f"Routing schedules 1-5 (before the closure event)...\n")
    pre_closure_results = []
    for i, schedule in enumerate(SCHEDULES[:5], start=1):
        legs = route_schedule(graph, schedule)
        ok = legs is not None
        check(f"schedule {i} ({' -> '.join(schedule)}) routes successfully", ok, failures)
        pre_closure_results.append(legs)

    if failures:
        print(f"\n{len(failures)} check(s) failed before the closure event. No token issued.")
        return 1

    print(f"\nTriggering closure event: {CLOSURE_EDGE[0]} <-> {CLOSURE_EDGE[1]}...\n")
    graph.close_edge(*CLOSURE_EDGE)

    print("Re-routing schedules 1-5 (should be unaffected if they didn't use the closed edge,")
    print("or successfully reroute around it if they did)...\n")
    reroute_forced = False
    for i, (schedule, old_legs) in enumerate(zip(SCHEDULES[:5], pre_closure_results), start=1):
        new_legs = route_schedule(graph, schedule)
        check(f"schedule {i} still routes successfully after the closure", new_legs is not None, failures)
        if new_legs is None:
            continue
        for old_leg, new_leg in zip(old_legs, new_legs):
            _, old_path = old_leg
            _, new_path = new_leg
            check(f"schedule {i} leg {old_path[0]}->{old_path[-1]}: post-closure route avoids the closed edge", not path_uses_edge(new_path, *CLOSURE_EDGE), failures)
            if old_path != new_path:
                reroute_forced = True

    check("at least one schedule was actually forced to change its route by the closure", reroute_forced, failures)

    print(f"\nRouting schedules 6-10 (computed entirely after the closure)...\n")
    for i, schedule in enumerate(SCHEDULES[5:], start=6):
        legs = route_schedule(graph, schedule)
        ok = legs is not None
        check(f"schedule {i} ({' -> '.join(schedule)}) routes successfully post-closure", ok, failures)
        if legs is not None:
            for _, path in legs:
                check(f"schedule {i} leg {path[0]}->{path[-1]} avoids the closed edge", not path_uses_edge(path, *CLOSURE_EDGE), failures)

    print("\nReopening the edge and confirming the graph recovers...\n")
    graph.reopen_edge(*CLOSURE_EDGE)
    reopened_ok = all(route_schedule(graph, s) is not None for s in SCHEDULES)
    check("all 10 schedules still route successfully after reopening", reopened_ok, failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
