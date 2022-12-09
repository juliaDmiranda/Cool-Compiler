from synTree import Node, tag
import TYPE_LIST as TL

global TYPE_LIST
TYPE_LIST = []

def ATTRIBUTE   (e:Node):
    pass
def BRACKETS    (e:Node):
    pass
def BOOL        (e:Node):
    pass
def CLASS       (e:Node):
    pass
def CASE        (e:Node):
    pass
def CASEOPT     (e:Node):
    pass
def DOT         (e:Node):
    pass
def EXPRL       (e:Node):
    pass
def FUNCALL     (e:Node):
    pass
def FUNCALLID   (e:Node):
    pass
def FORMALS     (e:Node):
    pass
def IF          (e:Node):
    pass
def ID          (e:Node):
    '''
    - verificar se o ID existe no escopo ou se existe em outra classe herdada
    - atualizar tipo retornado na árvore
    '''
    pass
def ISVOID      (e:Node):
    pass
def INTEGER     (e:Node):
    pass
def LET         (e:Node):
    pass
def LETOPT      (e:Node):
    pass
def METHOD      (e:Node):
    pass
def MULTEXPR    (e:Node):
    pass
def NEW         (e:Node):
    pass
def NOT         (e:Node):
    pass
def OPE         (e:Node):
    pass
def PARENTHESIS (e:Node):
    pass
def ASSIGNMENT  (e:Node):
    pass
def STRING      (e:Node):
    pass
def TIDE        (e:Node):
    pass
def WHILE       (e:Node):
    pass

class Analyser:
    setSelf_type = False 
    errs = []
    classScope          = 0 # guarda cópia da estrutura da classe
    classInheritedScope = 0 # guarda cópia da estrutura da classe
    currentlyScope      = 0
    typeListAnalyzer:TL.Creator
    scope             = [] # no Id, por exemplo saber que foi um assgnment
    '''
    Se o contexto for um método guardar 
    - adicionar id no método
    '''
    def __init__(self, typeList:TL.Creator):
        self.typeListAnalyzer = typeList

    def addError(self, msg):
        self.errs.append(msg)
    def setScope(self, scope): # basicamente o id do pai
        self.currentlyScope = scope
    def getScope(self):
        return self.currentlyScope
    def setContext(self, scope):
        self.scope = scope
    def getContext(self):
        return self.context

    def getTypes(self): # retorna a lista de tipos
        return self.typeListAnalyzer.typeList

    def checkType(self, obj:TL.Type, _id): # informar se o tipo foi duplicado
        '''
        Verificações sobre uma classe:
            - Foi declarada mais de uma vez
            - Herda de uma classe inexistente
        '''
        obj, qtd = self.typeListAnalyzer.getClass(obj.name, _id)

        if(qtd > 1): # veritica se o tipo é repetido
            if(obj.name.lower() in ['object','io','int','string','bool'] and obj.line!="BC"):
                self.addError(f"<{obj.line}> Class '{obj.name}' is Cool's basic class. You are not allowed to redefine it({qtd})")
            else:
                self.addError(f"<{obj.line}> Class '{obj.name}' declared multiple times ({qtd})")

        # se herda, verifica se a classe herdada existe
        if(obj.parent!=""):
            if(obj.parent.lower() in ['int','bool','string']):
                self.addError(f"<{obj.line}> Class '{obj.parent}' is Cool's basic class. You are not allowed to inherit from it")
            if(not self.hasClass(obj.parent,"justCheck")):
                self.addError(f"<{obj.line}> Class '{obj.name}' inherits class '{obj.parent}', but this class is not defined")

    def checkMethod(self, obj:TL.Method, _type, _id): # informar se o tipo foi duplicado
        '''
        Verificação sobre um método
            - Se foi declarado mais de uma vez
            - Se o tipo a ser retornado existe
            - Parâmetros
                - declarado mais de uma vez
                - tipo do parâmetro é inexistente
        '''
        # Verifica de método foi declarado mais de uma vez
        obj, qtd = self.typeListAnalyzer.getMethod(obj.name, _type, _id)
        if(qtd > 1):
            self.addError(f"<{obj.line}> Method '{obj.name}' was defined multiple times({qtd})")
            
        # Verifica se o tipo a ser retornado existe
        if(not self.hasClass(obj._type,"justCheck")):
            if(obj._type != "SELF_TYPE"):
                self.addError(f"<{obj.line}> Method '{obj.name}' returns type '{obj._type}', but this type is not defined.")

        cont = 1
        # verificação dos parâmetros
        for f in obj.formals:  
            # estrutura de um parâmetro --> (_nameOfFormal,_typeOfFormal)
            if(len([comp for comp in obj.formals if f == comp]) != 1): # verifica se parâmetro foi declarado mais de uma vez
                self.addError(f"<{obj.line}> Formal '{f[0]}'(formal {cont}) was defined multiple times.")
            
            # verifica se tipo do parâmetro é inexistente
            if(not self.hasClass(f[1], "justCheck")):
                if(obj._type != "SELF_TYPE"):
                    self.addError(f"<{obj.line}> Formal '{f[0]}'(formal {cont}) has type '{f[1]}', but this type is not defined.")
            cont+=1

    def checkAttribute(self, obj:TL.Attribute, _type:TL.Type, _id):
        '''
        Verificação sobre um atributo
            - Se foi declarado mais de uma vez
            - Se o tipo existe
        '''
        # Verifica de atributo foi declarado mais de uma vez
        obj, qtd = self.typeListAnalyzer.getAttribute(_type.name,obj.name, _type, _id)
        if(qtd > 1):
            self.addError(f"<{obj.line}> Attribute '{obj.name}' was defined multiple times({qtd})")
            
        # Verifica se o tipo a ser retornado existe
        if(not self.hasClass(obj._type, "justCheck")):
            if(obj._type != "SELF_TYPE"):
                self.addError(f"<{obj.line}> Attribute '{obj.name}' has type '{obj._type}', but this type is not defined.")


    def hasClass(self, className, line = "*"):
        '''
        Dado o nome da classe, o método retorna se essa classe existe ou não no programa

        Se a classe existir é retornada
        Se não retorna False
        '''
        obj, _ = self.typeListAnalyzer.getClass(className)
        if(not obj and line != "justCheck"):
            self.addError(f"<{line}> Class '{className}' is not defined")
        return obj

    def hasMethod(self, className, methodName):
        '''
        Dado o nome da classe e do método, o método retorna se esse método existe ou não na classe nomeada
        
        Se o método existir é retornado
        Se não retorna False
        '''
        _, obj = self.typeListAnalyzer.getClass(className)
        if(not obj):
            self.addError(f"<{obj.line}> Method '{className}' is not defined")
        return obj


# criar tabela hash para cada função
def exprAnalyzer(expr: Node):
    """
    Retorna um TIPO (string ou node?)

    - Casos especiais de atenção:
            * let [declaração de novas variáveis] : adicionar novas variáveis como formals no método
            * assignment: verificar se a variável já existe e verificar se o tipo corresponde ao tipo a ser retornado
    """
    if(expr.children == []):
        # se for ID
            # confere se ID existe (para isso vou precisar guardar o contexto (pilha?))
            # retorna tipo
        # confere se [e ]
        # retorna tipo (label)
        pass
    else:
        for e in expr.children:
            rType = eval(str(e.getLabel().name)+"(e)")

    return rType # retorna tipo

def exprMethodAnalyzer(methodExpr:Node):
    """
    Retorna um TIPO (string ou node?)
    """

    rType = "None" 

    for expr in methodExpr.children: # verifica cada expressão
        rType  = exprAnalyzer(expr)
    return rType 

def attributeAnalyzer(attribute: Node):
    '''
    Análise de um atributo:
        - se foi preenchido, verificar se foi com o mesmo tipo com o cal foi
    '''
    # verificar se TIPO do atributo existe

    # verificar se atributo é inicializado
    if(attribute.children == []): # se não
        pass
    else: # se sim
        rType = exprAnalyzer(attribute.children[0]) 
       # verificar se tipo retornado corresponde ao tipo do atributo

def methodAnalyzer(method: Node):
    '''
    Análise de um método:
        - retorno deve corresponder ao tipo de retorno
    '''
    if(method.children == []):
        #Informar erro de valor Nulo não ser igual ao tipo a ser retornado
        pass
    else:
        lastReturnedType = None # para guardar o retorno da última expressão
        for expr in method.children:
            lastReturnedType = exprMethodAnalyzer(expr)   # guarda TIPO retornado

    lastReturnedType = "Int"
    # verificar se retorno da última expressão é o mesmo do declarado como retorno do método    
    if(method._type != lastReturnedType):
        analyzer.addError(f"<{method.getLine()}> '{method.getName()}' returns type '{method._type}', but the last expression returned type '{lastReturnedType}'")

        

def classAnalyzer(root:Node):
    for _class in root: # análise de cada classe do programa

        # Guardar cópia da estrutura da classe
        # Guardar cópia da classe herdade (se tiver)
        analyzer.scope.append(analyzer.hasClass(_class.name))
        analyzer.scope.append(analyzer.hasClass(_class.father))
    
        for feauture in _class.children: # análise de feautures
            if(feauture.getLabel() == tag.METHOD):
                analyzer.scope.append(analyzer.hasMethod(_class.name, feauture.name)) # guarda cópia do método 
                methodAnalyzer(feauture)
            
            elif(feauture.getLabel() == tag.ATTRIBUTE): 
                attributeAnalyzer(feauture)

def preAnalyzer(typeList):
    analyzer.hasClass("Main") # verificar se a Main foi declarada
    analyzer.hasMethod("Main", "main") # verificar se a função main() foi declarada

    # Para cada tipo
    for t in analyzer.getTypes():
        # Verificação dos tipos
        analyzer.checkType(t,t.scopeId)
        # Verificação dos métodos
        for m in t.methods:
            analyzer.checkMethod(m, t, m.scopeId)
        # Verificação dos atributos
        for a in t.attributes:
            analyzer.checkAttribute(a, t, a.scopeId)

def main(typeList, synTree):
    global analyzer
    analyzer = Analyser(typeList)

    preAnalyzer(typeList)
    # classAnalyzer(synTree)

    with open("ERROSEMANTICO.txt", "w") as file:
        for e in analyzer.errs:
            file.write(e+"\n")