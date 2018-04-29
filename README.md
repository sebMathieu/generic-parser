
Description
-----------
Package to simplify the parsing of text files. The structure of the file to parse can be easily described by providing
the separators or regexes with capture groups. The structure can even be specified in a single JSON file.
Running the package with the file to parse as argument and a JSON file describing its structure may output directly
a parsed CSV or JSON file.

Example
-------

Parsing a dictionary from a text file, the following raw text file:

    AB
    Ab, n. Etym: [Of Syriac origin.]

    Defn: The fifth month of the Jewish year according to the
    ecclesiastical reckoning, the eleventh by the civil computation,
    coinciding nearly with August. W. Smith.

    ABACA
    Ab"a*ca, n. Etym: [The native name.]

    Defn: The Manila-hemp plant (Musa textilis); also, its fiber. See
    Manila hemp under Manila.



Structure:

    {
        "name": "word",
        "capture": "([A-Z]+)\n.+?, (.+?)( Etym: .+?)?\n\nDefn: ?(.+?) ?\n\n",
        "content":["word","type",null, {"name":"def", "replace":["\n"," "]}]
    }


JSON output:

    [
      {
        "word": "AB",
        "type": "n.",
        "def": "The fifth month of the Jewish year according to the ecclesiastical reckoning, the eleventh by the civil computation, coinciding nearly with August. W. Smith."
      },
      {
        "word": "ABACA",
        "type": "n.",
        "def": "The Manila-hemp plant (Musa textilis); also, its fiber. See Manila hemp under Manila."
      }
    ]


CSV output:

    word;type;def
    AB;n.;The fifth month of the Jewish year according to the ecclesiastical reckoning, the eleventh by the civil computation, coinciding nearly with August. W. Smith.
    ABACA;n.;"The Manila-hemp plant (Musa textilis); also, its fiber. See Manila hemp under Manila."

Structure documentation
-----------------------

Three type of structure are available: capture structures, separator structures and plain structures.


1. Separator structures

    Structure defining the parsing by finding a separator, for instance ";" for a CSV file.
    Sub-content can be parsed directly with the list parameter. The following structure directly parse a CSV file.

        {
          "sep":"\n",
          "list":";"
        }

2. Capture structures

    Structure where parsing is done using a regex with captures groups. The content list defines the name of the captured
    data. If a group must be ignored, add a null at the corresponding place.

        {
            "capture":"regex with groups",
            "content":["list,"of","structures","strings or",null]
        }

    Note that the "." in regexes includes the newline character.

3. Plain structures

    Base block to provide the key of an element for a json output and to apply regex replacements.
    Regex replacements are given in a list of pair elements, the regex to match and the replacement string.
    Note that names and replacement can be applied to seperator and capture structures too.

        {
            "name":"...",
            "replace":[]
        }