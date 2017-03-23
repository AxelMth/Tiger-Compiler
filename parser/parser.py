from ast.nodes import *
from . import tokenizer
import ply.yacc as yacc

tokens = tokenizer.tokens

precedence = (
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQUAL', 'DIFFERENT', 'LOWER_OR_EQUAL', 'LOWER', 'HIGHER_OR_EQUAL', 'HIGHER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right','UMINUS')
)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression TIMES expression
                  | expression OR expression
                  | expression AND expression
                  | expression MINUS expression
                  | expression DIVIDE expression
                  | expression HIGHER expression
                  | expression HIGHER_OR_EQUAL expression
                  | expression LOWER expression
                  | expression LOWER_OR_EQUAL expression
                  | expression EQUAL expression
                  | expression DIFFERENT expression'''
    p[0] = BinaryOperator(p[2], p[1], p[3])

def p_expression_ifthenelse(p):
    '''expression : IF expression THEN expression
                  | IF expression THEN expression ELSE expression'''
    p[0] = IfThenElse(p[2],p[4],p[6]) if len(p) == 7 else IfThenElse(p[2],p[4],None)

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = IntegerLiteral(p[1])

def p_expression_identifier(p):
    'expression : ID'
    p[0] = Identifier(p[1])

def p_expression_letExpression(p):
    '''expression : letExpression'''
    p[0] = p[1]

def p_error(p):
    import sys
    sys.stderr.write("no way to analyze %s\n" % p)
    sys.exit(1)

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer = tokenizer.lexer.clone())
