import json
import os
from synTree import Node, tag
import TYPE_LIST as TL
import coolToBril as CB

global TYPE_LIST
TYPE_LIST = []

def findComplement(num):
    ans = 0;
    x = 0;
    i = 0;
    while(num > 0):
        if (num % 2 == 1):
            x = 0;
        else:
            x = 1;
 
        ans += pow(2, i) * x;
        num //= 2;
        i += 1;
 
    return ans;

class Analyzer:
    stringValueFunctionCall = ""
    treeCopy = None
    ''' Para análise de escopo'''
    calledClass = ""
    calledMethodIndex = 0
    inAcall = False
    classId             = -1 
    classInheritedId    = -1 


    classScope          = -1 
    classInheritedScope = -1 

    methodScope         = 0  
    attributeScope      = 0 
    
    scope               = [] 
    scopeLet            = [] 
    '''
     [(name, type, value)]
    '''
    self_type           = [] 
    typeListAnalyzer:TL.Creator
    errs = [] 
    def resetFeauture(self):
        self.inLet              = False
        self.scopeLet           = [] 
        self.computeResult      = False   
        self.lastValue          = 0  
        self.lastTypeReturned   = '' 
        '''
        Em caso de chamada de função para outra classe, a próxima classe pode apresentar chamada de função também, então o self_type mais atual será da classe atual
        '''
        self.wasIf              = False
    def resetClass(self):
        self.methodScope        = 0  
        self.attributeScope     = 0 

    ''' Histórico de valores (tipo e valor) '''
    lastValue           = 0  
    lastTypeReturned = '' 
   
    def __init__(self, typeList:TL.Creator):
        self.typeListAnalyzer = typeList
    '''
    Para bug
    '''
    wasCall = False
    wasNew = False 
    wasIf = False  
    blockGoAhead = False 
    pauseErro   = False 
    
    def wasInIf(self): self.wasIf = not self.wasIf 
    
    def pauseErros(self):  self.pauseErro = False 

    ''' 
    FUNÇÕES AUXILIARES GERAIS
    '''
    def typeIndex(self, className):
        return self.typeListAnalyzer.getClassIndex(className)
    def getTypes(self):
        '''
        SOBRE
        -----
        Retorna a lista de tipos'''
        return self.typeListAnalyzer.typeList

    def hasClass(self, className, line = "*", msg = " "):
        '''
        SOBRE
        -----
        Verifica se uma classe existe.
        Casos em expressões:
            - let
            - Chamada de funções
            - case
            - new

        PARÂMETRO
        ----------
        - className: nome da classe
        - line: linha de possível erro
        - mensagem personalizada
        
        RETORNO
        -------
        - [] :  Se a classe não existe
        - obj:  Se a classe existe
        '''
        obj = self.typeListAnalyzer.getClass(className)

        
        if(not obj and className != "-" and className != ""):
            self.addError(f"<{line}>{msg}Class '{className}' is not defined.")
            return obj
        try:
            return obj[0]
        except:

            return obj
            
    def hasMethod(self, className, methodName, line="*"):
        '''
        SOBRE
        -----
        Verifica se um método existe no escopo procurado

        PARÂMETRO
        ----------
        - className: nome da classe
        - methodName: nome do método
        - line: linha de possível erro
        
        RETORNO
        -------
        - []:    Se o método não existe
        - obj: Se não retorna False
        '''
        obj = self.typeListAnalyzer.getClass(className)[0].getMethod(methodName)
        if(not obj):
            self.addError(f"<{line}> Method '{methodName}' is not defined in the class '{className}'.")
            return obj
        return obj[0]

    def compatibleType(self,_type, rType): 
        '''
        SOBRE
        -----
        Função que verifica se dois tipos são iguais. A função é útil para verificar se um valor retornado é do mesmo tipo da estrutura
        '''
        
        if(_type == rType or _type == '-' or rType =="Object"): return True
        else: return False

    def checkType(self, obj:TL.Type): 
        ''' 
        SOBRE
        -----
        Método para verificações sobre a lista de tipos mapeada durante a análise sintática.
        Quanto a classe, verifica-se:
            - Se uma calsse de mesmo nome já foi declarada
            - Se o tipo herdado pela classe existe
            - Se não "herda" do tipo Bool ou Int ou String
        '''
        if(obj.duplicated): 
            if(obj.name.lower() in ['object','io','int','string','bool'] and obj.line!="BC"):
                self.addError(f"<{obj.line}> Class '{obj.name}' is Cool's basic class. You are not allowed to redefine it.")
            else: self.addError(f"<{obj.line}> Class '{obj.name}' declared multiple times.")

        
        if(obj.parent!=""):
            if(obj.parent.lower() in ['int','bool','string']): self.addError(f"<{obj.line}> It isn't allowed to inherit from '{obj.parent}' type.")
            if(not self.typeListAnalyzer.getClass(obj.parent)): self.addError(f"<{obj.line}> Class '{obj.name}' inherits class '{obj.parent}', but this class is not defined.")
    
    def addError(self, msg):
        '''
        SOBRE
        -----
        Função que adiciona nova mensagem de erro  
        '''
        if(not self.pauseErro):
            self.errs.append(msg)
        else:
            self.pauseErros()

    '''
    REFERENTE AO ESCOPO : ACHO QUE NÃO VOU USAR
    '''
    def setScope(self, classI, methodI = -1, attributeI = -1): 
        
        self.classScope = classI
        if (self.getTypes()[classI].parent != ""): 
            self.classInheritedScope =  [self.typeListAnalyzer.typeList.index(c) for c in self.typeListAnalyzer.typeList if c.name == self.typeListAnalyzer.typeList[classI].parent][0]
        
        
        self.methodScope = methodI
        self.attributeScope = attributeI
        
    ''' 
    FUNÇÕES AUXILIARES PARA O LET
    '''
    inLet               = False 
    def popLet(self):
        if(self.scopeLet != []):
            self.scopeLet.pop()
    def setLet(self):
        if(self.inLet): 
            if(self.scopeLet==[]): self.inLet = False
        else: self.inLet = not self.inLet

    def setScopeLet(self, letOpts): self.scopeLet.append(letOpts)
    
    def getVarLet(self, obj): 
        for letScops in self.scopeLet[::-1]: 
            r = [var for var in letScops if obj.name == var[0]]
            if(r!=[]):
                self.lastTypeReturned, self.lastValue = r[0][1], r[0][2]
                
                return 

        self.inLet = False
        self.blockGoAhead = True
        ID(obj)               
        self.blockGoAhead = False
        self.inLet = True

    def setVarLet(self, name, line): 
        for i, letScopes in enumerate(self.scopeLet[::-1]): 
            r = [var for var in letScopes if name == var[0]] 
            if(r!=[]):
                toIndex = letScopes.index(r[0])
                self.scopeLet[i][toIndex][2] = analyzer.lastValue
                if (not analyzer.compatibleType(self.scopeLet[i][toIndex][1], analyzer.lastTypeReturned)): 
                    analyzer.addError(f"<{line}> '{name}' is defined as '{self.scopeLet[i][toIndex][1]}'. '{self.scopeLet[i][toIndex][2]}' is not assignable to '{analyzer.lastTypeReturned}'.") 
                
                return True
        return False
    ''' 
    FUNÇÕES AUXILIARES PARA EXECUTAR INSTRUÇÕES EM COOL
    '''
    computeResult    = False   

    def getResult(self, op, x, y = 0): 
        if(self.computeResult):
            x = True if x == "true" else False if x == "false" else x
            y = True if y == "true" else False if y == "false" else y
            if(op == "="): op = "=="
            elif(op == "/"): op = "//"
            
            if(op == "not"): self.lastValue =  not x
            elif(op=="~"): self.lastValue =  findComplement(int(x))
            
            else: self.lastValue = eval(f"{x} {op} {y}")
    
    ''' 
    FUNÇÕES AUXILIARES PARA PRÉ ANÁLISE
    '''
    def checkMethod(self, obj:TL.Method): 
        '''
        SOBRE
        -----
        Método para verificações sobre a lista de tipos mapeada durante a análise sintática.
        Quanto a cada método de uma classe, verifica-se:
            - Se um método de mesmo nome já foi declarado
            - Se o tipo retornado pelo método existe
            - Sobre os parâmetros:
                - Se um parâmetro de mesmo nome está sendo passado 
                - Se o tipo do parâmetro passsado existe
        '''
        
        if(obj.duplicated):
            self.addError(f"<{obj.line}> Method '{obj.name}' was already defined.")
            
        
        if(not self.typeListAnalyzer.getClass(obj._type)):
            if(obj._type != "SELF_TYPE"):
                self.addError(f"<{obj.line}> Method '{obj.name}' returns type '{obj._type}', but this type is not defined.")

        
        for cont,f in enumerate(obj.formals):  

            
            if(len([comp for comp in obj.formals if f[0] == comp[0]]) != 1): 
                self.addError(f"<{obj.line}> Formal '{f[0]}'(formal {cont}) was already defined.")
            
            
            if(not self.typeListAnalyzer.getClass(f[1])):
                if(obj._type != "SELF_TYPE"):
                    self.addError(f"<{obj.line}> Formal '{f[0]}'(formal {cont}) has type '{f[1]}', but this type is not defined.")
    def checkAttribute(self, obj:TL.Attribute):
        '''
        SOBRE
        -----
        Método para verificações sobre a lista de tipos mapeada durante a análise sintática.
        Quanto a cada atributo de uma classe, verifica-se:
            - Se o atributo de mesmo nome já foi declarado
            - Se o atributo foi declarado com um tipo tipo existe
        '''
        
        if(obj.duplicated):
            self.addError(f"<{obj.line}> Attribute '{obj.name}' was already defined.")
            
        
        if(not self.typeListAnalyzer.getClass(obj._type)):
            if(obj._type != "SELF_TYPE"):
                self.addError(f"<{obj.line}> Attribute '{obj.name}' has type '{obj._type}', but this type is not defined.")
    
    """
    Para fazer a geração de código
    """
    toBril = True
    brilInstruction = []
    brilFunction = []
    def setInstr(self, inst):
        self.brilInstruction.append(inst)
    def setFunc(self, func):
        self.brilFunction.append(func)


def IF          (e:Node):
    '''
    Só faz verificação das expressões
    '''

    rType = [0,0,0] 
    rValue = [0,0,0] 

    for i, c in enumerate(e.children):
        rType[i] = exprAnalyzer(c) 
        rValue[i] = analyzer.lastValue
        if(i == 1 and (rValue[0] == True or rValue == 'true')): 
            break

    
    if (i == 0 and not analyzer.compatibleType(e._type, analyzer.lastTypeReturned)): 
        analyzer.addError(f"<{e.line}> The <expr> {i+1} returned {rType[i]} but Bool was expected.") 
    
    if(rValue[0] == True or rValue[0] == "true"):
        
        analyzer.lastValue = str((rValue[1])).lower() if rValue[1] in [True,False] else rValue[1]
        analyzer.lastTypeReturned = rType[1]
        analyzer.wasInIf()
        return rType[1]
    
    else:
        
        analyzer.lastValue = str(rValue[2]).lower() if rValue[2] in [True,False] else rValue[2]
        analyzer.lastTypeReturned = rType[2] 
        analyzer.wasInIf()
        return rType[2] 
def MULTEXPR    (e:Node):

    for expr in e.children:
        if((expr._type in ['Bool', 'Int', 'String'] or expr.getLabel() == tag.NEW) and expr.getLabel() != tag.BOOLOP and expr.getLabel() != tag.INTOP and expr.label != tag.IF):
            if(expr._type in ['Bool', 'Int', 'String']):
                
                    
                analyzer.lastValue = expr.name
                analyzer.lastTypeReturned = expr._type
        else:
            eval(str(expr.getLabel().name)+"(expr)")

    return analyzer.lastTypeReturned

def WHILE       (e:Node): 
    '''
    Só faz verificação das expressões
    '''
    r = True
    while r:
        exprAnalyzer(e.children[1])
        exprAnalyzer(e.children[0])
        if (not analyzer.compatibleType(e._type, analyzer.lastTypeReturned)): 
            analyzer.addError(f"<{e.line}> First while branch returned {analyzer.lastTypeReturned} but Bool was expected.") 
        r = analyzer.lastValue
    
def BOOLOP      (e:Node):
    '''
    SOBRE
    -----
    Função para verificação de expressão de operações matemáticas <,<=,=   
    Deverá ser verificado:
     - Se o tipo retornado da expressão expr em -> expr<OP> é do tipo Int !!!! Pode ter qualquer tipo
     - Se o tipo retornado da expr em --> <OP>expr é do tipo Int

     RETORNO
     --------
     - Tipo Bool
    '''
    if(e.getName()!="not" and e.getName()!="="): 
        
        if(not analyzer.compatibleType('Int', analyzer.lastTypeReturned)):
            analyzer.addError(f"<{e.line}> The expression (<expr>{e.name}) was supposed to return Int, not {analyzer.lastTypeReturned}.")
        else:
            analyzer.computeResult = True
            x = analyzer.lastValue 
    
    analyzer.computeResult = True 
    x, leftType = analyzer.lastValue, analyzer.lastTypeReturned 
    '''
    Guarda o valor e o tipo retornado da expressão da esquerda
    Isso para saber se o valor da expressão da direita vai ser compatível com o anterior
    '''

    
    for expr in e.children: 
        rType  = exprAnalyzer(expr) 
    if(e.name == "not"): 
        comp = 'Bool'
        leftType = 'Bool' 
        x = analyzer.lastValue
    else:
        comp = leftType
    
    if(not analyzer.compatibleType(comp, rType)): 
        analyzer.addError(f"<{e.line}> The expression ({e.name}<expr>) was supposed to return {comp}, not {rType}.")
    else: 
        if(analyzer.toBril):
            ag1 = x
            arg2 =analyzer.lastValue
            op_arg = CB.convertOp(e.getName()) 
            analyzer.setInstr(CB.instr(op = op_arg,x = ag1,y = arg2))
        comp = int if leftType=="Int" else str
        analyzer.getResult(e.getName(), (comp)(x), (comp)(analyzer.lastValue))

    analyzer.lastTypeReturned = "Bool"
    return "Bool" 
def INTOP       (e:Node):
    '''
    SOBRE
    -----
    Função para verificação de expressão de operações matemáticas +,-,/,*    
    Deverá ser verificado:
     - Se o tipo retornado da expressão expr em -> expr<OP> é do tipo Int
     - Se o tipo retornado da expr em --> <OP>expr é do tipo Int

     RETORNO
     --------
     - último tipo retornado
        OBS: Caso ocorra o retorno de um tipo não correspondente, a póxima verificação não será válida, pois como nessa expressão
        as regras não foram atendidas não tem porque verificar o que não retornaria nada
    '''
    if(e.name != "~"):
        
        if(not analyzer.compatibleType('Int', analyzer.lastTypeReturned)):
            analyzer.addError(f"<{e.line}> The expression (<expr>{e.name}) was supposed to return Int, not {analyzer.lastTypeReturned}.")
        else:
                analyzer.computeResult = True
                x = analyzer.lastValue 
    analyzer.computeResult = True 
    x, leftType = analyzer.lastValue, analyzer.lastTypeReturned 
    '''
    Guarda o valor e o tipo retornado da expressão da esquerda
    Isso para saber se o valor da expressão da direita vai ser compatível com o anterior
    '''

    
    for expr in e.children: 
        rType  = exprAnalyzer(expr) 
    
    if(not analyzer.compatibleType('Int', rType)): 
        analyzer.addError(f"<{e.line}> The expression ({e.name}<expr>) was supposed to return Int, not {rType}.")
    else: 
        if(analyzer.toBril):
            ag1 = x
            arg2 =analyzer.lastValue
            op_arg = CB.convertOp(e.getName()) 
            analyzer.setInstr(CB.instr(op_arg,ag1,arg2))

        analyzer.getResult(e.getName(), (int)(x), (int)(analyzer.lastValue))
    
    analyzer.lastTypeReturned = rType
    return rType 
def ASSIGNMENT  (e:Node):
    exprAnalyzer(e.children[0]) 
    
    if((e.children[0].label == tag.NEW and e.children[0].children != []) or (e.children[0].label == tag.PARENTHESIS and e.children[0].children[0].label == tag.NEW)): 
        
        if(not analyzer.wasNew): 
            if(e.children[1].label == tag.FUNCALL):
                FUNCALL(e.children[1])
    ID(e, True)


def CASE        (e:Node):
    
    for caseOPT in e.children:
        pass
    '''  primeiro filho é a expressao a ser analisada (o valor retornado que será utilizado
        o filho é um opt 
        compara valor
        se for igual
            calcula atribuição 
            compara tipo com ulttiporetornad
                        ultimo 
            
        se não for igual
            vai pro próximo
    '''
def CASEOPT     (e:Node):
    pass

def IO(methodName, arg = None):

    if(methodName in ('out_string','out_int')):
        if(isinstance(arg[0][0], int)):
            print(arg[0][0])
        elif('"' in arg[0][0]): 
            print(arg[0][0][2:-2:])
        else:
            print(arg[0][0])
        analyzer.lastTypeReturned = "SELF_TYPE"
        return 'SELF_TYPE'

    elif(methodName in ('in_string', 'in_int')):
        try:
            analyzer.lastValue  = int(input()) if methodName == 'in_int' else input()
        except ValueError as ve:
            print(f'<input Erro>You entered with a String input, which is not a Int.Try again(last chance)')
            try:
                analyzer.lastValue  = int(input()) if methodName == 'in_int' else input()
            except ValueError as ve:
                print(f'<input Erro>You entered with a String input again, which is not a Int.')

        analyzer.lastTypeReturned  = 'Int' if methodName == 'in_int' else 'String'

        if(methodName == "in_string" and isinstance(analyzer.lastValue, int)): 
            analyzer.stringValueFunctionCall = analyzer.lastValue

        return analyzer.lastTypeReturned

        
def String(methodName, arg=None):
    if(methodName=="length"):
        analyzer.lastTypeReturned = 'Int'
        analyzer.lastValue = len(arg[0])
    elif(methodName == 'concat'):
        if(isinstance(arg, tuple) and arg!=None):
           analyzer.lastValue = analyzer.stringValueFunctionCall + arg[0]
        else: 
            analyzer.lastValue = f"{analyzer.stringValueFunctionCall} {arg[0][0][1:-1:]}" 
            print("<concatMostra> ", analyzer.stringValueFunctionCall)
        analyzer.stringValueFunctionCall = analyzer.lastValue
        analyzer.lastTypeReturned = "String"
    elif(methodName == "substr"):
        ret = (analyzer.stringValueFunctionCall[2:-1:])[int(arg[0][0]):int(arg[1][0]):]
        analyzer.lastTypeReturned = "String"
        analyzer.lastValue = ret
        analyzer.stringValueFunctionCall = ret
def FUNCALL     (e:Node):
    FUNCALLID(e.children[0].children[0], True)
    
def confere(a,b,c,d, e, f,g, confereMeth = 0, confereClass = 0):
    print("Id da classe atual = ", a)
    print("Id do método = ", b)
    print("Chamada da classe = ",c)
    print("Chamada do método = ",d)
    print("Argumentos = ",e)
    print("Achou método\nFormals=", f.formals) if f!=[] else print("Método não definido")
    print("Se todos os args tem tipo de formals = ", g)
    print(f"CONFERE: {confereMeth=}/{confereClass=}")
    print("\n*****\n")
    os.system("PAUSE")
    os.system("CLS")

def FUNCALLID   (e:Node, fromNew = False):
    exists = True
    argsMatchFormals = None

    if(not fromNew or analyzer.lastTypeReturned == analyzer.self_type[0]): 
        
        className = analyzer.self_type[0]

    else:
        className   = analyzer.lastTypeReturned
        
        exists = False if analyzer.hasClass(className, e.line) == [] else True

    if(exists):
        classObj = analyzer.hasClass(className, e.line)

        methodName  = e.name
        arguments   = [] 

        for argument in e.children[0].children:
            exprAnalyzer(argument)
            arguments.append([analyzer.lastValue,analyzer.lastTypeReturned])
            
        methodObj = analyzer.hasMethod(className, methodName, e.line)

        if(methodObj):   
            argsMatchFormals = not (False in [ argType[1] ==  forType[1] for argType,forType in zip(arguments, methodObj.formals)])
            
        else: 
            classInheritedName = analyzer.hasClass(className, e.line).parent
            if classInheritedName != '':
                classInheritedObj = analyzer.hasClass(classInheritedName, e.line)
                methodObj = analyzer.hasMethod(classInheritedName, methodName, e.line)

                if(methodObj):
                    analyzer.addError(f"<{e.line}> Method '{methodName}' is not defined in the class '{className}', but it is defined in the class inherited ('{classInheritedName}').")
                    classObj =  classInheritedObj
                    argsMatchFormals = not (False in [ argType[1] ==  forType[1] for argType,forType in zip(arguments, methodObj.formals)])
            else:
                analyzer.addError(f"<{e.line}> {className} do not inherits from any class. Invalid method call ({methodName})")

        if(argsMatchFormals):
            if(classObj.scopeId >= 1000): 
                ret = eval(f"{str(classObj.name)}(methodObj.name, arguments)") 
                if(ret == 'SELF_TYPE'):
                    analyzer.lastTypeReturned = classObj.name
            else: 
                found = False
                for _class in analyzer.treeCopy:
                    if(_class.name == classObj.name):
                        found = True
                        for method in _class.children:
                            if(method.name == methodObj.name):
                                classInfo = analyzer.getTypes()[analyzer.typeIndex(classObj.name)]
                                methodIndex = classInfo.methodIndex(methodObj.name) 
                                analyzer.calledMethodIndex = methodIndex
                                for arg, f in zip(arguments, methodObj.formals): 
                                    analyzer.getTypes()[analyzer.typeIndex(classObj.name)].methods[methodIndex].setValue(arg[0], f)
                                analyzer.inAcall = True
                                analyzer.calledClass = classObj.name
                                methodAnalyzer(method)

                                analyzer.inAcall = False
                if(not found):
                    print("ERRO NA CHAMADA")
            if (analyzer.toBril):
                analyzer.setFunc( CB.Function(name = methodObj.name,_type = methodObj._type, args = arguments, instr = analyzer.brilInstruction))
                
        else:
            if argsMatchFormals != None:
                analyzer.addError(f"<{e.line}> Method formals types did not match with the ones used as arguments. {methodName}({methodObj.formals}) -- {methodName}({methodObj.formals})")

    if(analyzer.toBril):
        m = CB.Master(functions = analyzer.brilFunction)
        with open("sample.json", "w") as outfile:
            json.dump(m.to_dict(), outfile)

def LET         (e:Node):
    letVars = [] 
    analyzer.setLet()
    for l in e.children:
        if(l.label==tag.MULTEXPR):
            if(not letVars): 
                exprAnalyzer(l)
            else: 
            
                analyzer.setScopeLet(letVars)
                letVars = []
                exprAnalyzer(l)
        else:
            
            if(l.children != []):
                ID(l)
                
                if (not analyzer.compatibleType(l._type, analyzer.lastTypeReturned)): 
                    if(l._type=='new'):
                        analyzer.addError(f"<{l.line}> '{l.name}' is defined as '{l.name}'. '{l._type}' is not assignable to '{analyzer.lastTypeReturned}'.") 
                    else:
                        analyzer.addError(f"<{l.line}> '{l.name}' is defined as '{l._type}'. '{l._type}' is not assignable to '{analyzer.lastTypeReturned}'.") 
                if(True): 
                    letVars.append([l.name, l._type, analyzer.lastValue])
            else:
                letVars.append([l.name, l._type, analyzer.lastValue])
            
    
    analyzer.popLet()
    analyzer.setLet()

    return analyzer.lastTypeReturned
def PARENTHESIS (e:Node):
    for expr in e.children:
        exprAnalyzer(expr)

def ID(e:Node, ass = False):
    if(analyzer.inLet): 
        if((e.label==tag.ASSIGNMENT or e.label==tag.LETOPT  )): 
            if(not analyzer.wasCall):
                exprAnalyzer(e.children[0]) 
                if(analyzer.wasNew):
                    FUNCALL(e.children[1])

                if(not analyzer.setVarLet(e.name, e.line)):
                    analyzer.inLet = False
                    ID(e, True)
                    analyzer.inLet = True
            else:
                analyzer.wasCall = False
        else: 
            
            analyzer.getVarLet(e)
            if(e.children != []):
                exprAnalyzer(e.children[0])

            
            return analyzer.lastTypeReturned
    else:
        
        classInfo = analyzer.getTypes()[analyzer.classScope]
        if(analyzer.methodScope == -1 or classInfo.methods == []):
            IDefined = False
        else: 
            IDefined = False
            formals =  classInfo.methods[analyzer.methodScope].formals
            if(formals != []):
                IDefined = [formal for formal in formals if formal[0]==e.name]
                IDefined = IDefined if IDefined==[] else IDefined[0]

                if(IDefined):
                    if(ass ): 
                        if (not analyzer.compatibleType(IDefined[1], analyzer.lastTypeReturned)): 
                            analyzer.addError(f"<{e.line}> '{e.name}' is defined as '{IDefined[1]}'. '{IDefined[1]}' is not assignable to '{analyzer.lastTypeReturned}'.") 
                        else:
                            analyzer.getTypes()[analyzer.classScope].methods[analyzer.methodScope].setValue(analyzer.lastValue, IDefined)
                    else:
                        analyzer.lastValue, analyzer.lastTypeReturned = analyzer.getTypes()[analyzer.classScope].methods[analyzer.methodScope].getValue(IDefined)
                        if(analyzer.blockGoAhead):
                            return analyzer.lastTypeReturned
        if not IDefined: 
            IDefined  = [a for a in classInfo.attributes if a.name == e.name]
            IDefined = IDefined if IDefined==[] else IDefined[0]
            
            if not IDefined: 
                IDefined  = [a for a in analyzer.getTypes()[analyzer.classInheritedScope].attributes if a.name == e.name]
                
                IDefined = IDefined if IDefined==[] else IDefined[0]
            if(ass): 
                try:
                    if (not analyzer.compatibleType(IDefined._type, analyzer.lastTypeReturned)):
                        analyzer.addError(f"<{e.line}> '{e.name}' is defined as '{IDefined._type}'. '{IDefined._type}' is not assignable to '{analyzer.lastTypeReturned}'.") 
                    else:
                        if(e.children != 0): 
                            for c in e.children:
                                exprAnalyzer(c)
                        analyzer.getTypes()[analyzer.classScope].attributes[classInfo.attributes.index(IDefined)].setValue(analyzer.lastValue)
                except Exception as ex:
                    
                    analyzer.pauseErros()
            else:
                if(analyzer.inAcall):
                    indexClass = analyzer.typeIndex(analyzer.calledClass)
                    analyzer.lastValue = analyzer.getTypes()[indexClass].methods[analyzer.calledMethodIndex].getValue(e.name)
                    if(analyzer.lastValue == []):
                        obj = analyzer.getTypes()[indexClass].attributes
                        analyzer.lastValue = analyzer.getTypes()[analyzer.classScope].attributes[obj.index(e.name)].getValue()
                else:
                    analyzer.lastValue = analyzer.getTypes()[analyzer.classScope].attributes[analyzer.attributeScope].getValue()
                    
                if(analyzer.blockGoAhead): return analyzer.lastTypeReturned

        if(not IDefined ): 
            if(e.label!=tag.LETOPT): analyzer.addError(f"<{e.line}> '{e.name}' is not defined in this scope")
            
        else: 
            if(isinstance(IDefined, tuple)):  analyzer.lastTypeReturned = IDefined[1]
            else:
                analyzer.lastTypeReturned = IDefined._type
                analyzer.lastValue = IDefined.value 
            if(e.children != 0 ): 
                for c in e.children: exprAnalyzer(c)
                    
        return analyzer.lastTypeReturned

def exprAnalyzer(expr: Node):
    """
    SOBRE
    -----
    A função do método é verificar as expressões quanto:
        - ao escopo
        - retorno de tipo
        - Casos especiais de atenção:
            * let [declaração de novas variáveis] : adicionar novas variáveis como formals no método
            * assignment: verificar se a variável já existe e verificar se o tipo corresponde ao tipo a ser retornado
    PARÂMETRO
    ---------
    - expr: objeto do tipo Node que contém estrutura a ser verificada

    RETORNO
    -------
    - A função retorna um TIPO do resultado da expressão (string ou node?)
    """
    if(expr.getLabel() == tag.ISVOID): 
        for e in expr.children:  rType = exprAnalyzer(e)
        
        if(analyzer.lastValue == 'void'): analyzer.lastValue = 'true'
        
        else:  analyzer.lastValue = 'false'
        
        return 'Bool'
    
    elif(expr.getLabel() == tag.SELF_TYPE): 
        analyzer.setSelf_type = True
        return analyzer.getTypes()[analyzer.classScope].name
    
    elif(expr.getLabel() in [tag.BOOL, tag.INTEGER, tag.STRING] or expr.getLabel() == tag.NEW):
        analyzer.lastTypeReturned = expr._type
        if(expr.label == tag.STRING): analyzer.stringValueFunctionCall = analyzer.lastValue 
        if(expr.getLabel() == tag.NEW):
            analyzer.lastValue = expr.name
            return analyzer.lastTypeReturned
        else: 
            if(not analyzer.hasClass(expr._type, expr.getLine())): analyzer.addError(f"<{e.line}> '{expr.name}' is not defined.")
            else:
                analyzer.lastTypeReturned   = expr._type
                analyzer.lastValue          = expr.name

        if(expr.children!=[]):
            for e in expr.children: rType = exprAnalyzer(e)
        
        return expr._type
    else:
        if(analyzer.inLet and analyzer.wasIf):
            analyzer.setVarLet(expr.name,expr.line)
            analyzer.wasInIf()
        else:
            rType = eval(f"{str(expr.getLabel().name)}(expr)") 

            return rType 

def methodAnalyzer(method:Node):
    """
    Retorna um TIPO (string ou node?)
    """
    if(method.children == []):
        
        pass
    else:
        for methodExpr in method.children:  
            if(methodExpr.label == tag.LET or methodExpr.label == tag.CASE or methodExpr.label==tag.IF or methodExpr.label==tag.WHILE):
                eval(f"{str(methodExpr.getLabel().name)}(methodExpr)") 
            else:
                if(methodExpr.children == [] or len(methodExpr.children) == 1):
                    exprAnalyzer(methodExpr)
                else:
                    for expr in methodExpr.children: 
                        exprAnalyzer(expr) 
   
    if( method._type != analyzer.lastTypeReturned and method._type!="Object"): analyzer.addError(f"<{method.getLine()}> '{method.getName()}' returns type '{method._type}', but the last expression returned type '{analyzer.lastTypeReturned}'")
def attributeAnalyzer(attribute: Node):
    '''
    SOBRE
    -----
    Função base de análise de tipo para uma tributo.
    Dado um atributo, verifica-se se o tipo retornado corresponde ao tipo declarado.

    PARÂMETRO
    ---------
    - attribute: objeto do tipo Node, atributo a ser analisado
    '''

    
    if(attribute.children == []): 
        pass
    else: 
        for c in attribute.children:
            exprAnalyzer(c)  
            
        if (not analyzer.compatibleType(attribute._type, analyzer.lastTypeReturned)): 
            analyzer.addError(f"<{attribute.line}> '{attribute.getName()}' is defined as '{attribute._type}'. '{attribute._type}' is not assignable to '{analyzer.lastTypeReturned}'.") 
        else:
            
            analyzer.getTypes()[analyzer.classScope].attributes[analyzer.attributeScope].setValue(analyzer.lastValue)

def preAnalyzer():
    '''
    SOBRE
    -----
    A função realiza uma pré análise de tipos utilizando a estrutura de lista de tipos montada na análise sintática
    '''
    if(analyzer.hasClass("Main")):  analyzer.hasMethod("Main", "main")

    for t in analyzer.getTypes():
        analyzer.checkType(t)
        for m in t.methods: analyzer.checkMethod(m)
        for a in t.attributes: analyzer.checkAttribute(a)
    
def main(root):
    analyzer.self_type.insert(0, root[0].name)
    objClass = analyzer.hasClass(root[0].name)
    analyzer.classId = objClass.scopeId
    if(objClass.parent != ''):
        try:
            analyzer.classInheritedId =  analyzer.hasClass(objClass.parent).scopeId
        except:
            analyzer.classInheritedId = -1

    indexMethod = 0
    indexAttribute = 0
    for feauture in root[0].children: 
        if(feauture.getLabel() == tag.METHOD):
            if(feauture.name!='main'): return
            analyzer.setScope(0+5, indexMethod, -1)
            methodAnalyzer(feauture)
            indexMethod +=1
        elif(feauture.getLabel() == tag.ATTRIBUTE): 
            analyzer.setScope(0+5, -1,indexAttribute)
            attributeAnalyzer(feauture)
            indexAttribute +=1
        analyzer.resetFeauture()
   

def sem(typeList, synTree):
    global analyzer
    analyzer = Analyzer(typeList)
    analyzer.treeCopy = synTree
    preAnalyzer()
    main(synTree)

    with open("ERROSEMANTICO.txt", "w") as file:
        for e in analyzer.errs:
            file.write(e+"\n")