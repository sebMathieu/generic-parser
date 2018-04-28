# -*- coding: UTF-8 -*-
"""General parser - version 0.1
Generic text parser from a JSON structure using regex or separator.

Usage:
    parser [options] <structure> <file2parse>

Options:
    -h               Display this help.
    -o OUTPUT_PATH   Output to a file, JSON or CSV (if the structure allows it).
    -f FORMAT        Chooses the output format in the command line and disable other prints.

The structure must be given as a JSON file. See provided example in structures and the readme file.
"""

import sys, os, io

from docopt import docopt

# Relative import fixes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import structure, export
import parser


def main(args):
    """
    Main routine.

    :param args: Arguments dictionary read by docopt.
    """
    try:
        # Output path
        output_path = args["-o"]

        # Read structure
        struct = structure.parse_structure(args["<structure>"])
        if output_path is not None:
            print("Parsing structure read of depth %s." % struct.depth())

        # Parse file
        parsed = struct.parse_file(args["<file2parse>"])
        if output_path is not None:
            print("%s elements parsed." % len(parsed))

        # Output
        output_path = args["-o"]
        if args["-f"] is None and output_path is not None:
            export.file_export(struct, parsed, output_path)
            print("The file has been \"%s\" written." % output_path)
        else:
            # Get format
            if args["-f"] is None:
                format = "json"
            else:
                format = args["-f"].lower()

            try:
                if output_path is None:
                    parser.FORMATS[format](struct, parsed, sys.__stdout__)
                else:
                    with open(output_path, "w") as file:
                        parser.FORMATS[format](struct, parsed, file)
            except KeyError:
                raise SyntaxError("Unkown output format: \"%s\". Available formats: %s" % (format, ",".join(parser.FORMATS.keys())))

    except (FileNotFoundError, SyntaxError) as e:
        print(e, file=sys.stderr)
        exit(1)


# Python entry point
if __name__ == "__main__":  # pragma: no cover
    args = docopt(__doc__)
    main(args)
