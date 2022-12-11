from synTree import Node, tag
import TYPE_LIST as TL

global TYPE_LIST
TYPE_LIST = []

class Analyzer:
    setSelf_type = False 
    errs = []
    classScope          = 0 # guarda cópia da estrutura da classe
    classInheritedScope = 0 # guarda cópia da estrutura da classe
    currentlyScope      = 0
    typeListAnalyzer:TL.Creator
    '''Contém lista de tipos gerada na análise sintática'''
    scope             = [] 
    '''Guarda estrutura do escopo (???) '''

    def __init__(self, typeList:TL.Creator):
        self.typeListAnalyzer = typeList

    def pop(self):
        self.scope.pop(0)
    def push(self, obj):
        '''
        SOBRE
        -----
        Guarda na estrutura escopo alguma estrutura
        '''
        if not obj:
            pass
        else:
            self.scope.insert(0, obj)

    def addError(self, msg):
        self.errs.append(msg)

    def setScope(self, scope): # basicamente o id do pai
        self.currentlyScope = scope

    def getScope(self):
        return self.scope

    def getTypes(self):
        '''
        SOBRE
        -----
        Retorna a lista de tipos'''
        return self.typeListAnalyzer.typeList

    def checkType(self, obj:TL.Type): # informar se o tipo foi duplicado
        ''' 
        SOBRE
        -----
        Método para verificações sobre a lista de tipos mapeada durante a análise sintática.
        Quanto a classe, verifica-se:
            - Se uma calsse de mesmo nome já foi declarada
            - Se o tipo herdado pela classe existe
            - Se não "herda" do tipo Bool ou Int ou String
        '''
        if(obj.duplicated): # veritica se o tipo é repetido
            if(obj.name.lower() in ['object','io','int','string','bool'] and obj.line!="BC"):
                self.addError(f"<{obj.line}> Class '{obj.name}' is Cool's basic class. You are not allowed to redefine it.")
            else:
                self.addError(f"<{obj.line}> Class '{obj.name}' declared multiple times.")

        # se herda, verifica se a classe herdada existe
        if(obj.parent!=""):
            if(obj.parent.lower() in ['int','bool','string']):
                self.addError(f"<{obj.line}> It isn't allowed to inherit from '{obj.parent}' type.")
            if(not self.typeListAnalyzer.getClass(obj.parent)):
                self.addError(f"<{obj.line}> Class '{obj.name}' inherits class '{obj.parent}', but this class is not defined.")

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
        # Verifica de método foi declarado mais de uma vez
        if(obj.duplicated):
            self.addError(f"<{obj.line}> Method '{obj.name}' was already defined.")
            
        # Verifica se o tipo a ser retornado existe
        if(not self.typeListAnalyzer.getClass(obj._type)):
            if(obj._type != "SELF_TYPE"):
                self.addError(f"<{obj.line}> Method '{obj.name}' returns type '{obj._type}', but this type is not defined.")

        # verificação dos parâmetros
        for cont,f in enumerate(obj.formals):  

            # estrutura de um parâmetro --> (_nameOfFormal,_typeOfFormal)
            if(len([comp for comp in obj.formals if f[0] == comp[0]]) != 1): # verifica se parâmetro foi declarado mais de uma vez
                self.addError(f"<{obj.line}> Formal '{f[0]}'(formal {cont}) was already defined.")
            
            # verifica se tipo do parâmetro existe
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
        # Verifica de atributo foi declarado mais de uma vez
        if(obj.duplicated):
            self.addError(f"<{obj.line}> Attribute '{obj.name}' was already defined.")
            
        # Verifica se o tipo a ser retornado existe
        if(not self.typeListAnalyzer.getClass(obj._type)):
            if(obj._type != "SELF_TYPE"):
                self.addError(f"<{obj.line}> Attribute '{obj.name}' has type '{obj._type}', but this type is not defined.")

    def hasClass(self, className, line = "*", msg = " "):
        '''
        Dado o nome da classe, o método retorna se essa classe existe ou não no programa

        Se a classe existir é retornada
        Se não retorna False
        '''
        obj = self.typeListAnalyzer.getClass(className)
        # pra quÊ isso:  and className != "-"
        if(not obj and className != "-"):
            self.addError(f"<{line}>{msg}Class '{className}' is not defined.")
        return obj

    def hasMethod(self, className, methodName, line=-1):
        '''
        Dado o nome da classe e do método, o método retorna se esse método existe ou não na classe nomeada
        
        Se o método existir é retornado
        Se não retorna False
        '''
        obj = self.typeListAnalyzer.getClass(className)[0].getMethod(methodName)
        if(not obj):
            self.addError(f"<{line}> Method '{methodName}' is not defined.")
        return obj

    def compatibleType(self,_type, rType):
        if(_type == rType):
            return True
        else:
            return False

    def showScope(self, nodeName):
        print("Node",nodeName)
        for i in self.scope:
            print("i>>> ",i)

def ATTRIBUTE   (e:Node):
    pass
def ARGUMENT    (e:Node):
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

# criar tabela hash para cada função
def exprAnalyzer(expr: Node):
    """
    Retorna um TIPO (string ou node?)

    - Casos especiais de atenção:
            * let [declaração de novas variáveis] : adicionar novas variáveis como formals no método
            * assignment: verificar se a variável já existe e verificar se o tipo corresponde ao tipo a ser retornado
    """
    if(expr.children == []):
        if(expr._type in ['Bool', 'Int', 'String']):
            return expr._type
        elif(expr.getLabel() == tag.NEW):
            pass
        else:
            # Caso não seja nenhum terminal, é possível que seja alguma expressão sem recursão
            rType = eval(str(expr.getLabel().name)+"(expr)") 

        # se for ID
            # confere se ID existe (para isso vou precisar guardar o contexto (pilha?))
            # retorna tipo
        # confere se [e ]
        # retorna tipo (label)
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

    # verificar se atributo é inicializado
    if(attribute.children == []): # se não
        pass
    else: # se sim
        rType = exprAnalyzer(attribute.children[0]) 
        
        # verificar se tipo retornado corresponde ao tipo do atributo
        if (not analyzer.compatibleType(attribute._type, rType)):
            analyzer.addError(f"<{attribute.line}> '{attribute.getName()}' is defined as '{attribute._type}'. '{attribute._type}' can't be assigned with '{rType}'.")
        

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
    '''
    SOBRE
    -----

    Função base para análise do programa. 
    Para cada classe declarada, verifica-se seus métodos e atributos 
    '''
    for _class in root: # análise de cada classe do programa

        # Guardar cópia da estrutura da classe atual
        analyzer.push(analyzer.hasClass(_class.name))
        # Guardar cópia da classe herdade (se tiver)
        analyzer.push(analyzer.hasClass(_class.inherit))

        for feauture in _class.children: # análise de feautures
            if(feauture.getLabel() == tag.METHOD):
                analyzer.push(analyzer.hasMethod(_class.name, feauture.name)) # guarda cópia do método 
                methodAnalyzer(feauture)
            
            elif(feauture.getLabel() == tag.ATTRIBUTE): 
                attributeAnalyzer(feauture)

def preAnalyzer():
    '''
    SOBRE
    -----
    A função realiza uma pré análise de tipos utilizando a estrutura de lista de tipos montada na análise sintática
    '''
    if(analyzer.hasClass("Main")): # verificar se a Main foi declarada
        analyzer.hasMethod("Main", "main") # verificar se a função main() foi declarada

    # Para cada tipo
    for t in analyzer.getTypes():
        # Verificação dos tipos
        analyzer.checkType(t)
        # Verificação dos métodos
        for m in t.methods:
            analyzer.checkMethod(m)
        # Verificação dos atributos
        for a in t.attributes:
            analyzer.checkAttribute(a)

def main(typeList, synTree):
    global analyzer
    analyzer = Analyzer(typeList)

    preAnalyzer(typeList)
    classAnalyzer(synTree)

    with open("ERROSEMANTICO.txt", "w") as file:
        for e in analyzer.errs:
            file.write(e+"\n")