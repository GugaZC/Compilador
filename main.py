from lexer import tokens
from lexer import lexer
from ply import yacc


def p_while(p):
    '''while    :  WHILE expr_condition EOL
                |  WHILE expr_condition block'''
    if p[3] != ";":
        p[0] = ("WHILE", p[2], p[3])
    else:
        p[0] = ("WHILE", p[2])

# TODOS fazer bloco principal, condicionais (IF ELSE)



def p_block(p):
    '''block : LBRACES assign EOB
             | LBRACES while EOB'''
    if str(p[3]) == '}':
        p[0] = ('BLOCK', p[2])
    else:
        p[0] = ('BLOCK', p[2], p[3])


def p_end_of_block(p):
    '''EOB  : RBRACES assign
            | RBRACES while
            | RBRACES'''
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_type(p):
    '''type : TYPE_INT
            | TYPE_FLOAT
            | TYPE_CHAR
            | TYPE_DOUBLE'''
    p[0] = p[1]


def p_end_of_line(p):
    '''EOL  : SEMICOLON assign
            | SEMICOLON while
            | SEMICOLON'''
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])


def p_assign(p):
    '''assign   : ID EQUALS expr_binary EOL
                | type assign'''
    if len(p) >= 5:
        p[0] = ("ASSIGN", p[1], p[3], p[4])
    elif len(p) == 3:
        p[0] = ("TYPE_" + str(p[1]).upper(), p[2])
        # TODO adicionar variável na tabela de símbolos


def p_exrp_condition(p):
    '''expr_condition   : LPAREN expr_binary RPAREN'''
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


def p_term(p):
    '''term : factor
            | variable'''
    p[0] = ('TERM', p[1])


def p_variable(p):
    '''variable : ID'''
    p[0] = ('VAR', p[1])


def p_factor(p):
    '''factor : INTEGER'''
    p[0] = ('INTEGER', p[1])


data = "while(1){int x = 2;int y = 2;} int y = 2;"
lexer.input(data)

for item in lexer:
    print(item)

yacc.yacc()
y = yacc.parse(data)
print(y)
