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

def p_seq_expr(p):
    '''expression : LPAREN exps RPAREN
                  | LPAREN RPAREN'''
    p[0] = SeqExp(p[2]) if len(p) == 4 else SeqExp([])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = IntegerLiteral(p[1])

def p_expression_identifier(p):
    '''expression : ID
                  | ID LPAREN args RPAREN'''
    p[0] = Identifier(p[1]) if len(p) == 2 else FunCall(Identifier(p[1]),p[3])

def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = BinaryOperator(p[1],IntegerLiteral(0),p[2])

def p_decl_var(p):
    '''decl_var : VAR ID ASSIGN expression
    		    | VAR ID COLON ID ASSIGN expression '''
    p[0] = VarDecl(p[2],None,p[4]) if len(p) == 5 else VarDecl(p[2],Type(p[4]),p[6])

def p_decl_fun(p):
    '''decl_fun : FUNCTION ID LPAREN args RPAREN EQUAL expression
                | FUNCTION ID LPAREN args RPAREN COLON ID EQUAL expression'''
    p[0] = FunDecl(p[2],p[4],Type(p[7]),p[9]) if len(p) == 10 else FunDecl(p[2],p[4],None,p[7])

def p_args(p):
    '''args :
            | argssome'''
    p[0] = p[1] if len(p) == 2 else []

def p_argssome(p):
    '''argssome : real_arg
                | argssome COMMA real_arg'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_real_arg(p):
    '''real_arg : ID COLON ID'''
    p[0] = VarDecl(p[1],Type(p[3]),None)

def p_arg_call(p):
    'real_arg : expression'
    p[0] = p[1]

def p_decls(p):
    '''decls : decl
             | decls decl'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_decl(p):
    '''decl : decl_var
            | decl_fun'''
    p[0] = p[1]

def p_exps(p):
    '''exps : expression
            | exps SEMICOLON expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_let(p):
    '''expression : LET decls IN exps END
                  | LET decls IN END'''
    p[0] = Let(p[2],p[4]) if len(p) == 6 else Let(p[2],[])

def p_assign(p):
    '''expression : ID ASSIGN expression'''
    p[0] = Assignment(Identifier(p[1]),p[3])

def p_error(p):
    import sys
    sys.stderr.write("no way to analyze %s\n" % p)
    sys.exit(1)

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer = tokenizer.lexer.clone())
