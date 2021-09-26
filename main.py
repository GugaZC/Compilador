from lexer import tokens
from lexer import lexer
from ply import yacc

table = {'VARIABLE': {}}
stash = {}
context = 0


def p_main(p):
    '''main    :  VOID MAIN LPAREN RPAREN block'''
    p[0] = ("MAIN", p[5])


def p_while(p):
    '''while    :  WHILE expr_condition EOL
                |  WHILE expr_condition block'''
    if p[3] != ";":  # block
        p[0] = ("WHILE", p[2], p[3])
    else:  # EOL
        p[0] = ("WHILE", p[2])


def p_if(p):
    '''if   : IF expr_condition block
            | IF expr_condition blockif else'''
    if len(p) == 5:  # else
        p[0] = ("IF", p[2], p[3], p[4])
    else:
        p[0] = ("IF", p[2], p[3])


def p_else(p):
    '''else :  ELSE block'''
    p[0] = ("ELSE", p[2])


def p_for(p):
    '''for  :  FOR LPAREN ID EQUALS expr_binary SEMICOLON expr_binary SEMICOLON increment_for RPAREN block
            |  FOR LPAREN type ID EQUALS expr_binary SEMICOLON expr_binary SEMICOLON increment_for RPAREN block'''
    if len(p) == 13:  # com type
        p[0] = ("FOR", p[4], p[8], p[12])
    else:  # sem type
        p[0] = ("FOR", p[3], p[7], p[11])


def p_for_increment(p):
    '''increment_for    :   ID PLUS PLUS
                        |   ID EQUALS expr_binary
                        |   ID MINUS MINUS'''
    p[0] = p[1]


def p_bif(p):
    '''blockif  : LBRACES assign RBRACES
                | LBRACES while RBRACES
                | LBRACES if RBRACES'''
    p[0] = ('BLOCK', p[2])
    global context
    context += 1


def p_block(p):
    '''block : LBRACES assign EOB
             | LBRACES while EOB
             | LBRACES if EOB
             | LBRACES for EOB'''
    if str(p[3]) == '}':
        p[0] = ('BLOCK', p[2])
    else:
        p[0] = ('BLOCK', p[2], p[3])
    global context
    context += 1


def p_end_of_block(p):
    '''EOB  : RBRACES assign
            | RBRACES while
            | RBRACES if
            | RBRACES for
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
            | SEMICOLON if
            | SEMICOLON'''
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])


def p_assign(p):
    '''assign   : ID EQUALS expr_binary EOL
                | type assign'''
    if len(p) >= 5:
        if p[3] in table['VARIABLE'].keys():
            if table['VARIABLE'][p[3]]['context'] < context:
                raise AssertionError("Problema no contexto")
        p[0] = p[1]

    elif len(p) == 3:
        p[0] = ("TYPE_" + str(p[1]).upper(), p[2])
        if not p[2] in table["VARIABLE"]:
            if p[2] in stash:
                if stash[p[2]]["context"] <= context:
                    del stash[p[2]]
                else:
                    raise AssertionError("Variable " + p[2] + " not in right context")
            table["VARIABLE"][p[2]] = {'type': "TYPE_" + str(p[1]).upper(), 'value': "", 'context': context}
        else:
            raise AssertionError("Variable already exists")


def p_exrp_condition(p):
    '''expr_condition   : LPAREN expr_binary RPAREN'''
    p[0] = ("EXPR_CONDITION", p[2])


def p_expr_binary(p):
    '''expr_binary : term
            | expr_binary PLUS expr_binary
            | expr_binary MINUS expr_binary
            | expr_binary GT expr_binary
            | expr_binary LT expr_binary'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (str(p[2]), p[1], p[3])


def p_term(p):
    '''term : factor
            | variable'''
    p[0] = p[1]


def p_variable(p):
    '''variable : ID'''
    if not p[1] in table['VARIABLE']:
        stash[p[1]] = {'context': context}

        # raise AssertionError("Variable " + p[1] + " does not exists " + str(table))
    else:
        if table['VARIABLE'][p[1]]['context'] < context:
            raise AssertionError("Deu ruim no context")
        # p[0] = table['VARIABLE'][p[1]]
    p[0] = p[1]


def p_factor_int(p):
    '''factor : INTEGER'''
    p[0] = ('TYPE_INT', p[1])


def p_factor_float(p):
    '''factor : FLOAT'''
    p[0] = ('TYPE_FLOAT', p[1])


file = open("main.c", "r")
data = file.read()
lexer.input(data)

yacc.yacc()
y = yacc.parse(data)
print(y)
print(str(table))
print(stash)
