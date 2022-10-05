nexToken = lambda line: line[1::] 
from Id import Ids
from class_ import Token
import Program_class as PC
myProgram = 0

def errNcompare(errSTR, ID_comp, startWnexToken=True):
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
    Após verificações retorna:

    True: se a lista ficou vazia
    False: se a lista não ficou vazia
    '''
    myProgram.setPs_err(errSTR)
    if(startWnexToken):
        if(isEmpty()):
            return True
    if (not myProgram.token.idEqual(ID_comp)):
        myProgram.addError()
        if(myProgram.afToken.idEqual(ID_comp)): # confere se o próximo é :
                if(isEmpty()): # pula :
                    return True
    return False

def isEmpty():
    if(myProgram.nexToken() == []):
        myProgram.addError()
        return True
    return False
# funções maiúsculas são não terminais
# funções minusculas são terminais
# verificar se é o início de uma nova expressão
# verificar se ele é o término da expressão(mesmo se o erro ocorrer)
# lembrar de guardar linha visitada anteriormente
def expr():
    # procurar não terminais
    # se não for nenhuma das opções erro
    # f"line {myProgram.token.line}: Expression expected"
    pass

def whatEver(line, err):
    # checa terminais antes
    # checa não terminais 
    return line, err

def ATTRIBUTE_func(line, err):
    err_aux = []
    try:
        # Verifica TYPE
        myProgram.setPs_err("line {myProgram.token.line}: Attribute declaration must be followed by a TYPE")
        token = if(myProgram.nexToken() == []):
        return myProgram
        myProgram.setPs_err() # não imprimir erro quando não tiver

        if(token.idEqual(Ids.TYPE_ID)):
            # verificar se tem atribuição
            # myProgram.setPs_err("line {myProgram.token.line}: Atribuition must be followed by 'exp'"
            token = if(myProgram.nexToken() == []):
            return myProgram
            # err_aux = [] # não imprimir erro quando não tiver
            if (token.idEqual(Ids.ATT_ID)):
                return expr(line, err)
                #### Verifica ; ?
            else:
                # myProgram.addError(f"line {myProgram.token.line}: Atribuition must be followed by 'exp'")
                return line, err

        else:
            myProgram.addError(f"line {myProgram.token.line}: Attribute declaration must be followed by a TYPE")
            return line, err

    except IndexError:
        if (not not err_aux):
            myProgram.addError(err_aux)
        return line, err

def formal():
    '''
    Após verificação de formal, retorna:
    True: se a lista ficou vazia
    False: se a lista não ficou vazia
    '''
    # Verifica ID
    ret = errNcompare("line {myProgram.token.line}: ID not founded. Formal expected",
    Ids.ID_ID)
    if(ret): return True
    
    # verifica  :
    ret = errNcompare("line {myProgram.token.line}: ':' expected",
    Ids.COLON_ID)
    if(ret): return True

    # verifica  TYPE
    ret = errNcompare("line {myProgram.token.line}: TYPE expected",
    Ids.TYPE_ID) 
    if(ret): return True

    return False
    
def METHOD_func():
    # verifica formal obrigatório
    if(formal()): return myProgram
    
    myProgram.nexToken()

    if(isEmpty()):
        return myProgram
    
    # Formals opcionais (Só se encontrar um ',')
    while(myProgram.token.idEqual(Ids.COMMA_ID)):
        if(formal()):
           return myProgram 
        elif(isEmpty()):
            return myProgram 

    # verifica )
    ret = errNcompare("line {myProgram.token.line}: ')' expected in method declaration",
    Ids.C_PARENTHESIS))
    if(ret): return myProgram
    
    # verifica :
    ret = errNcompare("line {myProgram.token.line}: ':' expected",
    Ids.COLON_ID)
    if(ret): return myProgram
    
    # verifica TYPE
    ret = errNcompare("line {myProgram.token.line}: TYPE expected",
    Ids.TYPE_ID)
    if(ret): return myProgram

    # verifica {
    ret = errNcompare("line {myProgram.token.line}: '{' expected",
    Ids.O_BRACKETS)
    if(ret): return myProgram
    
    # verifica se tem { extra
    if(myProgram.afToken.idEqual(Ids.O_BRACKETS)): # confere se o próximo(isto é, depois do { obrigatório) é { 

        if(isEmpty()): # pula o { encontrado extra pois terá mais de uma expressão
            return myProgram
        
        expr() # primeiro

        '''Na volta não posso dar next direto, pois em exp vou ter conferido o toke atual, vai que é ';'?'''
        # confere ;<-------------------------------
        ret = errNcompare("line {myProgram.token.line}: ';' expected",
        Ids.SEMICOLON_ID)
        if(ret): return myProgram
        
        # enquanto houver ';'
        while(myProgram.token.isEqual(Ids.SEMICOLON_ID)):
            expr()
            if(isEmpty()):
                return myProgram
        
        # se não tiver expression, isto é, achou o } (primeiro para fechar conjunto de expr)
        ret = errNcompare("line {myProgram.token.line}: '}' expected. You have more than one expr",
        Ids.C_BRACKETS)
        if(ret): return myProgram

    else: # methodo com uma única expressão
        expr()

    # } fechar method
    ret = errNcompare("line {myProgram.token.line}: '}' expected to close methods",
    Ids.C_BRACKETS)
    if(ret): return myProgram

def FEATURE_func():
    #     if(myProgram.nexToken() == []): # pula o ID encontrado
    # return myProgram
    
    # Verifica ID
    ret = errNcompare(f"line {myProgram.token.line}: ID was expected to initialize a feature",
    Ids.ID_ID)
    if(ret): return myProgram


    myProgram.setPs_err("'('(method) or ':'(attribute) expected")
    
    if(isEmpty()):
        return myProgram

    # verifica (
    if(myProgram.token.idEqual(Ids.O_PARENTHESIS)):
        return METHOD_func()
    else:
        if(myProgram.afToken.idEqual(Ids.O_PARENTHESIS)):
            myProgram.addError(f"line {myProgram.token.line}: '('(method) expected")
            if(myProgram.nexToken() == []): # consome (
                return myProgram
            return METHOD_func()

        if(myProgram.token.idEqual(Ids.COLON_ID)): # verifica :
            return ATTRIBUTE_func()

        elif(myProgram.afToken.idEqual(Ids.COLON_ID)):
            myProgram.addError(f"line {myProgram.token.line}: ':'(attribute) expected")
            if(myProgram.nexToken() == []): # consome :
                return myProgram
        else:
            myProgram.addError(f"line {myProgram.token.line}: '('(method) or ':'(attribute) expected")
            return myProgram

def CLASS_func ():

    myProgram.setPs_err(f"line {myProgram.token.line}:" + "Must be a class declaration")

    # Verifica class
    if (not myProgram.token.idEqual(Ids.CLASS_ID)):
        myProgram.addError()
        if(myProgram.afToken.idEqual(Ids.CLASS_ID)): # confere se o próximo é classe
            if(myProgram.nexToken() == []): # pula o class encontrado
                return myProgram
    
    # guarda erro
    myProgram.setPs_err("line {myProgram.token.line}: 'class' must be followed by a TYPE") 
    
    if(myProgram.nexToken() == []):
        myProgram.addError()
        return myProgram

    # Verifica TYPE
    if (not myProgram.token.idEqual(Ids.TYPE_ID)):
        myProgram.addError()
        if(myProgram.token.idEqual(Ids.TYPE_ID)): # confere se o próximo é TYPE
            if(myProgram.nexToken() == []): # pula o TYPE encontrado
                return myProgram

    # guarda erro antes de possível exception
    myProgram.setPs_err("line {myProgram.token.line}:" + " '{'" + f" expected after class declaration") # guarda erro para se ocorrer exceção vai ser esse erro
    if(myProgram.nexToken() == []):
        myProgram.addError()
        return myProgram

    # Verifica inherits (OPCIONAL)
    if(myProgram.token.idEqual(Ids.INHERITS_ID)):  
        # guarda erro antes de possível exception
        myProgram.setPs_err("line {myProgram.token.line}: 'inharits' must be followed by a TYPE")
        if(myProgram.nexToken() == []):
            myProgram.addError()
            return myProgram   

        # Verifica TYPE
        if (not myProgram.token.idEqual(Ids.TYPE_ID)): 
            myProgram.addError()
            if (myProgram.afToken.idEqual(Ids.TYPE_ID)):
                if(myProgram.nexToken() == []): # pula o TYPE encontrado
                    return myProgram
    
    myProgram.setPs_err("line {myProgram.token.line}:" + " '{'" + f" expected after class declaration") 
    if(myProgram.nexToken() == []):
        myProgram.addError()
        return myProgram     
    
    # Verifica {
    if(not myProgram.token.idEqual(Ids.O_BRACKETS)): 
        myProgram.addError()
        if(myProgram.afToken.idEqual(Ids.O_BRACKETS)):
            if(myProgram.nexToken() == []): # pula o { encontrado
                return myProgram 


    myProgram.setPs_err("line {myProgram.token.line}:" + " '}'" + f" expected")
    if(myProgram.nexToken() == []):
        myProgram.addError()
        return myProgram

    # CLASSE VAZIA
    # verifica }
    if(myProgram.afToken.idEqual(Ids.C_BRACKETS)):
        myProgram.setPs_err("line {myProgram.token.line}:" + " ';'" + f" expected in the end of a class declaration")
        if(myProgram.nexToken() == []):
            myProgram.addError()
            return myProgram

        if (not myProgram.token.idEqual(Ids.SEMICOLON_ID)):
            myProgram.addError()
            if(myProgram.afToken.idEqual(Ids.SEMICOLON_ID)):
                if(myProgram.nexToken() == []): # pula o ; encontrado
                    return myProgram
                return CLASS_func() #CONSIDERO CLASSE VAZIA SÓ POR TER } OU SOMENTE COM };
    
    FEATURE_func()

    # guarda erro
    myProgram.setPs_err("line {myProgram.token.line}:" + " '}'" + f" expected")
    if(myProgram.nexToken() == []):
        myProgram.addError()
        return myProgram

    # verifica }
    if(not myProgram.token.idEqual(Ids.C_BRACKETS)):
        myProgram.addError()
        if(myProgram.afToken.idEqual(Ids.C_BRACKETS)):
            if(myProgram.nexToken() == []): # pula o } encontrado
                return myProgram

    # verifica ;
    myProgram.setPs_err("line {myProgram.token.line}:" + " ';'" + f" expected in the end of a class declaration")
    if(myProgram.nexToken() == []):
        myProgram.addError()
        return myProgram
    if (not myProgram.token.idEqual(Ids.SEMICOLON_ID)):
        myProgram.addError()
        if(myProgram.afToken.idEqual(Ids.SEMICOLON_ID)):
            if(myProgram.nexToken() == []): # pula o ; encontrado
                return myProgram

    # se avabou essa classe, a próxima deve ser o início de outra classe
    return CLASS_func()


def IF_func ():
    pass
def WHILE_func():
    pass
def LET_func():
    pass
def CASE_func():
    pass
def NEW_func():
    pass
def ISVOID_func():
    pass
def PLUS_func():
    pass
def MINUS_func():
    pass
def ASTERISK_func():
    pass
def F_SLASH_func():
    pass
def TIDE_func():
    pass
def LESS_THAN_func():
    pass
def LESS_THAN_EQUAL_TO_func():
    pass
def EQUAL_TO_func ():
    pass
def NOT_func():
    pass

def program(line):
    myProgram = PC.Program(line)
    
    return myProgram
