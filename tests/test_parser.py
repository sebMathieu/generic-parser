# -*- coding: utf-8 -*-

import os
import unittest
import io

import genparser


class TestParser(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Set the working directory to the root.

    def test_list(self):
        struct = genparser.parse_structure("structures/list.json")
        self.assertEqual(struct.depth(), 2)

        # Parse
        l = struct.parse_file("data/list.txt")
        self.assertListEqual(l, [['1', 'A', '?'], ['2', 'B', ','], ['3', 'C', '%']])

        # JSON output
        out = io.StringIO()
        genparser.json_export(struct, l, out, None)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, '[[{"number": "1"}, "A", "?"], [{"number": "2"}, "B", ","], [{"number": "3"}, "C", "%"]]')

        # CSV output
        out = io.StringIO()
        genparser.csv_export(struct, l, out)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, "number\r\n1;A;?\r\n2;B;,\r\n3;C;%\r\n")

    def test_list2(self):
        struct = genparser.parse_structure("structures/list2.json")
        self.assertEqual(struct.depth(), 2)

        # Parse
        l = struct.parse_file("data/list.txt")
        self.assertListEqual(l, [['1', 'A', '?'], ['2', 'B', ','], ['3', 'C', '%']])

        # JSON output
        out = io.StringIO()
        genparser.json_export(struct, l, out, None)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, '[["1", "A", "?"], ["2", "B", ","], ["3", "C", "%"]]')

        # CSV output
        out = io.StringIO()
        genparser.csv_export(struct, l, out)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, "\r\n1;A;?\r\n2;B;,\r\n3;C;%\r\n")

    def test_dico(self):
        struct = genparser.parse_structure("structures/dico.json")
        self.assertEqual(struct.depth(), 1)

        # Parse
        l = struct.parse_file("data/dico.txt")
        self.assertListEqual(l, ['AB', 'ABACA'])

        # JSON output
        out = io.StringIO()
        genparser.json_export(struct, l, out, None)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, '[{"word": "AB"}, {"word": "ABACA"}]')

        # CSV output
        out = io.StringIO()
        genparser.csv_export(struct, l, out)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, "AB\r\nABACA\r\n")

    def test_dico2(self):
        struct = genparser.parse_structure("structures/dico2.json")
        self.assertEqual(struct.depth(), 2)

        # Parse
        l = struct.parse_file("data/dico.txt")
        self.assertListEqual(l, [['AB', 'n.',
          'The fifth month of the Jewish year according to the ecclesiastical reckoning, the eleventh by the civil computation, coinciding nearly with August. W. Smith.'],
         ['ABACA', 'n.', 'The Manila-hemp plant (Musa textilis); also, its fiber. See Manila hemp under Manila.']])

    def test_paths(self):
        struct = genparser.parse_structure("structures/paths.json")
        self.assertEqual(struct.depth(), 2)

        # Parse
        l = struct.parse_file("data/paths.txt")
        self.assertListEqual(l, [['path/folder1', 'bidule', 'a', 'txt'], ['blabla/folder1', 'machin', 'c', 'csv'], ['bla/folder2', 'bordel', 'f', 'json']])

        # JSON output
        out = io.StringIO()
        genparser.json_export(struct, l, out, None)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, '[{"folder": "path/folder1", "name": "bidule", "letter": "a", "extension": "txt"}, {"folder": "blabla/folder1", "name": "machin", "letter": "c", "extension": "csv"}, {"folder": "bla/folder2", "name": "bordel", "letter": "f", "extension": "json"}]')

        # CSV output
        out = io.StringIO()
        genparser.csv_export(struct, l, out)
        s = out.getvalue()
        out.close()
        self.assertEqual(s, "folder;name;letter;extension\r\npath/folder1;bidule;a;txt\r\nblabla/folder1;machin;c;csv\r\nbla/folder2;bordel;f;json\r\n")
