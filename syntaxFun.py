from Id import Ids
import Program_class as PC

def IF_func ():
    myProgram.nexToken(myProgram.situation)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    expr()
    # Verifica Then
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'then' was expected after the 1° 'if' condition",
    Ids.THEN_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    expr()
    # Verifica ELSE
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'else' was expected in 'if' structure",
    Ids.THEN_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    expr()
    # Verifica Fi
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'fi' was expected to close 'if' structure",
    Ids.FI_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    return myProgram

def WHILE_func():
    '''
    SOBRE
    -----------
    Função auxiliar de expr() para expressão WHILE
    '''
    myProgram.nexToken(myProgram.situation)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    
    expr()
    # Verificar Loop
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'loop' expected after 'while' structure condition",
    Ids.LOOP_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    expr()
    # Verificar Pool
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'pool' was expected to close 'while' structure",
    Ids.POOL_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    return myProgram

def LET_func():
    '''
    SOBRE
    -----------
    Função auxiliar de expr() para expressão LET
    '''
    myProgram.nexToken(myProgram.situation)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    while True:
        # Verifica ID
        checkToken_N_reportSyntError(f"line {myProgram.token.line}: ID expected on 'let' structure",
        Ids.ID_ID)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        
        # verifica  :
        checkToken_N_reportSyntError(f"line {myProgram.token.line}: ':' expected on 'let' structure",
        Ids.COLON_ID)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

        # verifica TYPE e resto
        err1 = "line {myProgram.token.line}: TYPE expected on 'let' structure"
        TYPE_ATT_EXPR_verif(err1)

        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

        if(not myProgram.token.idEqual(Ids.COMMA_ID)):
            break
    # Verifica in
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'in' was expected to close 'let' structure",
    Ids.IN_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    return expr()

def expr_line():
    # modificados para remover recursão a esquerda # +, -, *, /, <, <=, =
    while(myProgram.token.idEqual(Ids.PLUS_ID) or myProgram.token.idEqual(Ids.MINUS_ID) or myProgram.token.idEqual(Ids.ASTERISK_ID) or myProgram.token.idEqual(Ids.F_SLASH_ID) or myProgram.token.idEqual(Ids.LESS_THAN_ID) or myProgram.token.idEqual(Ids.LESS_THAN_EQUAL_TO_ID) or myProgram.token.idEqual(Ids.EQUAL_TO_ID)):
        myProgram.nexToken(PC.SIG.TokenFound)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        expr()
        
def CASE_func():
    '''
    SOBRE
    -----------
    Função auxiliar de expr() para expressão CASE
    '''
    myProgram.nexToken(myProgram.situation)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    expr()
    # Verifica Of
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'of' expected on case statement",
    Ids.OF_ID) 
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    myProgram.setPs_err(f"line {myProgram.token.line}:" + "'ID' missing in 'case' structure") # guarda erro para se ocorrer exceção vai ser esse erro
    if(not myProgram.token.idEqual(Ids.ID_ID)): 
        myProgram.addError()

    while(myProgram.token.idEqual(Ids.ID_ID)):
        caseOPT() # verifica :TYPE => expr; obrigatório
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    
    # Verifica esac
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:  'esac' was expected to close CASE structure",
    Ids.ESAC_ID) 
    if(myProgram.situation == PC.SIG.EndOfProgram): return True

def ID_EXPR_func(err=[]):
    '''
    SOBRE
    -----------
    Função auxiliar de expr() para expressão (exp, exp...)
    '''
    while True:
        myProgram.nexToken(PC.SIG.TokenFound)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

        expr()
        
        if(not myProgram.token.idEqual(Ids.COMMA_ID)): # verificar se tem mais parâmetros
            break
    checkToken_N_reportSyntError(err,
    Ids.C_PARENTHESIS) # Verifiicar )
    if(myProgram.situation == PC.SIG.EndOfProgram): return True
    return False

def checkToken_N_reportSyntError(errSTR, ID_comp, isFormal = False):
    '''
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
    ----------------
    Não retorna valores
    '''
    if (not myProgram.token.idEqual(ID_comp)): # se o token procurado não for o atual
        myProgram.setPs_err(errSTR)
        myProgram.addError()
        if(myProgram.afToken().idEqual(ID_comp)): # se o token procurado for o próximo
            myProgram.nexToken(PC.SIG.TokenFound)                  # "fingir" que acertou de primeira
        else:
            if(isFormal):
                myProgram.nexToken(PC.SIG.TokenNotFound) # ir para o próximo token já que o atual foi analisado
            else:
                myProgram.situation = PC.SIG.TokenNotFound
    else:
        myProgram.nexToken(PC.SIG.TokenFound) # ir para o próximo token já que o atual foi analisado

def caseOPT(err=0): # verifica :TYPE => expr; obrigatório
    '''
    SOBRE
    ----------------
    Função para checar a estrutura sintática das opções da expressão CASE
    Obs: o token '.' já foi analizado, portanto, o token 
    atual deve ser um ID para atender a regra sintática
    
    RETORNO
    ----------------
    '''
    myProgram.nexToken(myProgram.situation) # consome ID
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    # verifica o :
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + "':' missing in  'case' structure", Ids.COLON_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    # verifica TYPE
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + "TYPE missing in  'case' structure", Ids.TYPE_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    # verifica =>
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + "'=>' missing in  'case' structure", Ids.F_ATT_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    # expr
    expr()
    # ;
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + "';' missing in  'case' structure", Ids.SEMICOLON_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

def dotCheck():
    '''
    SOBRE
    ----------------
    Função para checar a estrutura do tipo .ID([expr,...])
    Obs: o token '.' já foi analizado, portanto, o token 
    atual deve ser um ID para atender a regra sintática
    
    RETORNO
    ----------------
    '''
    # verificar ID
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: ID expected in expression expr[@TYPE]... after '.'",
    Ids.ID_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    # verificar parênteses
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: '(' expected in expression expr[@TYPE]...",
    Ids.O_PARENTHESIS)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    # )
    if(myProgram.token.idEqual(Ids.C_PARENTHESIS)):
        myProgram.nexToken(PC.SIG.TokenFound)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        return
    else:
        myProgram.undo()
        if(ID_EXPR_func(f"line {myProgram.token.line}: At last one expression expected in expression expr[@TYPE]...")) : return myProgram

def expr():
    '''
    SOBRE
    -------------
    Função principal para tratar de expressões.
    Basicamente a estrutura é dividida em busca por expressões atômicas e não atômicas.
    
    - Expressões Atômicas: são simples, são símbolos terminais da gramática

    - Expressões Não Atômicas: são expressões que possuem símbolos não teminais(pensando na notação de gramática)
        - Dentro de funções 

    RETORNO
    -------------
    Até o momento retorna um objeto da classe Program_class.
    Espera-se adaptar para retornar algo relacionado a árvore semântica.
    '''
    if(myProgram.token.idEqual(Ids.SEMICOLON_ID)):
        return myProgram
    # procurar terminais
    elif(myProgram.token.idEqual(Ids.INTEGER_ID) or myProgram.token.idEqual(Ids.STRING_ID)):
        myProgram.nexToken(PC.SIG.TokenFound)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        return True
    elif(myProgram.token.idEqual(Ids.TRUE_ID) or myProgram.token.idEqual(Ids.FALSE_ID)):
        myProgram.nexToken(PC.SIG.TokenFound)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        return True
    else: # não terminais
        # Com recursão a direita
        if(myProgram.token.idEqual(Ids.ID_ID)): # ID (terminal ou n'ao teminal)
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            
            if(myProgram.token.idEqual(Ids.ATT_ID)): # Verifica Atribuição
                myProgram.nexToken(PC.SIG.TokenFound)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                return expr()
            elif(myProgram.token.idEqual(Ids.O_PARENTHESIS)): # Verifica Chamada de função ID(expr, expr)
                if(myProgram.afToken().idEqual(Ids.C_PARENTHESIS)):
                    myProgram.nexToken(myProgram.situation)

                    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                    myProgram.nexToken(myProgram.situation)

                    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                
                    return myProgram
                if(ID_EXPR_func(f"line {myProgram.token.line}: ')' was expected to close 'ID(expr, expr)' structure")): return myProgram
                return True
            elif(myProgram.token.idEqual(Ids.AT_ID)):
                myProgram.nexToken(PC.SIG.TokenFound)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                
                # verificar TYPE
                checkToken_N_reportSyntError(f"line {myProgram.token.line}: TYPE expected in expression expr[@TYPE]...",
                Ids.TYPE_ID)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                
                # verificar .
                checkToken_N_reportSyntError(f"line {myProgram.token.line}: '.' expected in expression expr[@TYPE]...",
                Ids.DOT_ID)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                
                if(not dotCheck()): return myProgram
                return myProgram
            elif(myProgram.token.idEqual(Ids.DOT_ID)):
                myProgram.nexToken(PC.SIG.TokenFound)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                if(not dotCheck()): return myProgram
                return myProgram
            else:
                expr_line() # adicionar ao fim de todas as outras expressões
                return myProgram
        elif(myProgram.token.idEqual(Ids.NEW_ID)): # new
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            # checar TYPE
            checkToken_N_reportSyntError(f"line {myProgram.token.line}: TYPE was expected after new",
            Ids.TYPE_ID)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            return myProgram
        elif(myProgram.token.idEqual(Ids.O_PARENTHESIS)): # Verificação de (expr)
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            expr()
            # bug2()
            checkToken_N_reportSyntError(f"line {myProgram.token.line}: ')' was expected to close '(expr)' structure",
            Ids.C_PARENTHESIS)# Verifica )
            if(myProgram.situation == PC.SIG.EndOfProgram): return True
        # TIDE e ISVOID e NOT
        elif(myProgram.token.idEqual(Ids.ISVOID_ID) or myProgram.token.idEqual(Ids.NOT_ID) or myProgram.token.idEqual(Ids.TIDE_ID)):
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            return expr()
        elif(myProgram.token.idEqual(Ids.IF_ID)):     # IF
            return IF_func()
        elif(myProgram.token.idEqual(Ids.WHILE_ID)):# WHILE
            return WHILE_func()
        elif(myProgram.token.idEqual(Ids.LET_ID)): # LET
            LET_func()
        # CASE
        elif(myProgram.token.idEqual(Ids.CASE_ID)):
            return CASE_func()
        elif(myProgram.token.idEqual(Ids.O_BRACKETS)):
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            # mais de uma expressão
            while True:
                if(myProgram.token.idEqual(Ids.C_BRACKETS)):
                    myProgram.nexToken(PC.SIG.TokenFound)
                    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                    return True

                ret = expr()

                if(not ret):
                    checkToken_N_reportSyntError(f"line {myProgram.token.line}:"+ '}' + "expected to close multiple expression statement", Ids.C_BRACKETS)
                    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                    return
                checkToken_N_reportSyntError(f"line {myProgram.token.line}: ';' expected in multiple expression statement", Ids.SEMICOLON_ID)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
       # modificados para remover recursão a esquerda # +, -, *, /, <, <=, =
        elif(myProgram.token.idEqual(Ids.PLUS_ID) or myProgram.token.idEqual(Ids.MINUS_ID) or myProgram.token.idEqual(Ids.ASTERISK_ID) or myProgram.token.idEqual(Ids.F_SLASH_ID) or myProgram.token.idEqual(Ids.LESS_THAN_ID) or myProgram.token.idEqual(Ids.LESS_THAN_EQUAL_TO_ID) or myProgram.token.idEqual(Ids.EQUAL_TO_ID)):
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            return expr()
        elif(myProgram.token.idEqual(Ids.SEMICOLON_ID)):
            return myProgram
        else: # se não for nenhuma das opções erro
            myProgram.setPs_err(f"line {myProgram.token.line}: Expression expected")
            myProgram.addError()  
            return False  
        # por while para ficar conferindo até dar não "."
        while (myProgram.token.idEqual(Ids.DOT_ID)):
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            expr()
        return True

def TYPE_ATT_EXPR_verif(err1, err2=[]):
    '''
    SOBRE
    --------
    Função para verificar estrutura TYPE <- expr
    '''
    # verificar TYPE
    checkToken_N_reportSyntError(err1,
    Ids.TYPE_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    # verificar <-
    myProgram.setPs_err(err2) # guarda erro para se ocorrer exceção vai ser esse erro

    if(myProgram.token.idEqual(Ids.ATT_ID)):
        myProgram.nexToken(myProgram.situation)
        if(myProgram.situation == PC.SIG.EndOfProgram): return
        expr()
    else:
        return myProgram

def ATTRIBUTE_func():
    '''
    SOBRE
    ----------
    Função que trata da estrutura de um atributo 
    '''
    err1 = f"line {myProgram.token.line}: " + "No atribute Type declared"
    TYPE_ATT_EXPR_verif(err1)

def formal():
    '''
    SOBRE
    --------
    Função que verifica estrutura de parÂmetro
    '''
    # Verifica ID
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: ID not founded. Formal expected",
    Ids.ID_ID, PC.SIG.IsFormal)
    if(myProgram.situation == PC.SIG.EndOfProgram): return
    elif(myProgram.situation == PC.SIG.TokenNotFound): 
        return
    
    # verifica  :
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: ':' expected",
    Ids.COLON_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return

    # verifica  TYPE
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: TYPE expected",
    Ids.TYPE_ID) 
    if(myProgram.situation == PC.SIG.EndOfProgram): return
    
def METHOD_func():
    if(myProgram.token.idEqual(Ids.C_PARENTHESIS)):
        myProgram.nexToken(myProgram.situation) # pula o { encontrado extra pois terá mais de uma expressão
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram 
    else:
        # verifica formal obrigatório
        formal()
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

        if(myProgram.situation == PC.SIG.TokenFound):
            while(myProgram.token.idEqual(Ids.COMMA_ID)):
                myProgram.nexToken(myProgram.situation) # pula o { encontrado extra pois terá mais de uma expressão
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram 

                formal()
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                # myProgram.nexToken(myProgram.situation)
                # if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        
        # verifica )
        checkToken_N_reportSyntError(f"line {myProgram.token.line}: ')' expected in method declaration",
        Ids.C_PARENTHESIS)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        
    # verifica :
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: ':' expected",
    Ids.COLON_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    
    # verifica TYPE
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: TYPE expected",
    Ids.TYPE_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    # verifica {
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: {'{'} expected",
    Ids.O_BRACKETS)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    
    # verifica se tem { extra
    if(myProgram.token.idEqual(Ids.O_BRACKETS)): # confere se o próximo(isto é, depois do { obrigatório) é {
        myProgram.nexToken(myProgram.situation) # pula o { encontrado extra pois terá mais de uma expressão
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram 

        semiCommaErr = f"line {myProgram.token.line}: ';' expected"
        while True:
            expr()
            if(not myProgram.token.idEqual(Ids.DOT_ID)):
                if(not myProgram.token.idEqual(Ids.SEMICOLON_ID)):
                    myProgram.setPs_err(f"line {myProgram.token.line}: {';'} expected in the end of an expression when more than one expression are added in a method")
                    myProgram.addError()
                    break
                myProgram.nexToken(myProgram.situation) # pula ';'
    
                if(myProgram.token.idEqual(Ids.C_BRACKETS)): # evitar um erro de falta de expressão só porque o próximo é '}', o que seria correto nesse ponto do código
                    break
            else:
                myProgram.nexToken(myProgram.situation)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram 

        # verifica } fecha expr múltiplas
        checkToken_N_reportSyntError(f"line {myProgram.token.line}: {'}'} expected. You have more than one expr",
        Ids.C_BRACKETS)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    else: # method com uma única expressão
        expr()

    # } fechar method
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: {'}'} expected to close methods",
    Ids.C_BRACKETS)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    return myProgram

def FEATURE_func():
    # Verifica ID
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: ID was expected to initialize a feature",
    Ids.ID_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    if(myProgram.token.idEqual(Ids.O_PARENTHESIS)):
        myProgram.nexToken(myProgram.situation)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        return METHOD_func()
    else:
        # segunda chance só se o token analisado não for :
        if(not myProgram.token.idEqual(Ids.COLON_ID) and myProgram.afToken().idEqual(Ids.O_PARENTHESIS)):
            myProgram.nexToken(PC.SIG.TokenFound)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            return METHOD_func()
        else:
            if(myProgram.token.idEqual(Ids.COLON_ID)): # verifica :
                myProgram.nexToken(PC.SIG.TokenFound)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                return ATTRIBUTE_func()
            elif(myProgram.afToken().idEqual(Ids.COLON_ID)): # se o próximo for :
                myProgram.nexToken(PC.SIG.TokenFound)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
                return ATTRIBUTE_func()
            else:
                myProgram.nexToken(PC.SIG.TokenFound)
                if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

                myProgram.setPs_err(f"line {myProgram.token.line}: '('(method) or ':'(attribute) expected")
                myProgram.addError()
                return myProgram

def CLASS_func ():    
    # Verifica class
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + "Must be a class declaration",
    Ids.CLASS_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    
    # Verifica TYPE
    checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'class' must be followed by a TYPE",
    Ids.TYPE_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram

    # Verifica inherits (OPCIONAL) só uma chance aos opcionais
    if(myProgram.token.idEqual(Ids.INHERITS_ID)):  
        myProgram.nexToken(myProgram.situation)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
        # Verifica TYPE
        checkToken_N_reportSyntError(f"line {myProgram.token.line}: 'inharits' must be followed by a TYPE",
        Ids.TYPE_ID)
        if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    
    # Verifica {
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + " '{'" + f" expected after class declaration",
    Ids.O_BRACKETS)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    # CLASSE VAZIA
    # verifica }
    if(not myProgram.token.idEqual(Ids.C_BRACKETS)):
        while True:
            FEATURE_func()
            # verifica ;
            checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + " ';'" + f" expected in the end of a feature on {myProgram.token.token}",
            Ids.SEMICOLON_ID)
            if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
            
            if(not myProgram.token.idEqual(Ids.ID_ID)):
                break
    endClassError = f"line {myProgram.token.line}:" + " ';'" + f" expected to close class"
    # verifica }
    checkToken_N_reportSyntError(f"line {myProgram.token.line}:" + " '}'" + f" expected o close class statement",
    Ids.C_BRACKETS)
    if(myProgram.situation == PC.SIG.EndOfProgram): 
        myProgram.setPs_err(endClassError)
        myProgram.addError()
        return myProgram
    # verifica ;
    checkToken_N_reportSyntError(endClassError,
    Ids.SEMICOLON_ID)
    if(myProgram.situation == PC.SIG.EndOfProgram): return myProgram
    
    return CLASS_func()

def program(line):
    # global cont
    global myProgram
    myProgram = PC.Program(line)
    
    ret = CLASS_func()

    return myProgram
