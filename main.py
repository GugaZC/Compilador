from lexer import tokens
from lexer import lexer
from ply import yacc

def p_while(p):
    '''while :  WHILE expr_condition'''
    p[0] = ("WHILE", p[2])

def p_exrp_condition(p):
    '''expr_condition   : LPAREN expr_binary RPAREN'''
    p[0] = ("EXPR_CONDITION", p[2])


def p_expr_binary(p):
    '''expr_binary : term
            | LPAREN expr_binary RPAREN
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


data = "while(5>(1+2))"
lexer.input(data)

for item in lexer:
    print(item)

yacc.yacc()
y = yacc.parse(data)
print(y)
