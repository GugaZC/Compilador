# ATIVIDADE PRÁTICA - reconhecedor de estruturas em C

from ply import *

# Palavras reservadas <palavra>:<TOKEN>
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'int': 'TYPE_INT',
    'float': 'TYPE_FLOAT',
    'double': 'TYPE_DOUBLE',
    'char': 'TYPE_CHAR',
    'for': 'FOR',
    'while': 'WHILE',
    'main': 'MAIN',
    'return': 'RETURN',
    'void': 'VOID'
}

# Demais TOKENS
tokens = [
             'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
             'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
             'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING',
             'ID', 'NEWLINE', 'SEMICOLON', 'RBRACES', 'LBRACES', 'SQUOTES', 'DQUOTES'
         ] + list(reserved.values())

t_ignore = ' \t\n'


def t_REM(t):
    r'REM .*'
    return t


# Definição de Identificador com expressão regular r'<expressão>'
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


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
t_SQUOTES = r'\''
t_DQUOTES = r'\"'


def t_INTEGER(t):
    r'\b(?<!\.)\d+(?!\.)\b'
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r'([0-9]+([.][0-9]*)?|[.][0-9]+)'
    t.value = float(t.value)
    return t


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


# Constroi o analisador léxico
lexer = lex.lex()

if __name__ == "__main__":
    # string de teste
    data = '''
    int main()
    {
        int x = 0;
        int i; 
        float y = 2.0;
        char j = 'a';
        double z = 10;
        for(i = 0; i<10; i++){
            x++;
        }
        while(x>=0){
            x--;
        }
        if(y>0){
            j = 'b';
        }
        else{
            x++;
        }
        return 0;
    }
    '''

    # string de teste como entrada do analisador léxico
    lexer.input(data)

    # Tokenização
    for tok in lexer:
        print(tok)
