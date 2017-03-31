import ply.lex as lex
import sys
# List of keywords. Each keyword will be return as a token of a specific
# type, which makes it easier to match it in grammatical rules.
keywords = {'array': 'ARRAY',
            'break': 'BREAK',
            'do': 'DO',
            'else': 'ELSE',
            'end': 'END',
            'for': 'FOR',
            'function': 'FUNCTION',
            'if': 'IF',
            'in': 'IN',
            'let': 'LET',
            'nil': 'NIL',
            'of': 'OF',
            'then': 'THEN',
            'to': 'TO',
            'type': 'TYPE',
            'var': 'VAR',
            'while': 'WHILE'}

# List of tokens that can be recognized and are handled by the current
# grammar rules.
tokens = ('END', 'IN', 'LET', 'VAR',
          'PLUS', 'TIMES','OR','AND','MINUS','DIVIDE',
          'HIGHER','LOWER','HIGHER_OR_EQUAL','LOWER_OR_EQUAL','EQUAL','DIFFERENT',
          'COMMA', 'SEMICOLON',
          'LPAREN', 'RPAREN',
          'NUMBER', 'ID',
          'COLON', 'ASSIGN',
	      'IF','THEN','ELSE',
	      'FUNCTION')

t_PLUS = r'\+'
t_TIMES = r'\*'
t_OR = r'\|'
t_AND = r'&'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_ASSIGN = r':='
t_COMMA = r','
t_SEMICOLON = r';'
t_HIGHER = r'>'
t_LOWER = r'<'
t_HIGHER_OR_EQUAL = r'>='
t_LOWER_OR_EQUAL = r'<='
t_EQUAL = r'='
t_DIFFERENT = r'<>'

t_ignore = ' \t'
#t_ignore = r'//.*\n'

# Declare the state
states = (
  ('oneccomment','exclusive'),
  ('ccomment','exclusive'),
)

def t_begin_oneccomment(t):
    r'\/\/'
    t.lexer.push_state('oneccomment')

def t_oneccomment_end(t):
    r'\n'
    t.lexer.pop_state()

t_oneccomment_ignore = " \t"

def t_oneccomment_error(t):
    t.lexer.skip(1)

# Match the first /*. Enter ccode state.
def t_begin_ccomment(t):
    r'\/\*'
    t.lexer.level = 1
    # Starts 'ccomment' state
    t.lexer.push_state('ccomment')

def t_ccomment_inbricated(t):
    r'\/\*'
    t.lexer.level += 1
    t.lexer.push_state('ccomment')

def t_ccomment_end(t):
    r'\*\/'
    t.lexer.level -= 1
    t.lexer.pop_state()                     # Back to the previous state

# For bad characters, we just skip over it
def t_ccomment_error(t):
    t.lexer.skip(1)

t_ccomment_ignore = " \t\n"

# Count lines when newlines are encounteredCan
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Distinguish between identifier and keyword. If the keyword is not also
# in the tokens list, this is a syntax error pure and simple since we do
# not know what to do about it.
def t_ID(t):
    r'[A-Za-z][A-Za-z\d_]*'
    if t.value in keywords:
        t.type = keywords.get(t.value)
        if t.type not in tokens:
            raise lex.LexError("unhandled keyword %s" % t.value, t.type)
    return t

# Recognize number - no leading 0 are allowed
def t_NUMBER(t):
    r'[1-9]\d*|0'
    t.value = int(t.value)
    return t

def t_error(t):
    raise lex.LexError("unknown token %s" % t.value, t.value)

def t_ANY_eof(t):
    try:
        if t.lexer.level != 0:
            sys.exit(1)
    except AttributeError:
        pass

lexer = lex.lex()
