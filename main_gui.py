from lexer_gui import Lexer
from lexer_gui import tokens
from ply import yacc
from os import remove


def p_exrp_condition(p):
    '''exrp_condition   : LPAREN expr_binary RPAREN'''
    p[0] = ("EXPR_CONDITION", p[2])


def p_expr_binary(p):
    '''expr_binary : term
            | expr_binary PLUS expr_binary
            | expr_binary MINUS expr_binary
            | expr_binary GT expr_binary'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (str(p[2]), p[1], p[3])


def p_term_factor(p):
    '''term : factor'''
    p[0] = ('NUM', p[1])


def p_factor(p):
    '''factor : INTEGER'''
    p[0] = p[1]


data = "(5>(1+2))"
lexer = Lexer()
_tokens = lexer.tokenyze(data)
for item in _tokens:
    print(item)

yacc.yacc()
y = yacc.parse(data)
print(y)
