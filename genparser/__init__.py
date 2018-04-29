from .structure import Structure, parse_structure
from .export import file_export, csv_export, json_export


FORMATS = {"csv": csv_export, "json": json_export}
""" Dictionary of formats associated with the corresponding output functions."""
