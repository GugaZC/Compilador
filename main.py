from lexer import tokens
from lexer import lexer
from ply import yacc

table = {'VARIABLE': {}}
stash = {}
verify = {}
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
        '''
        Se a direita for um terminal tenta verificar o tipo da variavel a esquerda
        '''
        if "TYPE_" in p[3]:
            right_var = {"name": "TERMINAL", "type": p[3]}

            if p[1] in table['VARIABLE']:
                '''
                se for diferente do terminal sobe erro
                '''
                if table['VARIABLE'][p[1]]['type'] != p[3]:
                    raise AssertionError(
                        "Variable {} is {} and should be {}".
                            format(p[1], table['VARIABLE'][p[1]]['type'], p[3]))
            else:
                '''
                se a variável a esquerda não foi declarada adiciona o tipo do terminal
                pra ser checado na declaração da variável a esquerda
                '''
                if not p[1] in verify:
                    verify[p[1]] = []
                verify[p[1]].append({"name": "TERMINAL", "type": p[3]})
            p[0] = {"left_var": p[1], "right_var": right_var }
            return
        else:
            right_var = {"name": p[3], "type": "undefined"}
        if p[3] in table['VARIABLE']:
            '''
            se a variável da direita exisitr na tabela de variáveis
            valida o contexto
            '''
            if table['VARIABLE'][p[3]]['context'] < context:
                raise AssertionError(
                "On p_assign: Variable {} have context {}, but its context {}"
                        .format(p[1], table['VARIABLE'][p[1]]['context'], str(context)))
            '''
            se ambos existerem na tabela de variáveis, valida os tipos na tabela
            '''
            if p[1] in table["VARIABLE"]:
                if table["VARIABLE"][p[3]]["type"] != table["VARIABLE"][p[1]]["type"]:
                    raise AssertionError(
                    "On p_assign: Variable {} have context {}, but its context {}"
                        .format(p[2], stash[p[2]]['context'], str(context)))

            right_var["type"] = table["VARIABLE"][p[3]]["type"]
        elif not p[1] in table["VARIABLE"]:
            '''
            se a variável da esquerda não tiver na tabela ela pode ainda
            ter sido declarada em um contexto maior, adiciona a variaǘel a direita
            pra comparar p tipo quando declarar a variável a esquerda
            '''
            if not p[1] in verify:
                verify[p[1]] = []
            verify[p[1]].append({"name": p[3], "type":
               table["VARIABLE"][p[3]]["type"] if p[3] in table["VARIABLE"] else "undefined" })
        p[0] = {"left_var": p[1], "right_var": right_var }

    elif len(p) == 3:
        # p[0] = ("TYPE_" + str(p[1]).upper(), p[2])
        '''
        caso a variável sendo declarada tenha sido usada "pra frente"
        por uma variável de dclarada antes desta, atualiza na lista de 
        verificações o tipo dela
        '''            
        for key, val in verify.items():
            if key == p[2]["left_var"]:
                continue
            for i in range(len(val)):
                if val[i]["name"] == p[2]["left_var"]:
                    val[i]["type"] = "TYPE_" + str(p[1]).upper()
        '''
        verifica se a variável sendo declarada foi utiliazada com tipagem errada
        "pra frente"
        '''
        for key, val in verify.items():
            if key == p[2]["left_var"]:
                for i in range(len(val)):
                    if val[i]["type"] != "TYPE_" + str(p[1]).upper():
                        raise AssertionError(
                        "Variable {} is {} and should be {}".
                            format(key, val[i]["type"], "TYPE_" + str(p[1]).upper(), p[2]))
                                    
        '''
        se o ID não existe na tabela de variáveis
        verifica na stash se é utilizado adiante no código
        '''
        if not p[2]["left_var"] in table["VARIABLE"].keys():
            if p[2]["left_var"] in stash:
                ''' 
                se tiver na stash pode deletar, a partir daqui 
                será encontrado a partir da tabela de variáveis
                '''
                if stash[p[2]["left_var"]]["context"] <= context:
                    del stash[p[2]["left_var"]]
                else:
                    raise AssertionError(
                    "On p_assign definition: Stash variable {} have context {}, but its context {}"
                        .format(p[2], stash[p[2]]['context'], str(context)))
        else:
            raise AssertionError("Variable already exists")
        table["VARIABLE"][p[2]["left_var"]] = {'type': "TYPE_" + str(p[1]).upper(), 'value': "", 'context': context}



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
    '''
    se não tiver na tabela adiciona na stash
    pra verificar a definição "depois"
    '''
    if not p[1] in table['VARIABLE']:
        stash[p[1]] = {'context': context}
        # raise AssertionError("Variable " + p[1] + " does not exists " + str(table))
    else:
        if table['VARIABLE'][p[1]]['context'] < context:
            raise AssertionError(
                "On p_variable: Variable {} have context {}, but its context {}"
                        .format(p[1], table['VARIABLE'][p[1]]['context'], str(context)))
        # p[0] = table['VARIABLE'][p[1]]
    p[0] = p[1]


def p_factor_int(p):
    '''factor : INTEGER'''
    p[0] = 'TYPE_INT'


def p_factor_float(p):
    '''factor : FLOAT'''
    p[0] = 'TYPE_FLOAT'


file = open("main.c", "r")
data = file.read()
lexer.input(data)

yacc.yacc()
y = yacc.parse(data)
# print(y)
print(str(table))
if len(stash) > 0:
    for entry in stash:
        print("entry in stash: {}".format(str(entry)))
    raise AssertionError("Stash not empty, variable used and not declared")
# print(stash)
