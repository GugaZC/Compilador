# Compilador da linguagem c

Compilador desenvolvido utilizando a biblioteca ply que segue as fases de analise léxica, analise sintática e analise semântica.

## Instalação 
Para executar o projeto basta clonar o repositório e instalar a dependencia com o código abaixo:
```sh
pip3 install ply
```
Depois de terminar a instalação da biblioteca `ply` será necessário a execução do arquivo `main.py` para ver os tokens gerados e a tabela de símbolos. Esses tokens e a tabela são em relação ao código adicionado no arquivo `main.c`. 

## Descrições das etapas de desenvolvimento
Nessa seção será descrito brevemente como foi feito a implementação de cada etapa do compilador, sendo elas:
 - Análise léxica
 - Análise sintática
 - Análise semântica
### Análise léxica
A análise léxica, ou tokenização, de um compilador consiste na separação de cadeias de caracteres em tokens. Para isso o analisador léxico lê todas as linhas do código de entrada e separa em partes menores de acordo com expreções regulares defnidas. Nesse compilador, existem tokens de palavras reservadas que incluem as estruturas ```if, else, for, while```  e tipos de variáveis como ```int, float```, também existem tokens de símbolos como ```=, +, -, /, >```. Além dos items citados anteriormente, a análise léxica permite atribuir valores aos tokens a partir de funções como:
```python=
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')  
    return t
```
Nesta implementação foram ignorados símbolos de `tab`, `space` e fim de linha:
```python=
t_ignore = ' \t\n'
```

### Análise sintática
A análise sintática é uma fase do processo de compilação onde é feita uma verificação da estrutura gramatical segundo uma determinada gramática formal.
Para essa análise, fizemos a declaração de funções de acordo com a biblioteca `lexer`, essas funções são responsáveis pelo que o compilador irá ler e verificar se o que foi lido está dentro do esperado para a linguagem desenvolvida. Como exemplo, podemos verificar a função que faz a verificação de um while: 
```python=
def p_while(p):
    '''while    :  WHILE expr_condition EOL
                |  WHILE expr_condition block'''
    if p[3] != ";":  # block
        p[0] = ("WHILE", p[2], p[3])
    else:  # EOL
        p[0] = ("WHILE", p[2])
```
Nessa função, podemos ver que o que está comentado e em letra minúscula é um símbolo não terminal que é o nome de uma outra função no código, o que faz com que o compilador vá para essa próxima função que, no exemplo acima, tem o nome de  `expr_condition`. Já as palavras em letra maiúscula são os símbolos terminais, que foram declarados como palavras reservadas na parte da análise léxica, ou seja, quando o compilador faz a leitura dessa cadeira de caracteres ele não passa para uma próxima função e encerra a leitura para aquele símbolo terminal.


### Análise semântica
Regras além das definidas pela análise sintática são responsabilidade da análise semântica. Utilizando a biblioteca `ply` é possível criar regras logo após a validação da análise sintática. Um exemplo é apresentado na função ```p_variable()```. 

Para garantir que as variáveis não declaradas sejam utilizadas no código, é validádo se esta existe na tabela de variáveis do compilador. Caso exista, é validado o seu contexto (`if` linha 10).

`stash` :
```python=
def p_variable(p):
    '''variable : ID'''
    '''
    se não tiver na tabela adiciona na stash
    pra verificar a definição "depois"
    '''
    if not p[1] in table['VARIABLE']:
        stash[p[1]] = {'context': context}
    else:
        if table['VARIABLE'][p[1]]['context'] < context:
            raise AssertionError(
                "On p_variable: Variable {} have context {}, but its context {}"
                        .format(p[1], table['VARIABLE'][p[1]]['context'], str(context)))
        # p[0] = table['VARIABLE'][p[1]]
    p[0] = p[1]
```

Caso a variável ainda não exista na tabela de variáveis, ainda é possível que ela seja declarada em um momento posterior da análise semântica (visto que a análise é feita resolvendo os tokens a direita primeiro), por isso é adiciona a uma estrura `stash` para ser posteriormente validado o uso.
```python=
...
if not p[1] in table['VARIABLE']:
        stash[p[1]] = {'context': context}
...
```
Em toda declaração de variável é checado se a variável declarada está na `stash`, de maneira que, caso uma variável seja utilizada e não declarada a `stash` manterá uma variável "solta".
```python=
def p_assign(p):
    '''assign   : ID EQUALS expr_binary EOL
                | type assign'''
...
    if p[2]["left_var"] in stash:
        if stash[p[2]["left_var"]]["context"] <= context:
            del stash[p[2]["left_var"]]
        else:
            raise AssertionError(
            "On p_assign definition: Stash variable {} have context {}, but its context {}"
                .format(p[2], stash[p[2]]['context'], str(context)))
...
```
No final da compilação é verificado se existem variáveis utilizadas e não declaradas.
```python=
if len(stash) > 0:
    for entry in stash:
        print("entry in stash: {}".format(str(entry)))
    raise AssertionError("Stash not empty, variable used and not declared")
```
Outra regra semântica definida pelo compilador é a verificação de tipagem. Caso exista uma expressão do tipo `int a = 3`, será validada a tipagem, comparando o tipo do token `3`, com o tipo armazenado na tabela de variáveis referente a variável `a`.
```python=
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
```
Caso a variável ainda não existir na tabela de variáveis, o tipo da variável a direita é adicionado a uma estrutura de verificação (`verify`) que será utilizada na declaração da variável `a`.
```python=
'''
se a variável a esquerda não foi declarada adiciona o tipo do terminal
pra ser checado na declaração da variável a esquerda
'''
if not p[1] in verify:
    verify[p[1]] = []
verify[p[1]].append({"name": "TERMINAL", "type": p[3]})
```

Em toda declaração de variável é verificado se ela foi utilizada a frente no código. Caso tenha sido e com o tipo errado, o compilador dectada o erro e para a compilação.
```python=
...
for key, val in verify.items():
    if key == p[2]["left_var"]:
        for i in range(len(val)):
            if val[i]["type"] != "TYPE_" + str(p[1]).upper():
                raise AssertionError(
                "Variable {} is {} and should be {}".
                    format(key, val[i]["type"], "TYPE_" + str(p[1]).upper(), p[2]))
...
```