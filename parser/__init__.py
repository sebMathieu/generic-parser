from structure import Structure, parse_structure
from export import csv_export, json_export


FORMATS = {"csv": csv_export, "json": json_export}
""" Dictionary of formats associated with the corresponding output functions."""
