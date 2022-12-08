from synTree import Node, tag
import TYPE_LIST as TL

global TYPE_LIST
TYPE_LIST = []

class Analyser:
    setSelf_type = False 
    errs = []
    classScope          = 0 # guarda cópia da estrutura da classe
    classInheritedScope = 0 # guarda cópia da estrutura da classe
    currentlyScope      = 0
    typeListAnalyzer:TL.Creator
    scope             = None # no Id, por exemplo saber que foi um assgnment
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
            self.addError(f"<{obj.line}> Class '{obj.name}' declared multiple times ({qtd})")

        # se herda, verifica se a classe herdada existe
        if(obj.parent!=""):
            if(not self.hasClass(obj.parent)):
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


def ID(idNode):
    '''
    - verificar se o ID existe no escopo ou se existe em outra classe herdada
    - atualizar tipo retornado na árvore
    '''
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
        # se for ID
            # confere se ID existe (para isso vou precisar guardar o contexto (pilha?))
            # retorna tipo
        # confere se [e ]
        # retorna tipo (label)
        pass
    else:
        for e in expr:
            rType = eval(str(e.getLabel().name)+"(e)")

            rType = exprAnalyzer(e)
        return rType # retorna tipo

def exprMethodAnalyzer(methodExpr):
    """
    Retorna um TIPO (string ou node?)
    """

    rType = "None" 

    for expr in methodExpr: # verifica cada expressão
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
    # verificar se tipo de retorno existe

    # se tiver parâmetro
        # verificar se tipo do parâmetro existe

    if(method.children == []):
        #Informar erro de valor Nulo não ser igual ao tipo a ser retornado
        pass
    else:
        lastReturnedType = None # para guardar o retorno da última expressão
        for expr in method.children:

            lastReturnedType = exprMethodAnalyzer(expr)   # guarda TIPO retornado

    # verificar se retorno da última expressão é o mesmo do declarado como retorno do método    

def classAnalyzer(root):
    for _class in root: # análise de cada classe do programa

        # Guardar cópia da estrutura da classe
        # Guardar cópia da classe herdade (se tiver)
    
        # Atualizar escopo (id)
        for feauture in _class.children: # análise de feautures
            if(feauture.getLabel() == tag.METHOD): 
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
    analyzer.typeListAnalyzer.printTypes()
    preAnalyzer(typeList)
    with open("ERROSEMANTICO.txt", "w") as file:
        for e in analyzer.errs:
            file.write(e+"\n")