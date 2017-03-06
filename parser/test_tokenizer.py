import unittest

from ply.lex import LexError

from .tokenizer import lexer

class TestLexer(unittest.TestCase):

    def check(self, type, value):
        t = lexer.token()
        self.assertEqual(t.type, type)
        self.assertEqual(t.value, value)

    def check_end(self):
        t = lexer.token()
        self.assertIsNone(t)

    def test_basic(self):
        lexer.input("42")
        self.check('NUMBER', 42)
        self.check_end()

    def test_op(self):
        lexer.input("1 + 2 * 3")
        self.check('NUMBER', 1)
        self.check('PLUS', '+')
        self.check('NUMBER', 2)
        self.check('TIMES', '*')
        self.check('NUMBER', 3)
        lexer.input("|")
        self.check('OR','|')
        lexer.input("-")
        self.check('MINUS','-')
        lexer.input("&")
        self.check('AND','&')
        lexer.input("/")
        self.check('DIVIDE','/')
        lexer.input(">")
        self.check('HIGHER','>')
        lexer.input("<")
        self.check('LOWER','<')
        lexer.input("<=")
        self.check('LOWER_OR_EQUAL','<=')
        lexer.input(">=")
        self.check('HIGHER_OR_EQUAL','>=')
        lexer.input("=")
        self.check('EQUAL','=')
        lexer.input("<>")
        self.check('DIFFERENT','<>')
        self.check_end()

    def test_keyword(self):
        lexer.input("var")
        self.check('VAR', 'var')
        lexer.input("int")
        self.check('INT','int')
        lexer.input("let")
        self.check('LET','let')
        lexer.input("in")
        self.check('IN','in')
        lexer.input("end")
        self.check('END','end')
        self.check_end()

    def test_identifier(self):
        lexer.input("foobar")
        self.check('ID', 'foobar')
        self.check_end()

    def test_if_then_else(self):
        lexer.input("if")
        self.check('IF',"if")
        lexer.input("then")
        self.check('THEN',"then")
        lexer.input("else")
        self.check('ELSE',"else")

    def test_error(self):
        lexer.input("foobar@")
        self.check('ID', 'foobar')
        self.assertRaises(LexError, lexer.token)

    def test_unhandled_keyword(self):
        lexer.input("array")
        self.assertRaises(LexError, lexer.token)

if __name__ == '__main__':
    unittest.main()
