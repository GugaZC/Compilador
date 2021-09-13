from lexer import Lexer
from lexer import tokens
from ply import yacc

# def p_assign_int(p):
#     '''assign : VAR_INT ID EQUALS term'''
#     if not isinstance(p[4], int):
#         raise ValueError( "Expected int, got type {}".format( type(p[4] ) ) )
#     p[2] = p[4]


# def p_assign_float(p):
#     '''assign : VAR_FLOAT ID EQUALS term'''
#     if not isinstance(p[4], float):
#         raise ValueError( "Expected float, got type {}".format( type(p[4] ) ) )
#     p[2] = p[4]

# def p_term_mul(p):
#     '''term : term TIMES factor'''
#     p[0] = p[1] * p[3]

# def p_term_sum(p):
#     '''term : term PLUS factor
#             | assign PLUS factor '''
#     p[0] = p[1] + p[3]

# def p_term_sub(p):
#     '''term : term MINUS factor'''
#     p[0] = p[1] - p[3]

# def p_term_factor(p):
#     '''term : factor'''
#     p[0] = p[1]

# def p_factor(p):
#     '''factor : INTEGER
#               | FLOAT'''
#     p[0] = p[1]

def p_expr_plus(p):
    '''expr : term PLUS factor'''
    p[0] = ('+', p[1], p[3])


def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]


def p_factor(p):
    '''factor : INTEGER'''
    p[0] = ('NUM', p[1])

data = "1+2"
lexer = Lexer()
_tokens = lexer.tokenyze( data )
for item in _tokens:
    print( item )

yacc.yacc()
y = yacc.parse(data)
print(y)
