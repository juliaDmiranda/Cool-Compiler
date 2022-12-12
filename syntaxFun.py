from ast import Expression
import os
from Id import Ids
import Program_class as PC
import TYPE_LIST  as tl
import synTree as  st

def ATT_func(data, myTree):
    """
    SOBRE
    -------------
    Função para tratar expressão ID <- expr, que representa uma atribuição.
    Trata-se de uma parte de uma expressão com recursão a direita.
    
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
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.ASSIGNMENT) # não precisa setar de novo(fazer teste depois)
    tmp.setLine(data[0].token.line)
    tmp.setName(data[0].token.token)

    # consome token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram):  return data #return data

    # cria filho 1
        
    data, myTree = expr(data, myTree) # chama expressão

    data, myTree = expr_line(data, myTree) # recursão à esquerda

    # myTree.addChild(tmp)
    return data, myTree

def ID_func(data, myTree):
    """
    SOBRE
    -------------
    Função para tratar expressões que começam com ID. Trata-se de uma expressão com recusão a direita.
    ID --> expr 
    ID --> epsilon, isto é, somente o ID
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
                    (ID)           1 raiz
                /    |     \\
            expr1  expr2  expr3    3 filhos
    
    """
    # adicionar raiz
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.ID)
    tmp.setName(data[0].token.token)
    tmp.setLine(data[0].token.line)
    tmp.setType("-")
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): 
        myTree.addChild(tmp)
        return data, myTree # return data
    
    # <-
    if(data[0].token.idEqual(Ids.ATT_ID)): # Verifica Atribuição
        tmp.setLabel(st.tag.ASSIGNMENT)
        data, tmp = ATT_func(data, tmp)
    # ()
    elif(data[0].token.idEqual(Ids.O_PARENTHESIS)):
        tmp.setLabel(st.tag.FUNCALLID)
        data, tmp = O_PARENTHESIS_func(data, tmp)
   
    if(tmp.children == None):
        tmp.addChild()
    
    # sozinho "ID" --> não faz nada
    myTree.addChild(tmp)
    return data, myTree

def IF_func(data, myTree):
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
    # cria raiz do tipo IF
    tmp:st.Node = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.IF)
    tmp.setName(data[0].token.token)
    tmp.setType("Bool")
    tmp.setLine(data[0].token.line)

    # consome token lido
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree

    # cria filho 1
    data, tmp = expr(data, tmp) # chama expressão
    data, aux = expr_line(data, tmp.children[-1]) # recursão à esquerda
    tmp.children[-1] = aux

    # Verifica Then
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'then' was expected after the 1° 'if' condition",
    Ids.THEN_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree

    # cria filho 2
    data, tmp = expr(data, tmp) # chama expressão
    data, aux = expr_line(data, tmp.children[-1]) # recursão à esquerda -1 para fazer com que a próxima expressão não seja mais um filho do nó IF
    tmp.children[-1] = aux
    # Verifica ELSE
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'else' was expected in 'if' structure",
    Ids.ELSE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree

    # cria filho 3
    data, tmp = expr(data, tmp) # chama expressão
    data, aux = expr_line(data, tmp.children[-1]) # recursão à esquerda
    tmp.children[-1] = aux
    # Verifica Fi
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'fi' was expected to close 'if' structure",
    Ids.FI_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree

    myTree.addChild(tmp)
    return data, myTree

def WHILE_func(data, myTree):
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
    # cria raiz do tipo WHILE
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.WHILE)
    tmp.setName(data[0].token.token)
    tmp.setLine(data[0].token.line)
    tmp.setType("Bool")

    # consome token lido
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree
    
    # cria filho 1
    data, tmp = expr(data, tmp) # chama expressão
    data, aux = expr_line(data, tmp.children[-1])  # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!
    tmp.children[-1] = aux

    # Verificar Loop
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'loop' expected after 'while' structure condition",
    Ids.LOOP_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree

    # cria filho 2
        
    data, tmp = expr(data, tmp) # chama expressão
    data, aux = expr_line(data, tmp.children[-1])  # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!
    tmp.children[-1] = aux

    # Verificar Pool
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'pool' was expected to close 'while' structure",
    Ids.POOL_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree

    myTree.addChild(tmp)
    return data, myTree

# NÃO SEI O QUE FAZER COM O LETTTT
def LET_func(data, myTree):
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
    # Cria raíz
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.LET)
    tmp.setName(data[0].token.token)
    tmp.setLine(data[0].token.line)
    
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    while True:
        # criar filho n
        aux = st.Node()
        aux.children = []
        aux.setLabel(st.tag.LETOPT)
        aux.setName(data[0].token.token)
        aux.setLine(data[0].token.line)

        # Verifica ID (info do nó)
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ID expected on 'let' structure",
        Ids.ID_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # verifica  :
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ':' expected on 'let' structure",
        Ids.COLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        aux.setType(data[0].token.token)
        # verificar TYPE (info do nó)
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE expected on 'let' structure",
        Ids.TYPE_ID, data)

        if(data[0].token.idEqual(Ids.ATT_ID)):
            data[0].nexToken(data[0].situation)
            if(data[0].situation == PC.SIG.EndOfProgram): return
        
            data, aux = expr(data, aux) # chama expressão

            data, aux = expr_line(data, aux) # recursão à esquerda

        tmp.addChild(aux)
        if(not data[0].token.idEqual(Ids.COMMA_ID)): # verificar se terá outro ID:TYPE
            break
        
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return

    # ao sair do loop, a raiz terá um total de k-1 filhos
    # cria kaézimo filho (IN)

    # Verifica in
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'in' was expected to close 'let' structure",
    Ids.IN_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    data, tmp = expr(data, tmp) # chama expressão

    data, tmp = expr_line(data, tmp) # recursão à esquerda

    myTree.addChild(tmp)

    return data, myTree

def CASE_func(data, myTree):
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
    # criar raíz
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.CASE)
    tmp.setLine(data[0].token.line)
    tmp.setName(data[0].token.token)

    # Consome token lido
    data[0].nexToken(data[0].situation)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree
    
    # cria filho 1
    data, tmp = expr(data, tmp) # chama expressão
    data, tmp = expr_line(data, tmp) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

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
        aux = st.Node()
        aux.setLabel(st.tag.CASEOPT)
        aux.setName(data[0].token.token)
        aux.setLine(data[0].token.line)

        data[0].nexToken(data[0].situation) # consome ID (filho)

        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # verifica o :
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "':' missing in  'case' structure", Ids.COLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        aux.setType(data[0].token.token)
        # verifica TYPE (filho)
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "TYPE missing in  'case' structure", Ids.TYPE_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # verifica =>
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "'=>' missing in  'case' structure", Ids.F_ATT_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
        
        # cria filho n+2
        
        data, aux = expr(data, aux) # chama expressão

        data, aux = expr_line(data, aux) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

        # ;
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "';' missing in  'case' structure", Ids.SEMICOLON_ID, data)
        
        tmp.addChild(aux)
        
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        
    # Verifica esac
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:  'esac' was expected to close CASE structure",
    Ids.ESAC_ID, data) 
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    myTree.addChild(tmp)

    return data, myTree

def NEW_func(data, myTree):
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
                    (NEW) --- TYPE    
    """
    # cria raiz
    
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.NEW)
    tmp.setName(data[0].token.token)
    tmp.setLine(data[0].token.line)
    tmp.addChild("NULL")

    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    tmp.setType(data[0].token.token)
    # checar TYPE
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE was expected after new",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    myTree.addChild(tmp)
    return data, myTree

def ISVOID_func(data, myTree):
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
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.ISVOID)
    tmp.setName(data[0].token.token)
    tmp.setType('Bool')
    tmp.setLine(data[0].token.line)

    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # cria filho 1
    data, tmp = expr(data, tmp) # chama expressão

    data, tmp = expr_line(data, tmp) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    myTree.addChild(tmp)

    return data, myTree

def NOT_func(data, myTree):
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
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.BOOLOP)
    tmp.setName(data[0].token.token)
    tmp.setType('Bool')
    tmp.setLine(data[0].token.line)

    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # cria filho 1
    data, tmp = expr(data, tmp) # chama expressão

    data, tmp = expr_line(data, tmp) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    myTree.addChild(tmp)

    return data, myTree

def TIDE_func(data, myTree):
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
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.INTOP)
    tmp.setName(data[0].token.token)
    tmp.setType(data[0].token.token)
    tmp.setLine(data[0].token.line)

    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    # cria filho 1
    data, tmp = expr(data, tmp) # chama expressão
    data, tmp = expr_line(data, tmp) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    myTree.addChild(tmp)
    return data, myTree

def O_PARENTHESIS_func(data, myTree):
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
    tmp = st.Node()
    tmp.children = []
    if(myTree.getLabel() == st.tag.FUNCALLID):
        tmp.setLabel(st.tag.ARGUMENT)
    else:
        tmp.setLabel(st.tag.PARENTHESIS)
    tmp.setLine(data[0].token.line)
    tmp.setName(data[0].token.token)

    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): 
        myTree.addChild(tmp)
        return data, myTree
    
     # cria filho 1
    while True:    
        data, tmp = expr(data, tmp) # chama expressão
        data, tmp = expr_line(data, tmp) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

        if(not data[0].token.idEqual(Ids.COMMA_ID)):
            break
        
        data[0].nexToken(PC.SIG.TokenFound)
        myTree.addChild(tmp)
        if(data[0].situation == PC.SIG.EndOfProgram): 
            return data, myTree
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ')' was expected to close '(expr)' structure",
    Ids.C_PARENTHESIS, data)# Verifica )
    if(data[0].situation == PC.SIG.EndOfProgram): # DEsnecess[ario (?)]
        myTree.addChild(tmp)
        return data, myTree

    if(tmp.children == None):
        tmp.addChild()
    myTree.addChild(tmp)
    return data, myTree

def O_BRACKETS_func(data, myTree):
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
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.MULTEXPR)
    tmp.setName(data[0].token.token)
    tmp.setType(data[0].token.token)
    tmp.setLine(data[0].token.line)


    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    # mais de uma expressão
    # então não precisa conferir nesse ponto se na primeira chamada é uma {
    # Já se espera que seja uma expressão a seguir
    while True:
        # cria Nnésimo filho 
        data, tmp = expr(data, tmp) # chama expressão
        data, tmp = expr_line(data, tmp) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ';' expected in multiple expression statement", Ids.SEMICOLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        # tmp.addChild(aux)
        # Se encontroou } então significa que não terá mais chamada de expr
        if(data[0].token.idEqual(Ids.C_BRACKETS)): 
            break

    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:"+ '}' + "expected to close multiple expression statement", Ids.C_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
        
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    myTree.addChild(tmp)

    return data, myTree

def DOT_func(data, myTree):
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
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.DOT)
    tmp.setName(data[0].token.token)
    tmp.setType(data[0].token.token)
    tmp.setLine(data[0].token.line)

    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

        
    data, tmp = expr(data,tmp) # chama expressão

    data, tmp = expr_line(data, tmp) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    myTree.addChild(tmp)

    return data, myTree

def AT_func(data, myTree):
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
                    (AT) --TYPE* -- ID*   1 ou mais filhos
        * une em um nó só? Não, pois ID terá outros filhos
    """
    # cria raiz
    myTree.setLine(data[0].token.line)

    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    myTree.setName(data[0].token.token)
    myTree.setType(data[0].token.token)
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
        
    data, myTree = DOT_func(data, myTree) # passar o trabalho para outra função que irá fazer a mesma coisa
    
    return data, myTree

def OPs_func(data, myTree):
    """
    SOBRE
    -------------
    
    Função para tratar expressão expr OP expr
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
    myTree.setName(data[0].token.token)
    myTree.setLine(data[0].token.line)

    # Consumir token lido
    data[0].nexToken(PC.SIG.TokenFound)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # cria Nnésimo filho 
    
    data, myTree = expr(data, myTree, True) # chama expressão

    data, myTree = expr_line(data, myTree) # recursão à esquerda ## garantir que se não tiver, não irá atrapalhar o resto da estrutura!

    # myTree.addChild(tmp)

    return  data, myTree

def expr_line(data, myTree):
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
    - data  : lista que contém classe de manipulação de tokens, lista de tipos 
    - mytree: árvore semântica modificados

    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    """
    tmp = st.Node()
    tmp.children = []
    tmp.setLabel(st.tag.EXPRL)
    tmp.setLine(data[0].token.line)
    foundexpl = False
    while True:
        # modificados para remover recursão a esquerda # +, -, *, /, <, <=, =
        if(data[0].token.idEqual(Ids.PLUS_ID) or data[0].token.idEqual(Ids.MINUS_ID) or data[0].token.idEqual(Ids.ASTERISK_ID) or data[0].token.idEqual(Ids.F_SLASH_ID)):
            tmp.setLabel(st.tag.INTOP)
            tmp.setType("Int")
            foundexpl = True
            data, tmp = OPs_func(data, tmp)
        elif(data[0].token.idEqual(Ids.LESS_THAN_ID) or data[0].token.idEqual(Ids.LESS_THAN_EQUAL_TO_ID) or data[0].token.idEqual(Ids.EQUAL_TO_ID)):
            tmp.setType("Bool")
            tmp.setLabel(st.tag.BOOLOP)
            foundexpl = True
            data, tmp = OPs_func(data, tmp)
        elif(data[0].token.idEqual(Ids.AT_ID)): # concerteza ao ter um @ terá de ter TYPE.ID depois
            foundexpl = True
            tmp.setLabel(st.tag.FUNCALL)
            data, tmp = AT_func(data, tmp)
        elif(data[0].token.idEqual(Ids.DOT_ID)): # concerteza ao ter um . terá de ter ID depois
            tmp.setLabel(st.tag.FUNCALL)
            foundexpl = True
            data, tmp = DOT_func(data, tmp)
        else:
            break

    if(foundexpl):
        data, tmp =  expr(data, tmp)
        myTree.addChild(tmp)

    return data, myTree
       
def expr(data, myTree, setErr=False):
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
    - data: lista que contém classe de manipulação de tokens, lista de tipos
    - myTree: árvore semântica
    - setRtt: Para casos de expressões com recursão à esquerda. Por essa variável sabe-se se está esperando obrigatoriamente um expressão à direita.
              \nÉ setada novamente a Falso caso entre em alguma função evitando que errôneamente se conclua que não foi encontrada nenhuma expressão

    RETORNO
    -------------
    - data: lista que contém classe de manipulação de tokens, lista de tipos e árvore semântica modificados
    - myTree: retorna estrutura da árvore recebida modificad/atualizada
   
    FORMAÇÃO DA ÁRVORE SEMÂNTICA
    ----------------------------
    A formação da árvore semântica é tratada separadamente para cada tipo de expressão identificada em Cool.
    Isso quer dizer que, em cada função destinada a cada um dos grupos de expressões dispostos abaixo, com 
    exceção de expressões atômicas as quais serão tratadas diretamente na chamada de expr(), haverá a adição
    de nós segundo a regra sintática de cada expressão.
    Pensar ainda em como vai ocorrer a ligação dos símbolos terminais
        - depende do nó anterior de um outro contexto?
        - em qual nó irei ligar?

    TO DO
    -----
    - Otimmizar depois com eval as chamadas
    """
    # Terminais
    if(data[0].token.idEqual(Ids.INTEGER_ID) or data[0].token.idEqual(Ids.STRING_ID) or data[0].token.idEqual(Ids.TRUE_ID) or data[0].token.idEqual(Ids.FALSE_ID)):
        tmp = st.Node()
        tmp.children = []
        tmp.setLine(data[0].token.line)
        tmp.setName(data[0].token.token)
        tmp.setType(data[0].token.id)
        tmp.addChild()
        tmp.setLabel(str(data[0].token.id)[4:-3:])

        data[0].nexToken(PC.SIG.TokenFound)

        myTree.addChild(tmp)

        if(data[0].situation == PC.SIG.EndOfProgram): return data, myTree # desnecessário(ver)
        return data, myTree

    # Recursões a direita
    if(data[0].token.idEqual(Ids.ID_ID)):  
        data, myTree = ID_func(data, myTree) #ID
        setErr = False
    if(data[0].token.idEqual(Ids.IF_ID)):  
        data, myTree = IF_func(data, myTree) #IF
        setErr = False
    
    if(data[0].token.idEqual(Ids.WHILE_ID)): 
        data, myTree= WHILE_func(data, myTree) #WHILE
        setErr = False
    
    if(data[0].token.idEqual(Ids.LET_ID)): 
        data, myTree = LET_func(data, myTree) #LET
        setErr = False
    
    if(data[0].token.idEqual(Ids.CASE_ID)): 
        data, myTree = CASE_func(data, myTree) #CASE
        setErr = False
    
    if(data[0].token.idEqual(Ids.NEW_ID)): 
        data, myTree = NEW_func(data, myTree) #NEW
        setErr = False
    
    if(data[0].token.idEqual(Ids.ISVOID_ID)): 
        data, myTree = ISVOID_func(data, myTree) #ISVOID
        setErr = False
    
    if(data[0].token.idEqual(Ids.NOT_ID)): 
        data, myTree = NOT_func(data, myTree) #NOT
        setErr = False
        
    if(data[0].token.idEqual(Ids.TIDE_ID)): 
        setErr = False
        data, myTree = TIDE_func(data, myTree) #NOT
    
    if(data[0].token.idEqual(Ids.O_PARENTHESIS)): 
        setErr = False
        data, myTree = O_PARENTHESIS_func(data, myTree) #(

    if(data[0].token.idEqual(Ids.O_BRACKETS)): 
        setErr = False
        data, myTree = O_BRACKETS_func(data, myTree)  #{

    else:
        if(setErr):
            data[0].setPs_err(f"line {data[0].token.line}: Expression expected.")
            data[0].addError()
    return data, myTree

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

def ATTRIBUTE_func(data, myTree):
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
    myTree.setLabel(st.tag.ATTRIBUTE)

    _AttName = data[2]
    
    myTree.setType(data[0].token.token)

    # verificar TYPE
    data, attType = checkToken_N_reportSyntError(f"line {data[0].token.line}: " + "No attribute Type declared",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data


    # verificar se há atribuição de valor junto da declaração de um atributo
    if(data[0].token.idEqual(Ids.ATT_ID)):
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return
        data, myTree = expr(data, myTree)
        data, myTree = expr_line(data, myTree)

    data[1][1].newAttribute(_AttName,attType, myTree.getId(), myTree.line)
    return data, myTree

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
            return data, _listOfFormals
        # verifica  :
        data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: ':' expected in formal structure",
        Ids.COLON_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data, _listOfFormals

        # verifica  TYPE
        data, _typeOfFormal = checkToken_N_reportSyntError(f"line {data[0].token.line}: TYPE expected",
        Ids.TYPE_ID, data) 
        if(data[0].situation == PC.SIG.EndOfProgram): return data, _listOfFormals

        _listOfFormals.append((_nameOfFormal,_typeOfFormal))
        if(not data[0].token.idEqual(Ids.COMMA_ID)):
            break
        data[0].nexToken(data[0].situation) # pula o { encontrado extra pois terá mais de uma expressão
        if(data[0].situation == PC.SIG.EndOfProgram): return data, _listOfFormals
    return data, _listOfFormals
    
def METHOD_func(data, myTree:st.Node):#oi
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
    _Methodname = data[2]
    _typeOfReturn = ""
    _listOfFormals = []

    myTree.setLabel(st.tag.METHOD) # informa que é um nó do tipo Método
    if(data[0].token.idEqual(Ids.C_PARENTHESIS)):
        data[0].nexToken(data[0].situation) # pula o { encontrado extra pois terá mais de uma expressão
        if(data[0].situation == PC.SIG.EndOfProgram): return data 
    else:
        # verifica formal obrigatório
        data, _listOfFormals  = formal(data) # N'ao precisa de n[os contendo formals já que temos lista de tipos
        
        myTree.addChild(_listOfFormals,True) # adiciona a lista não como filho (serão somente as expressões)

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

    myTree.setType(_typeOfReturn)
    
    # verifica {
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: {'{'} expected",
    Ids.O_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # ANT:  verifica se tem { extra
    # RESP: não precisa, já tem uma expressão do tipo {expr;^+}

    data, myTree = expr(data, myTree)
    data, myTree = expr_line(data, myTree)

    # } fechar method
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}: {'}'} expected to close methods",
    Ids.C_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data

    data[1][1].newMethod(_Methodname, _typeOfReturn, _listOfFormals,myTree.getLine(), myTree.getId())


    return data, myTree

def FEATURE_func(data):
    """
    Para a árvore sintática retorna uma criança
    """

    tmp = st.Node() # nó temporário
    tmp.children = []

    _name =  ""
    tmp.setLine(data[0].token.line)
    # Verifica ID
    data, _name = checkToken_N_reportSyntError(f"line {data[0].token.line}: ID was expected to initialize a feature",
    Ids.ID_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data, tmp
    data[2] = _name

    tmp.setName(_name)
    if(data[0].token.idEqual(Ids.O_PARENTHESIS)):
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return data, tmp
        data, tmp =  METHOD_func(data, tmp)
        
        return data, tmp
    else:
        # segunda chance só se o token analisado não for :
        if(not data[0].token.idEqual(Ids.COLON_ID) and data[0].afToken().idEqual(Ids.O_PARENTHESIS)):
            data[0].nexToken(PC.SIG.TokenFound)
            if(data[0].situation == PC.SIG.EndOfProgram): return data, tmp
            data, tmp = METHOD_func(data, tmp)
        else:
            if(data[0].token.idEqual(Ids.COLON_ID)): # verifica :
                data[0].nexToken(PC.SIG.TokenFound)
                if(data[0].situation == PC.SIG.EndOfProgram): return data, tmp
                data, tmp = ATTRIBUTE_func(data, tmp)

            elif(data[0].afToken().idEqual(Ids.COLON_ID)): # se o próximo for :
                data[0].nexToken(PC.SIG.TokenFound)
                if(data[0].situation == PC.SIG.EndOfProgram): return data, tmp
                data, tmp = ATTRIBUTE_func(data, tmp)
            else:
                data[0].nexToken(PC.SIG.TokenFound)
                if(data[0].situation == PC.SIG.EndOfProgram): return data, tmp

                data[0].setPs_err(f"line {data[0].token.line}: '('(method) or ':'(attribute) expected")
                data[0].addError()
            

        return data, tmp # retorna filho da função
        
def CLASS_func (data): 
    _className, _typeInherits = "" ,""

    # cria raiz    
    tmp = st.Node()
    tmp.children = []

    # Verifica class
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + "Must be a class declaration",
    Ids.CLASS_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # add nome e linha da classe declarada
    tmp.setName(data[0].token.token)
    tmp.setLine(data[0].token.line)
    tmp.setLabel(st.tag.CLASS)
    # Verifica TYPE
    data, _className = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'class' must be followed by a TYPE",
    Ids.TYPE_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # Verifica inherits (OPCIONAL) só uma chance aos opcionais
    if(data[0].token.idEqual(Ids.INHERITS_ID)):  
        data[0].nexToken(data[0].situation)
        if(data[0].situation == PC.SIG.EndOfProgram): return data

        # add classe herdada
        tmp.setType(data[0].token.token) # adiciona sendo o mesmo nome da classe herdada
        tmp.setInherit(data[0].token.token) # TIRAR??????????????

        # Verifica TYPE
        data, _typeInherits = checkToken_N_reportSyntError(f"line {data[0].token.line}: 'inharits' must be followed by a TYPE",
        Ids.TYPE_ID, data)
        if(data[0].situation == PC.SIG.EndOfProgram): return data
    
    # Para lista de tipos
    data[1][1] = tl.Type(_className, tmp.getId(),tmp.getLine(), _typeInherits)
    data[1][1].methods = []
    data[1][1].attributes = []

    # Verifica {
    data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + " '{'" + f" expected after class declaration",
    Ids.O_BRACKETS, data)
    if(data[0].situation == PC.SIG.EndOfProgram): return data
    # CLASSE VAZIA
    # verifica }
    if(not data[0].token.idEqual(Ids.C_BRACKETS)):
        while True:

            data, child = FEATURE_func(data)
            
            tmp.addChild(child) # adiciona subárvore retornada
            
            # verifica ;
            data, _ = checkToken_N_reportSyntError(f"line {data[0].token.line}:" + " ';'" + f" expected in the end of a feature.",
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

    # Para lista  de tipos
    data[1][0].addType(data[1][1])
    
    # verifica ;
    data, _ = checkToken_N_reportSyntError(endClassError,
    Ids.SEMICOLON_ID, data)
    if(data[0].situation == PC.SIG.EndOfProgram): 
        data[3].append(tmp)
        return data

    data[3].append(tmp) # adiciona um tipo a raíz
    data = CLASS_func(data)

    return data

def program(line):
    myProgram   = PC.Program(line)
    myTypeList  = tl.Creator()
    synTree     = []
    data = [myProgram, [myTypeList,0], "", synTree]

    data = CLASS_func(data)
    
    return data