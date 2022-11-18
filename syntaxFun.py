from Id import Ids
import Program_class as PC
def ATT_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão ID <- expr, que representa uma atribuição.
    Trata-se de uma parte de uma expressão com recusão a direita.
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, ID <- expr gera
                    (ID)   1 raiz
                      |
                     expr   1
    """
    # cria raiz

    # consome token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram):  return data #return data

    # cria filho 1
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda

    return data

def IF_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão IF. Ao longo da estrutura IF há expressões.

    IF expr THEN expr ELSE expr FI

    PARÂMETROS
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Lembrando que é possível que alguma expressão
    com recursão a esquerda seja chamada em algum 
    momento (expr + expr, por exemplo) que será tratada
    pela função expr_line
    Na estrutura da árvore semântica, uma expressão IF gera
                        (IF)           1 raiz
                    /    |     \\
                expr1  expr2  expr3    3 filhos
    """
    # consome token lido
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # cria raiz do tipo IF

    # cria filho 1
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda

    # Verifica Then
    checkToken_N_reportSyntError(f"line {data[0].token.line}: 'then' was expected after the 1° 'if' condition",
    Ids.THEN_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # cria filho 2
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda

    # Verifica ELSE
    checkToken_N_reportSyntError(f"line {data[0].token.line}: 'else' was expected in 'if' structure",
    Ids.ELSE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # cria filho 3
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda

    # Verifica Fi
    checkToken_N_reportSyntError(f"line {data[0].token.line}: 'fi' was expected to close 'if' structure",
    Ids.FI_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    return data

def WHILE_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão WHILE
    Ao longo da estrutura WHILE há expressões

    WHILE expr LOOP expr POOL

    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Lembrando que é possível que alguma expressão
        com recursão a esquerda seja chamada em algum 
        momento (expr + expr, por exemplo) que será tratada
        pela função expr_line
        
        - Na estrutura da árvore semântica, uma expressão IF gera
                    (WHILE)     1 raiz
                    /    \\
                expr1  expr2    2 filhos
    
    """
    # consome token lido
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # cria raiz do tipo WHILE

    # cria filho 1
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    # Verificar Loop
    checkToken_N_reportSyntError(f"line {data[0].token.line}: 'loop' expected after 'while' structure condition",
    Ids.LOOP_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # cria filho 2
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda

    # Verificar Pool
    checkToken_N_reportSyntError(f"line {data[0].token.line}: 'pool' was expected to close 'while' structure",
    Ids.POOL_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    return data


def LET_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão LET

    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão LET gera
                    (LET)     1 raiz
                      |
                  ID&TYPE1*   1 ou mais filhos
                      |
                     expr     1 filho
    Observe que as informações de ID, TYPE devem ser guardados porque serão úteis na análise semântica
    """
    
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    while True:
        # criar filho n

        # Verifica ID (info do nó)
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ID expected on 'let' structure",
        Ids.ID_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # verifica  :
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ':' expected on 'let' structure",
        Ids.COLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        # verificar TYPE (info do nó)
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE expected on 'let' structure",
        Ids.TYPE_ID, data)

        if(data[0].token.idEqual(Ids.ATT_ID)):
            data[0].nexToken(data[0].situation)
            if(data[0].situation == PC.SIG.EndOfProgram): return
        
            data = expr(data) # chama expressão

            data = expr_line(data) # recursão à esquerda

        if(not data[0].token.idEqual(Ids.COMMA_ID)): # verificar se terá outro ID:TYPE
            break
        
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return

    # ao sair do loop, a raís terá um total de k-1 filhos
    # cria kanézimo filho (IN)

    # Verifica in
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'in' was expected to close 'let' structure",
    Ids.IN_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda

    return data
    
def CASE_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão CASE
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão CASE gera
                (CASE)        1 raiz
                /    \\
            expr1  ID&TYPE    2 filhos
                        |       1 filho
                        expr
    Observe que as informações de ID, TYPE devem ser guardados porque serão úteis na análise semântica
    """

    # Consome token lido
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # cria filho 1
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    # Verifica Of
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'of' expected on case statement",
    Ids.OF_ID, data) 
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    data[0].setPs_err(f"line {data[0].token.line}:" + "'ID' missing in 'case' structure") # guarda erro para se ocorrer exceção vai ser esse erro
    if(not data[0].token.idEqual(Ids.ID_ID)): 
        data[0].addError()

    # Considerando que o filho 1 já exista
    while(data[0].token.idEqual(Ids.ID_ID)):
        # cria filho n + 1

        data[0].nexToken(data[0].situation) # consome ID (filho)

        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # verifica o :
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "':' missing in  'case' structure", Ids.COLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # verifica TYPE (filho)
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "TYPE missing in  'case' structure", Ids.TYPE_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # verifica =>
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "'=>' missing in  'case' structure", Ids.F_ATT_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # cria filho n+2
        
        data = expr(data) # chama expressão

        data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

        # ;
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "';' missing in  'case' structure", Ids.SEMICOLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # Verifica esac
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:  'esac' was expected to close CASE structure",
    Ids.ESAC_ID, data) 
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    return data

def NEW_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão NEW.

    NEW type

    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão CASE gera
                    (NEW)   1 raiz
                      |
                    TYPE    1 filho
    """
    # cria raiz
        
    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # cria filho
        
    # checar TYPE (filho)
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE was expected after new",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    return data

def ISVOID_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão ISVOID. Trata-se de uma expressão com recusão a direita.

    ISVOID --> expr

    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão ISVOID gera
                  (ISVOID)   1 raiz
                      |
                     expr    1 filho
    """
    # cria raiz
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # cria filho 1
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    return data
def NOT_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão NOT. Trata-se de uma expressão com recusão a direita.

    NOT --> expr
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão NOT gera
                    (NOT)   1 raiz
                      |
                     expr   1 filho
    """
    # cria raiz
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # cria filho 1
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    return data

def TIDE_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão TIDE. Trata-se de uma expressão com recusão a direita.

    TIDE --> expr
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão TIDE gera
                    (TIDE)   1 raiz
                      |
                     expr   1 filho
    """
    # cria raiz
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # cria filho 1
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    return data

def O_PARENTHESIS_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão (expr).
    Trata-se de uma expressão com recusão a direita

    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão (expr) gera
                    ('(')   1 raiz
                      |
                     expr   1 filho
    """
     # cria raiz
        
    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
     # cria filho 1
    while True:    
        data = expr(data) # chama expressão

        data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

        if(not data[0].token.idEqual(Ids.COMMA_ID)):
            break
                
        data[0].nexToken(PC.SIG.TokenFound)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ')' was expected to close '(expr)' structure",
    Ids.C_PARENTHESIS, data)# Verifica )
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    return data

def O_BRACKETS_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão {[[expr;]]^+}.
    Trata-se de uma expressão com recusão a direita
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão {[[expr;]]^+} gera
                    ('{')   1 raiz
                      |
                     expr   1 ou mais filhos
    """
    # cria raiz
        
    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # mais de uma expressão
    # então não precisa conferir nesse ponto se na primeira chamada é uma {
    # Já se espera que seja uma expressão a seguir
    while True:
        # cria Nnésimo filho 
        data = expr(data) # chama expressão

        data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ';' expected in multiple expression statement", Ids.SEMICOLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        # Se encontroou } então significa que não terá mais chamada de expr
        if(data[0].token.idEqual(Ids.C_BRACKETS)): 
            break

    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:"+ '}' + "expected to close multiple expression statement", Ids.C_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    return data


def ID_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressões que começam com ID. Trata-se de uma expressão com recusão a direita.
    ID --> expr 
    ID --> epslon, isto é, somente o ID

    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, uma expressão inicializada com ID gerará 
    um nó somente na outra função na qual foi chamada. Caso contrário geraria 
    redundância de nó
                    (IF)           1 raiz
                /    |     \\
            expr1  expr2  expr3    3 filhos
    
    """
    # adicionar raiz
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data # return data
    
    # <-
    if(data[0].token.idEqual(Ids.ATT_ID)): # Verifica Atribuição
        data = ATT_func(data)
    # ()
    elif(data[0].token.idEqual(Ids.O_PARENTHESIS)):
        data = O_PARENTHESIS_func(data)
    
    # sozinho "ID" --> não faz nada

    return data

def DOT_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão .ID
    Trata-se de uma parte de uma expressão com recusão a esquerda
    de chamada de método.
    
    PARÂMETROS
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, .ID gera
                    (DOT)   1 raiz
                      |
                      ID   1 ou mais filhos
    """

    # cria raiz
        
    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # cria filho (ID)
        
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    return data

def AT_func(data):
    """
    SOBRE
    -------------
    Função para tratar expressão @TYPE.ID
    Trata-se de uma parte de uma expressão com recusão a esquerda
    de chamada de método.

    PARÂMETROS
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, .ID gera
                    (AT)   1 raiz
                      |
                    TYPE*   1 ou mais filhos
                      |
                      ID*   1 ou mais filhos
        * une em um nó só? Não, pois ID terá outros filhos
    """
    # cria raiz
        
    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # cria filho 1

    # verificar TYPE
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE expected in expression expr[@TYPE]...",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # verificar .
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: '.' expected in expression expr[@TYPE]...",
    Ids.DOT_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    if(data[0].situation == PC.SIG.TokenFound):
        # retornar ao anterior para poder dar next 
        # na função ID_func(data) sem afetar o programa
        data[0].undo()  
        # retornar ao anterior para poder dar next 
        # na função DOT_func(data) sem afetar o programa
        
    data = DOT_func(data) # passar o trabalho para outra função que irá fazer a mesma coisa
    return data

def OPs_func(data):
    """
    SOBRE
    -------------
    
    Função para tratar expressão @TYPE.ID
    Trata-se de uma parte de uma expressão com recusão a esquerda
    de chamada de método.

    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    Na estrutura da árvore semântica, operadores lógicos e aritiméticos geram
                <exp>   (estrutura de recursão anterior)
                     \\
                     (OP)   1 raiz
                      |
                     expr   1 filho
    """
    # cria raiz
    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # cria Nnésimo filho 
    
    data = expr(data) # chama expressão

    data = expr_line(data) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    return  data

def expr_line(data):
    """
    SOBRE
    -------------
    Função que trata recursão à esquerda presente em algumas expressões da linguagem Cool.
    Um exemplo disso é a estrutura:
                  expr + expr

    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    """
    while True:
        # modificados para remover recursão a esquerda # +, -, *, /, <, <=, =
        if(data[0].token.idEqual(Ids.PLUS_ID) or data[0].token.idEqual(Ids.MINUS_ID) or data[0].token.idEqual(Ids.ASTERISK_ID) or data[0].token.idEqual(Ids.F_SLASH_ID) or data[0].token.idEqual(Ids.LESS_THAN_ID) or data[0].token.idEqual(Ids.LESS_THAN_EQUAL_TO_ID) or data[0].token.idEqual(Ids.EQUAL_TO_ID)):
            data = OPs_func(data)
        elif(data[0].token.idEqual(Ids.AT_ID)): # concerteza ao ter um @ terá de ter TYPE.ID depois
            data = AT_func(data)

        elif(data[0].token.idEqual(Ids.DOT_ID)): # concerteza ao ter um . terá de ter ID depois
            data = DOT_func(data)
        else: break

    data = expr(data)
    return data
    
        
def expr(data):
    """
    SOBRE
    -------------
    Função principal para tratar de expressões.
    Basicamente a estrutura é dividida em busca por expressões atômicas e não atômicas.
    
    - Expressões Atômicas: são simples, são símbolos terminais da gramática

    - Expressões Não Atômicas: são expressões que possuem símbolos não teminais(pensando na notação de gramática)
        - Tratadas dentro de suas respectivas funções 
        - Em cada uma, é possível que alguma expressão com recursão a esquerda seja chamada em algum 
    momento (expr + expr, por exemplo) que será tratada pela função expr_line

    PARÂMETROS
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
   
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    A formação da árvore semântica é tratada separadamente para cada tipo de expressão identificada em Cool.
    Isso quer dizer que, em cada função destinada a cada um dos grupos de expressões dispostos abaixo, com 
    exceção de expressões atômicas as quais serão tratadas diretamente na chamada de expr(), haverá a adição
    de nós segundo a regra sintática de cada expressão.

    Pensar ainda em como vai ocorrer a ligação dos símbolos terminais
        - depende do nó anterior de um outro contexto?
        - em qual nó irei ligar?
    """
    # Terminais
    if(data[0].token.idEqual(Ids.INTEGER_ID) or data[0].token.idEqual(Ids.STRING_ID) or data[0].token.idEqual(Ids.TRUE_ID) or data[0].token.idEqual(Ids.FALSE_ID)):
        data[0].nexToken(PC.SIG.TokenFound)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

    # Recursões a direita
    
    if(data[0].token.idEqual(Ids.ID_ID)):  data = ID_func(data) #ID
    
    if(data[0].token.idEqual(Ids.IF_ID)):  data = IF_func(data) #IF
    
    if(data[0].token.idEqual(Ids.WHILE_ID)): data = WHILE_func(data) #WHILE
    
    if(data[0].token.idEqual(Ids.LET_ID)): data = LET_func(data) #LET
    
    if(data[0].token.idEqual(Ids.CASE_ID)): data = CASE_func(data) #CASE
    
    if(data[0].token.idEqual(Ids.NEW_ID)): data = NEW_func(data) #NEW
    
    if(data[0].token.idEqual(Ids.ISVOID_ID)): data = ISVOID_func(data) #ISVOID
    
    if(data[0].token.idEqual(Ids.NOT_ID)): data = NOT_func(data) #NOT
        
    if(data[0].token.idEqual(Ids.TIDE_ID)): data = TIDE_func(data) #NOT
    
    if(data[0].token.idEqual(Ids.O_PARENTHESIS)): data = O_PARENTHESIS_func(data) #(
    
    if(data[0].token.idEqual(Ids.O_BRACKETS)): data = O_BRACKETS_func(data)  #{

    return data

def checkToken_N_reportSyntError(errSTR, ID_comp, data, isFormal = False):
    """
    SOBRE
    ----------------
    Função criada para comparar um dado token T com um elemento 
    E esperado para seguir a ordem sintática da gramática.
    Nessa verificação, mesmo que T não seja E, verifica-se se
    o próximo token após T é E. Se for, será considerado consumido
    como se o erro sintático não ocorreu. Porém a mensagem de erro
    ainda aparecerá ao usuário após a análise.

    PARÂMETROS
    ----------------
    errSTR : mensagem de erro referente a regra que a falta do E inflingiu
    ID_comp: Identificador do E esperado naquele momento
    
    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    """
    typeOrName = ""
    if (not data[0].token.idEqual(ID_comp)): # se o token procurado não for o atual
        data[0].setPs_err(errSTR)
        data[0].addError()
        if(data[0].afToken().idEqual(ID_comp)): # se o token procurado for o próximo
            data[0].nexToken(PC.SIG.TokenFound)                  # "fingir" que acertou de primeira
            typeOrName =data[0].token.token

        else:
            if(isFormal):
                data[0].nexToken(PC.SIG.TokenNotFound) # ir para o próximo token já que o atual foi analisado
            else:
                data[0].situation = PC.SIG.TokenNotFound
    else:
        typeOrName =data[0].token.token
        data[0].nexToken(PC.SIG.TokenFound) # ir para o próximo token já que o atual foi analisado
        
    return data, typeOrName
def ATTRIBUTE_func(data):
    """
    SOBRE
    ----------
    Função que trata da estrutura de um atributo .
    Verificar estrutura TYPE <- expr.
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica
    
    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    """
    # verificar TYPE
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: " + "No atribute Type declared",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # verificar se há atribuição de valor junto da declaração de um atributo
    if(data[0].token.idEqual(Ids.ATT_ID)):
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return
        data = expr(data)

    return data

def formal(data):
    """
    SOBRE
    --------
    Função que verifica estrutura de parâmetro de um método.
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica
    
    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    """
    _listOfFormals = []
    while True:
        # Verifica ID
        data, _nameOfFormal = checkToken_N_reportSyntError(f"line {data[0].token.line}: ID not founded. Formal expected",
        Ids.ID_ID, data, PC.SIG.IsFormal)
        if(data[0].situation == PC.SIG.EndOfProgram or data[0].situation == PC.SIG.TokenNotFound): 
            return data
        # verifica  :
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ':' expected in formal structure",
        Ids.COLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        # verifica  TYPE
        data, _typeOfFormal = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE expected",
        Ids.TYPE_ID, data) 
        if(data[0].situation == PC.SIG.EndOfProgram): return data


        if(not data[0].token.idEqual(Ids.COMMA_ID)):
            break
        data[0].nexToken(data[0].situation) # pula o { encontrado extra pois terá mais de uma expressão
        _listOfFormals.append((_nameOfFormal,_typeOfFormal))
        if(data[0].situation == PC.SIG.EndOfProgram): return data
    print(_listOfFormals)
    return data, _listOfFormals
    
def METHOD_func(data, _Methodname):
    """
    SOBRE
    --------
    Função que verifica estrutura de um método declarado em Cool
    
    PARÂMETROS
    -------------
    data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica
    
    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    """
    _typeOfReturn = ""
    _listOfFormals = []
    if(data[0].token.idEqual(Ids.C_PARENTHESIS)):
        data[0].nexToken(data[0].situation) # pula o { encontrado extra pois terá mais de uma expressão
        if(data[0].situation == PC.SIG.EndOfProgram): return data 
    else:
        # verifica formal obrigatório
        data, _listOfFormals  = formal(data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        # verifica )
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ')' expected in method declaration",
        Ids.C_PARENTHESIS, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # verifica :
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ':' expected",
    Ids.COLON_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # verifica TYPE
    data, _typeOfReturn = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE expected",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # verifica {
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: {'{'} expected",
    Ids.O_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # ANT:  verifica se tem { extra
    # RESP: não precisa, já tem uma expressão do tipo {expr;^+}

    data = expr(data)
    data = expr_line(data)

    # } fechar method
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: {'}'} expected to close methods",
    Ids.C_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    data[1].newMethod(_Methodname, _typeOfReturn)
    if _listOfFormals!=[]:
        # print(data[1].obj.methods[-1].name)

        for f in _listOfFormals:
            data[1].newFormal(f[0], f[1])

    return data

def FEATURE_func(data):
    _name =  ""
    # Verifica ID
    data, _name = checkToken_N_reportSyntError(f"line {data[0].token.line}: ID was expected to initialize a feature",
    Ids.ID_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    if(data[0].token.idEqual(Ids.O_PARENTHESIS)):
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        data =  METHOD_func(data,_name)
        return data
    else:
        # segunda chance só se o token analisado não for :
        if(not data[0].token.idEqual(Ids.COLON_ID) and data[0].afToken().idEqual(Ids.O_PARENTHESIS)):
            data[0].nexToken(PC.SIG.TokenFound)
            if(data[0].situation == PC.SIG.EndOfProgram): return data
            data = METHOD_func(data)
        else:
            if(data[0].token.idEqual(Ids.COLON_ID)): # verifica :
                data[0].nexToken(PC.SIG.TokenFound)
                if(data[0].situation == PC.SIG.EndOfProgram): return data
                data = ATTRIBUTE_func(data)
            elif(data[0].afToken().idEqual(Ids.COLON_ID)): # se o próximo for :
                data[0].nexToken(PC.SIG.TokenFound)
                if(data[0].situation == PC.SIG.EndOfProgram): return data
                data = ATTRIBUTE_func(data)
            else:
                data[0].nexToken(PC.SIG.TokenFound)
                if(data[0].situation == PC.SIG.EndOfProgram): return data

                data[0].setPs_err(f"line {data[0].token.line}: '('(method) or ':'(attribute) expected")
                data[0].addError()

        return data

def CLASS_func (data): 
    _className, _typeInherits = "" ,""
    # Verifica class
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "Must be a class declaration",
    Ids.CLASS_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # Verifica TYPE
    data, _className = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'class' must be followed by a TYPE",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # Verifica inherits (OPCIONAL) só uma chance aos opcionais
    if(data[0].token.idEqual(Ids.INHERITS_ID)):  
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        # Verifica TYPE
        data, _typeInherits = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'inharits' must be followed by a TYPE",
        Ids.TYPE_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    data[1].newType(_className, _typeInherits)

    # Verifica {
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + " '{'" + f" expected after class declaration",
    Ids.O_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    # CLASSE VAZIA
    # verifica }
    if(not data[0].token.idEqual(Ids.C_BRACKETS)):
        while True:
            data = FEATURE_func(data)
            # verifica ;
            data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + " ';'" + f" expected in the end of a feature on {data[0].token.token}",
            Ids.SEMICOLON_ID, data)
            if(data[0].situation == PC.SIG.EndOfProgram): return data
            
            if(not data[0].token.idEqual(Ids.ID_ID)):
                break
    endClassError = f"line {data[0].token.line}:" + " ';'" + f" expected to close class"
    # verifica }
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + " '}'" + f" expected o close class statement",
    Ids.C_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): 
        data[0].setPs_err(endClassError)
        data[0].addError()
        return data

    data[1].addType()
    
    # verifica ;
    data, _ = checkToken_N_reportSyntError(endClassError,
    Ids.SEMICOLON_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    data = CLASS_func(data)

    return data

def program(line):
    myProgram = PC.Program(line)

    data = [myProgram, 0, 0]

    data = CLASS_func(data)

    return data
