"""
Project 2: USI Pathfinder -- given campus dataset.

A small model of the USI campus: waypoints (buildings/junctions) with
coordinates, and walkable edges with travel-time weights (minutes).
Not the real USI campus layout -- a representative stand-in sized for
a semester project. Do not modify this file.
"""

WAYPOINTS = {
    "BEC": (0, 0),      # Business & Engineering Center
    "SCI": (2, 1),      # Science Center
    "LIB": (4, 2),      # Library
    "UC": (2, 3),       # University Center
    "RH1": (0, 4),      # Residence Hall 1
    "RH2": (1, 5),      # Residence Hall 2
    "REC": (4, 5),      # Recreation, Fitness & Wellness Center
    "PAC": (5, 3),      # Performance & Arts Center
    "PARK": (6, 1),     # Parking Garage
    "HP": (3, 0),       # Health Professions Building
}

# (node_a, node_b, weight_in_minutes) -- undirected
EDGES = [
    ("BEC", "SCI", 4),
    ("BEC", "HP", 5),
    ("SCI", "LIB", 3),
    ("SCI", "UC", 3),
    ("SCI", "HP", 3),
    ("UC", "LIB", 2),
    ("UC", "RH1", 4),
    ("UC", "RH2", 3),
    ("RH1", "RH2", 2),
    ("RH2", "REC", 3),
    ("UC", "REC", 5),
    ("LIB", "PAC", 3),
    ("REC", "PAC", 4),
    ("PAC", "PARK", 3),
    ("LIB", "PARK", 5),
    ("HP", "PARK", 6),
]
