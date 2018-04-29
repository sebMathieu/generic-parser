# -*- coding: UTF-8 -*-
"""
Description of the structure of the file to parse.
"""

import json
import re
from typing import List


class Structure:
    """
    Structure to parse.

    Attributes:
        name: Name of the field.
        replace: List of 2-tuples with regexes and replacement string.
    """

    def __init__(self, name=None):
        self.name = name
        self.replace = []

    def __str__(self):
        if self.name is None:
            return ""
        else:
            return self.name

    def to_json(self, parsed):
        """
        Transpose the parsed content to JSON data using the key given by the names in the structure.

        Args:
            parsed: Content associated to the structure

        Returns:
            Dictionary.
        """

        if self.name is None:
            raise ValueError("Each part of the structure must be named to generate a dictionary from a structure.")
        return {self.name: parsed}

    def _clean_str(self, s: str):
        """ Clean the parsed content according to the rules of the structure.

        Args:
            s: String to clean.

        Returns:
            Cleaned string.
        """
        for r, c in self.replace:
            s = r.sub(c, s)
        return s

    def parse_file(self, file_path, bufsize=65536):
        """
        Parse a file following a given structure.

        Args:
            file_path: Path to the file.
            bufsize: Buffer size as a positive integer. If none, read line by line.

        Returns:
             Parsed content as a list.
        """

        content = [""]  # Current content read
        parsed = []
        with open(file_path) as file:
            if bufsize is None:
                for line in file:
                    content[0] += line
                    self.parse(content, parsed)
            else:
                while True:
                    s = file.read(bufsize)
                    if s == '':
                        break
                    content[0] += s
                    while self.parse(content, parsed):
                        pass

        return parsed

    def parse(self, container, parsed):
        """
        Recursive function to parse a string from a structure.

        Args:
            container: List of one string.
            parsed: List to receive the parsed content.

        Returns:
            Boolean true if something as been found.
        """

        parsed.append(self._clean_str(container[0]))
        container[0] = ""
        return True

    def depth(self):
        """
        Get the maximum depth of the structure.


        Returns:
             Positive integer.
        """
        return 0


class SeparatorStructure(Structure):
    """
    Structure parsing based on a separator.

    Attributes:
        separator: Regex with the separator.
        list: List separator.
        content: Array of sub-structures or strings.
    """

    def __init__(self, separator, name=None):
        super().__init__(name)
        self.separator = separator
        self.list = None
        self.content = []

    def parse(self, container: List[str], parsed: list):
        # Search
        match = self.separator.search(container[0])
        if match is None:
            return

        # Define content
        content = [self._clean_str(container[0][:match.start()])]
        try:
            container[0] = container[0][match.end():]
        except IndexError:
            container[0] = ""

        # Sub-content
        p = []
        if len(self.content) > 0:
            for s in self.content:
                s.parse(content, p)

        if self.list is not None:
            m = self.list.search(content[0])
            while m is not None:
                p.append(content[0][:m.start()])
                content[0] = content[0][m.end():]
                m = self.list.search(content[0])
            p.append(content[0])

        # Add to the data
        if len(p) > 0:
            parsed.append(p)
        elif len(content[0]) > 0:
            parsed.append(content[0])

        return True

    def depth(self):
        d = 0 if self.list is None else 1
        for s in self.content:
            if isinstance(s, Structure):
                d = max(d, s.depth())
        return 1 + d

    def to_json(self, parsed):
        if len(self.content) == 0 and self.list is None:
            return super().to_json(parsed)

        j = 0
        data = []
        for i, p in enumerate(parsed):
            # Skip none
            while j < len(self.content) and self.content[j] is None:
                j += 1

            if j < len(self.content):
                s = self.content[j]
                j += 1
                if type(s) in (CaptureStructure, SeparatorStructure):
                    data.append(s.to_json(p))
                else:
                    data.append(p)
            else:
                data.append(p)

        return data


class CaptureStructure(Structure):
    """
    Structure parsing by capture.

    Attributes:
        capture: Regex with the capture with at most one capture group. The first group is used.
        content: Array of sub-structures or strings.
    """

    def __init__(self, capture, name=None):
        super().__init__(name)
        self.capture = capture
        self.content = []

    def parse(self, container: List[str], parsed: list):
        # Search
        match = self.capture.search(container[0])
        if match is None:
            return

        if self.capture.groups == 1 and self.content is None or len(self.content) == 0:
            parsed.append(self._clean_str(match.group(1)))
        else:
            # Get content
            captured = []
            parsed.append(captured)
            for i, s in enumerate(self.content):
                if s is None:
                    continue

                c = self._clean_str(match.group(i + 1))
                if isinstance(s, Structure):
                    s.parse([c], captured)
                else:
                    captured.append(c)

        # Keep the rest
        try:
            container[0] = container[0][match.end():]
        except IndexError:
            container[0] = ""

        return True

    def depth(self):
        d = 0
        for s in self.content:
            if isinstance(s, Structure):
                d = max(d, s.depth())
        if len(self.content) > 1:
            d += 1
        return 1 + d

    def to_json(self, parsed):
        if len(self.content) == 0:
            return super().to_json(parsed)

        j = 0
        dic = {}
        for i in range(len(parsed)):
            # Skip none
            while self.content[j] is None:
                j += 1

            s = self.content[j]
            if type(s) in (CaptureStructure, SeparatorStructure):
                dic[s.name] = s.to_json(parsed[i])
            elif type(s) == Structure:  # but no sub-structures then
                dic[s.name] = parsed[i]
            else:
                dic[s] = parsed[i]

            j += 1

        return dic


def parse_structure(file_path: str):
    """
    Parse a JSON file containing the structure of files to parse.

    Args:
        file_path: Path to the JSON file with the structure.

    Returns:
         Structure tree.

    """
    try:
        with open(file_path, "r") as file:
            return dictionary2structure(json.load(file))
    except json.JSONDecodeError as e:
        raise SyntaxError("Invalid JSON file \"%s\". %s" % (file_path, e))


def dictionary2structure(dico: dict):
    """
    Convert a dictionary obtained from JSON to a structure tree.

    Args:
        dico: Dictionary.

    Returns:
        Structure tree.
    """

    s = None

    # Separator
    try:
        regex_text = dico["sep"]
        s = SeparatorStructure(re.compile(regex_text, re.DOTALL))

        # List
        regex_text = dico["list"]
        s.list = re.compile(regex_text, re.DOTALL)
    except KeyError:
        pass

    # Capture
    if s is None:
        try:
            regex_text = dico["capture"]
            s = CaptureStructure(re.compile(regex_text, re.DOTALL))
            if s.capture.groups < 1:
                raise SyntaxError("Invalid capture regex expression \"%s\", no group found." % s.capture)
        except KeyError:
            pass

    # Invalid structure
    if s is None:
        s = Structure()

    # Name
    try:
        s.name = dico["name"]
    except KeyError:
        pass

    # Content
    try:
        content = dico['content']
        s.content = [d if d is None or type(d) == str else dictionary2structure(d) for d in content]
        if type(s) == CaptureStructure and s.capture.groups > 1 and len(s.content) != s.capture.groups:
            raise SyntaxError(
                "The length of the content list associated  with the capture regex expression \"%s\" must be equal to the number of groups, %s instead of %s." % (
                    s.capture, s.capture.groups, len(s.content)))
    except KeyError:
        if type(s) == CaptureStructure and s.capture.groups > 1:
            raise SyntaxError("A content list must be specified with the capture regex expression \"%s\"." % s.capture)

    # Replace
    try:
        replace_in = dico['replace']
        if len(replace_in) % 2 != 0:
            raise SyntaxError(
                "Invalid replacement input. Replacement are only performed by group of two. Input: %s" % replace_in)

        i = 0
        while i < len(replace_in):
            s.replace.append((re.compile(replace_in[i], re.DOTALL), replace_in[i + 1]))
            i += 2
    except KeyError:
        pass

    return s
