# -*- coding: UTF-8 -*-
"""
Export structures to various file format.
"""

import csv
import json
import re

import parser


def file_export(struct, parsed, output_path):
    """
    Export a structure to the given output.

        struct: Structure of depth inferior to 2.
        parsed: List parsed according to the given structure.
        output_path: Output file path.
    """

    # Find format
    match = re.search("\\.([a-zA-Z]{3})", output_path)
    if match is None:
        raise SyntaxError("Output format not regognized from the output file path \"%s\". Available formats: %s" %
                          (output_path, ",".join(parser.FORMATS.keys())))
    exporter = parser.FORMATS[match.group(1)]

    # Write
    with open(output_path, "w") as file:
        exporter(struct, parsed, file)


def json_export(struct, parsed, output):
    """
    Export a structure to the given output in JSON.

        struct: Structure of depth inferior to 2.
        parsed: List parsed according to the given structure.
        output: Output stream.
    """
    converted = [struct.to_json(e) for e in parsed]
    json.dump(converted, output)


def csv_export(struct, parsed, output, header=True, column_separator=';'):
    """
    Export a structure to the given output in CSV.

    Args:
        struct: Structure of depth inferior to 2.
        parsed: List parsed according to the given structure.
        output: Output stream.
        header: Boolean to write a header.
        column_separator: Column separator for the output.
    """

    if struct.depth() == 0:
        return
    elif struct.depth() > 2:
        raise SyntaxError("Export via CSV is limited to structure of a maximal depth of 2 (given %s)." % struct.depth())

    writer = csv.writer(output, delimiter=column_separator)

    # Header
    if header and struct.depth() > 1:
        writer.writerow([str(s) for s in struct.content if s is not None])

    # Data
    if struct.depth() == 1:
        for e in parsed:
            writer.writerow([e])
    else:
        for row in parsed:
            writer.writerow(row)
