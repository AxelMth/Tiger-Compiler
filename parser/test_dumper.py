import unittest

from parser.dumper import Dumper
from parser.parser import parse

class TestDumper(unittest.TestCase):

    def parse_dump(self, text):
        tree = parse(text)
        return tree.accept(Dumper(semantics=False))

    def check(self, text, expected):
        self.assertEqual(self.parse_dump(text), expected)

    def test_literal(self):
        self.check("42", "42")

    def test_priority(self):
        self.check("1+2*3", "(1 + (2 * 3))")
        self.check("2*3+1", "((2 * 3) + 1)")
        self.check("2/3-5","((2 / 3) - 5)")
        self.check("5-2/3","(5 - (2 / 3))")
        self.check("10-2-1","((10 - 2) - 1)")

    def test_ifThenElse(self):
        self.check("if 1 then 2 else 2+1","if 1 then 2 else (2 + 1)")
        self.check("if 1-1 then 2 else 5+2","if (1 - 1) then 2 else (5 + 2)")

if __name__ == '__main__':
    unittest.main()
