# ATIVIDADE PRÁTICA - reconhecedor de estruturas em C

from ply import *

class Lexer: 
    def __init__( self ):
        self.tokens = tokens
        self.lex = lex.lex()

    def tokenyze(self, data):
        self.lex.input( data )
        ret = []
        for token in self.lex:
            ret.append( token )
        return ret

t_ignore = ' \t'

# Palavras reservadas <palavra>:<TOKEN>
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'int' : 'VAR_INT',
    'float' : 'VAR_FLOAT',
    'double' : 'VAR_DOUBLE',
    'char' : 'VAR_CHAR',
    'for' : 'FOR_LOOP',
    'while' : 'WHILE_LOOP',
    'main' : 'MAIN_BLOCK',
    'return' : 'RETURN'
}

tokens = [
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING',
    'ID', 'NEWLINE', 'SEMICOLON', 'RBRACES', 'LBRACES', 'SAPOSTROPHE'
] + list(reserved.values())

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RBRACES = r'\}'
t_LBRACES = r'\{'
t_SAPOSTROPHE = r'\''
t_SEMICOLON = r'\;'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='
t_COMMA = r'\,'
t_SEMI = r';'
# t_INTEGER = r'\d+'
# t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'

def t_INTEGER(t):
    r'\b(?<!\.)\d+(?!\.)\b'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'([0-9]+([.][0-9]*)?|[.][0-9]+)'
    t.value = float(t.value)
    return t

def t_REM(t):
    r'REM .*'
    return t

# Definição de Identificador com expressão regular r'<expressão>'
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


if __name__ == "__main__":
    # Constroi o analisador léxico
    lexer = lex.lex()

    # string de teste
    data = '''
    main() 
    for() { } 
    while(0) { }
    int a = 1+1;
    float b = 2.0 ;
    char c = 'd'
    if(x<y){
        x = y;
    } else {
        if(x>y){
            y = x;
        }else{
            x = 0;
            y = 0;
        }
    }
    '''

    # string de teste como entrada do analisador léxico
    lexer.input(data)

    # Tokenização
    for tok in lexer:
        print(tok)
