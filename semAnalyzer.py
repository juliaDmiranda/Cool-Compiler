import os
from synTree import Node, tag
import TYPE_LIST as TL

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
    typeListAnalyzer:TL.Creator
    errs = [] # lista de erros semânticos encontrados ao longo da anáalise

    ''' Para análise de escopo'''
    classScope          = 0  # guarda índice da classe ondee está ocorrendo a análise
    classInheritedScope = -1 # guarda índice da classe herdada
    methodScope         = 0  # guarda índice do método onde está ocorrendo a análise
    attributeScope      = 0 # guarda index do atributo para, caso ocorra uma atribuição, esse valor possa ser alterado
    inLet               = False
    scope               = [] 
    scopeLet            = [] # Guarda variáveis de escopo: à princípio do LET
    '''
     [(name, type, value)]
    '''
    ''' outros '''
    computeResult    = False   # se estiver eme alguma estrutura que depende do resultaod de um cálculo (ex: if)
    lastValue           = 0  # resultaod anterior de alguma expressão
    lastTypeReturned = '' # Contém lista de tipos gerada na análise sintática
    
    ''' Talvez saia'''
    resultOfExpression  = None # resultado da expressão calculada
    setSelf_type = False 
    blockComparation = False # Quando dá algum erro de retorno

    def __init__(self, typeList:TL.Creator):
        self.typeListAnalyzer = typeList

        ''' 
    FUNÇÕES AUXILIARES GERAIS
    '''
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

        # pra quÊ isso:  and className != "-"
        if(not obj and className != "-"):
            self.addError(f"<{line}>{msg}Class '{className}' is not defined.")
            return obj

        return obj[0]
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
            self.addError(f"<{line}> Method '{methodName}' is not defined.")
            return obj

        return obj[0]
    def compatibleType(self,_type, rType): # antes: rType
        '''
        SOBRE
        -----
        Função que verifica se dois tipos são iguais. A função é útil para verificar se um valor retornado é do mesmo tipo da estrutura
        '''
        if(_type == rType or _type == '-'): # antes: rType # a exceção '-' é para o if, já que não sei o que retornará
            return True
        else:
            return False
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
    def addError(self, msg):
        '''
        SOBRE
        -----
        Função que adiciona nova mensagem de erro  
        '''
        self.errs.append(msg)

    '''
    REFERENTE AO ESCOPO : ACHO QUE NÃO VOU USAR
    '''
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
    def setScope(self, classI, methodI = -1, attributeI = -1): # basicamente o id do pai
        # seta índice da classe atual
        self.classScope = classI
        
        if (self.getTypes()[classI].parent != ""): # (se herda de alguma classe) seta índice do parente da classe atual
            self.classInheritedScope =  [self.typeListAnalyzer.typeList.index(c) for c in self.typeListAnalyzer.typeList if c.name == self.typeListAnalyzer.typeList[classI].parent][0]
        # seta índice do método
        self.methodScope = methodI
        self.attributeScope = attributeI
    def showScope(self, nodeName):
        print("Node",nodeName)
        for i in self.scope:
            print("i>>> ",i)
 
    ''' 
    FUNÇÕES AUXILIARES PARA O LET
    '''
    def popLet(self):
        if(self.scopeLet != []):
            self.scopeLet.pop()
    def setLet(self):
        if(self.inLet == False):
            self.inLet = True
        elif(self.inLet == True):
            # confere antes se o expr let de onde estou está dentro de outro let
            if(self.scopeLet==[]):
                self.inLet = False
    def setScopeLet(self, letOpts):
        self.scopeLet.append(letOpts)
    def getVarLet(self, name):
        # procura variável e retorna o tipo e o valor

        for letScops in self.scopeLet[::-1]: # procura a partir do escopo atual
            r = [var for var in letScops if name == var[0]]
            if(r!=[]):
                return r[0][1], r[0][2]

        return 'Object', 'void'
    def setVarLet(self, name, line):
        # ,newVallue é o lastValue
        # procura por nome (excopo de trás para frente)
        
        for i, letScopes in enumerate(self.scopeLet[::-1]): # procura a partir do escopo atual
            r = [var for var in letScopes if name == var[0]] # não tatrou para caso seja let dentro de let
            if(r!=[]):
                toIndex = letScopes.index(r[0])
                self.scopeLet[i][toIndex][2] = analyzer.lastValue
                if (not analyzer.compatibleType(self.scopeLet[i][toIndex][1], analyzer.lastTypeReturned)): # confere se o tipo corresponde ao da variável local do let
                    analyzer.addError(f"<<{r}>><{line}> '{name}' is defined as '{self.scopeLet[i][toIndex][1]}'. '{self.scopeLet[i][toIndex][2]}' is not assignable to '{analyzer.lastTypeReturned}'.") 
        # muda o valor
    ''' 
    FUNÇÕES AUXILIARES PARA EXECUTAR INSTRUÇÕES EM COOL
    '''
    def getResult(self, op, x, y = 0): # ÚTIL PARA IF
        if(self.computeResult):
            x = True if x == "true" else False if x == "false" else x
            y = True if y == "true" else False if y == "false" else y
            if(op == "="): op = "=="
            elif(op == "/"): op = "//"
            if(op == "not"):
                self.lastValue =  not x
            elif(op=="~"):
                self.lastValue =  findComplement(int(x))
            else:
                self.lastValue = eval(f"{x} {op} {y}")

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
    

# Implementadas
def MULTEXPR    (e:Node):

    for expr in e.children:
        if((expr._type in ['Bool', 'Int', 'String'] or expr.getLabel() == tag.NEW) and expr.getLabel() != tag.BOOLOP and expr.getLabel() != tag.INTOP):
            analyzer.lastTypeReturned = expr._type # antes: rType
            if(expr._type in ['Bool', 'Int', 'String']):
                analyzer.lastValue = expr.name
        else:
            # Caso não seja nenhum terminal, é possível que seja alguma expressão sem recursão
            analyzer.lastTypeReturned = eval(str(expr.getLabel().name)+"(expr)")   # antes: rType
            # analyzer.lastTypeReturned = exprAnalyzer(expr) # Funciona com essa chamda também # antes: rType

    return analyzer.lastTypeReturned # antes: rType
def IF          (e:Node):
    '''
    Só faz verificação das expressões
    '''
    rType = [0,0,0] # tipos retornados de cada expressão da estrutura if (3)
    rValue = [0,0,0] # valor retornado em cada expressão
    for i, c in enumerate(e.children):
        rType[i] = exprAnalyzer(c) 
        rValue[i] = analyzer.lastValue

        # verificar se tipo retornado corresponde ao tipo do atributo
        if (i == 0 and not analyzer.compatibleType(e._type, analyzer.lastTypeReturned)): # depois por mensagem já no método de uma vez, só muda a mensagem de erro # antes: rType
            analyzer.addError(f"<{e.line}> The <expr> {i+1} returned {rType[i]} but Bool was expected.") # antes: rType

    if(rValue[0] == True or rValue[0] == "true"):
        print(f"<{e.line}> If returned {str((rValue[1])).lower() if rValue[1] in [True,False] else rValue[1]}")
        analyzer.lastValue = str((rValue[1])).lower() if rValue[1] in [True,False] else rValue[1]
        return rType[1]
    
    else:
        print(f"<{e.line}> If returned {str(rValue[2]).lower() if rValue[2] in [True,False] else rValue[2]}")
        analyzer.lastValue = str(rValue[2]).lower() if rValue[2] in [True,False] else rValue[2]
        return rType[2] 
def WHILE       (e:Node):
    '''
    Só faz verificação das expressões
    '''
    rType = [0,0] # tipos retornados de cada expressão da estrutura while (2)
    rValue = [0,0] # valor retornado em cada expressão
    for i, c in enumerate(e.children):
        rType[i] = exprAnalyzer(c) 
        rValue[i] = analyzer.lastValue

    # verificar se tipo retornado corresponde ao tipo do atributo
    if (not analyzer.compatibleType(e._type, rType[0])): # depois por mensagem já no método de uma vez, só muda a mensagem de erro # antes: rType
        analyzer.addError(f"<{e.line}> First while branch returned {rType[0]} but Bool was expected.") # antes: rType
    
    return rType[1]
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
    if(e.getName()!="not" and e.getName()!="="): # not não tem expressão anterior ao keyword e = avalia a segunda expressão
        # Verifica tipo de expr da esquerda
        if(not analyzer.compatibleType('Int', analyzer.lastTypeReturned)):
            analyzer.addError(f"<{e.line}> The expression (<expr>{e.name}) was supposed to return Int, not {analyzer.lastTypeReturned}.")
        else:
            analyzer.computeResult = True
            x = analyzer.lastValue 
    
    analyzer.computeResult = True # Calcular de fato o resultado
    x, leftType = analyzer.lastValue, analyzer.lastTypeReturned 
    '''
    Guarda o valor e o tipo retornado da expressão da esquerda
    Isso para saber se o valor da expressão da direita vai ser compatível com o anterior
    '''

    # Verificar tipo de expr da direita
    for expr in e.children: # verifica cada expressão
        rType  = exprAnalyzer(expr) # antes: rType
    if(e.name == "not"): # not não tem expressão antes do not
        comp = 'Bool'
        leftType = 'Bool' # evitar que o anterior seja de outra expressão que tenha retornado Int para não tentar ocnverter bool em int, por exemplo
        x = analyzer.lastValue
    else:
        comp = leftType
    
    if(not analyzer.compatibleType(comp, rType)): # antes: rType
        analyzer.addError(f"<{e.line}> The expression ({e.name}<expr>) was supposed to return {comp}, not {rType}.")
    else: # fazer cálculo para saber o valor booleano retornado
        comp = int if leftType=="Int" else str
        analyzer.getResult(e.getName(), (comp)(x), (comp)(analyzer.lastValue))

    analyzer.lastTypeReturned = "Bool"
    return "Bool" # antes: rType
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
        # Verifica tipo de expr da esquerda
        if(not analyzer.compatibleType('Int', analyzer.lastTypeReturned)):
            analyzer.addError(f"<{e.line}> The expression (<expr>{e.name}) was supposed to return Int, not {analyzer.lastTypeReturned}.")
        else:
                analyzer.computeResult = True
                x = analyzer.lastValue 
    analyzer.computeResult = True # Calcular de fato o resultado
    x, leftType = analyzer.lastValue, analyzer.lastTypeReturned 
    '''
    Guarda o valor e o tipo retornado da expressão da esquerda
    Isso para saber se o valor da expressão da direita vai ser compatível com o anterior
    '''

    # Verificar tipo de expr da direita
    for expr in e.children: # verifica cada expressão
        rType  = exprAnalyzer(expr) # antes: rType
    
    if(not analyzer.compatibleType('Int', rType)): # antes: rType
        analyzer.addError(f"<{e.line}> The expression ({e.name}<expr>) was supposed to return Int, not {rType}.")
        # analyzer.blockComparation = True
    else: # fazer cálculo para saber o valor booleano retornado
        analyzer.getResult(e.getName(), (int)(x), (int)(analyzer.lastValue))

    analyzer.lastTypeReturned = rType
    return rType # antes: rType
def ASSIGNMENT  (e:Node):
    exprAnalyzer(e.children[0]) # antes: rType
    ID(e, True)

# Faltando
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
def LET         (e:Node):
    letVars = [] # TIPO [(name, type, value)] Fazer isso
    analyzer.setLet()
    # AGORA a Estrutura depois do in, isto é, quando a tag não for LETOPT
    for l in e.children:
        if(l.label==tag.MULTEXPR):
            if(not letVars): # (evitar que faça isso lá embaixo) Para não sobrescrever letVars e escopo (pois se for True, as variáveis já foram inclusas e agora está senda analisada a estrutura do in)
                
                rType = exprAnalyzer(l)
            else: 
                # (no analyzer) setar variáveis do escopo do let (adiciona em uma pilha, pois pode ter let dentro de let?)
                analyzer.setScopeLet(letVars)
                letVars = []
                rType = exprAnalyzer(l)
        else:
            # (localmente)setar variáveis do escopo do let (adiciona em uma pilha, pois pode ter let dentro de let?)
            if(l.children != []):
                ID(l)
                # # Lembra de verificar o tipo
                if (not analyzer.compatibleType(l._type, analyzer.lastTypeReturned)): # confere se o tipo corresponde ao da variável local do let
                    analyzer.addError(f"<{l.line}> '{l.name}' is defined as '{l._type}'. '{l._type}' is not assignable to '{analyzer.lastTypeReturned}'.") 
                if(True): # se o tipo for compatível
                    letVars.append([l.name, l._type, analyzer.lastValue])
            else:
                letVars.append([l.name, l._type, analyzer.lastValue])
            
    
    # quando sair, retira as variáveis do escopo do let atual
    analyzer.popLet()
    analyzer.setLet()

    return analyzer.lastTypeReturned
def PARENTHESIS (e:Node):
    pass


def ID(e:Node, ass = False):
    if(analyzer.inLet ): # se for Let, consideraremos as variáveiss de dentro do escopo dessa estrutura
        if(e.label==tag.ASSIGNMENT or e.label==tag.LETOPT): # se for para atualizar valores - formato de armazenamento -> [(name, type, value)]
            # TIRAR gera loop infinito, não precisa, no método do ASSIGNMENT já retornei o último tipo #r = exprAnalyzer(e)
            # atualizar o valor
            rType = exprAnalyzer(e.children[0])
            analyzer.setVarLet(e.name, e.line)
            
            # seta último tipo e seta último valor -> ACHO QUE NÃO PRECISA

        else: # se for só para retorna o valor
            # seta último tipo e seta último valor
            analyzer.lastTypeReturned, analyzer.lastValue = analyzer.getVarLet(e.name)
            if(e.children != []):
                rType = exprAnalyzer(e.children[0])

            # retorna últipo tipo
            return analyzer.lastTypeReturned
    else:
        # Proocura nos formals do método atual
        classInfo = analyzer.getTypes()[analyzer.classScope]
        if(analyzer.methodScope == -1 or classInfo.methods == []):
            IDefined = False
        else: # vê se está em algum parâmetro passado
            IDefined = False
            formals =  classInfo.methods[analyzer.methodScope].formals
            if(formals != []):
                IDefined = [formal for formal in formals if formal[0]==e.name]
                IDefined = IDefined if IDefined==[] else IDefined[0]

                if(IDefined):
                    if(ass ): # atribuição de valor de formal
                        if (not analyzer.compatibleType(IDefined[1], analyzer.lastTypeReturned)): # confere se o tipo corresponde ao do formal
                            analyzer.addError(f"<{e.line}> '{e.name}' is defined as '{IDefined[1]}'. '{IDefined[1]}' is not assignable to '{analyzer.lastTypeReturned}'.") # antes: rType
                        else:
                            analyzer.getTypes()[analyzer.classScope].methods[analyzer.methodScope].setValue(analyzer.lastValue, IDefined)
                    else:
                        analyzer.lastValue = analyzer.getTypes()[analyzer.classScope].methods[analyzer.methodScope].getValue(IDefined)

        if not IDefined: # Procura nos atributos classe atual
            IDefined  = [a for a in classInfo.attributes if a.name == e.name]
            IDefined = IDefined if IDefined==[] else IDefined[0]
            
            if not IDefined: # Procura nos atributos da classe herdada / dedsconsiderando métodos de mesmo nome com o mesmo parâmetro
                IDefined  = [a for a in analyzer.getTypes()[analyzer.classInheritedScope].attributes if a.name == e.name]
                
                IDefined = IDefined if IDefined==[] else IDefined[0]
            if(ass): # atribuição a um atributo
                if (not analyzer.compatibleType(IDefined._type, analyzer.lastTypeReturned)):
                    analyzer.addError(f"<{e.line}> '{e.name}' is defined as '{IDefined._type}'. '{IDefined._type}' is not assignable to '{analyzer.lastTypeReturned}'.") # antes: rType
                else:
                    if(e.children != 0): # casos ar < 2 + 1
                        for c in e.children:
                            exprAnalyzer(c)
                    analyzer.getTypes()[analyzer.classScope].attributes[classInfo.attributes.index(IDefined)].setValue(analyzer.lastValue)
            else:
                analyzer.lastValue = analyzer.getTypes()[analyzer.classScope].attributes[analyzer.attributeScope].getValue()

        if(not IDefined): # se não encontrado: mensagem de erro
            analyzer.addError(f"<{e.line}> '{e.name}' is not defined in this scope")
        else: # se achado: seta como últimos Tipo e valor encontrados
            # retorna esses valores
            if(isinstance(IDefined, tuple)):
                analyzer.lastTypeReturned = IDefined[1]
            else:
                analyzer.lastTypeReturned = IDefined._type
                analyzer.lastValue = IDefined.value 
            if(e.children != 0): # casos ar < 2 + 1
                for c in e.children:
                    exprAnalyzer(c)
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
    if(expr.getLabel() == tag.ISVOID): # N'ao sei o que fazer 
        for e in expr.children:
            rType = exprAnalyzer(e)

        return expr._type
   
    elif(expr.getLabel() in [tag.BOOL, tag.INTEGER, tag.STRING] or expr.getLabel() == tag.NEW):
        analyzer.lastTypeReturned = expr._type
        if(not expr.getLabel() == tag.NEW): # dá atençaõe special ao new que mexerá com tipos
            analyzer.lastValue = expr.name
        else: # checagem do tipo
            if(not analyzer.hasClass(expr._type, expr.getLine())):
                analyzer.addError(f"<{e.line}> '{expr.name}' is not defined.") # antes: rType
            else:
                analyzer.lastTypeReturned   = expr._type
                analyzer.lastValue          = expr._type


        if(expr.children!=[]):
            for e in expr.children:
                rType = exprAnalyzer(e)
        return expr._type # retorna tipo # antes: rType

    else:
        rType = eval(f"{str(expr.getLabel().name)}(expr)") # pega nome da tag e faz xhamada da função específica # antes: rType
        analyzer.lastTypeReturned = rType
        return rType # retorna tipo # antes: rType

def exprMethodAnalyzer(methodExpr:Node):
    """
    Retorna um TIPO (string ou node?)
    """

    rType = "None"  # antes: rType
    if(methodExpr.label == tag.LET or methodExpr.label == tag.CASE):
        rType = eval(f"{str(methodExpr.getLabel().name)}(methodExpr)") # pega nome da tag e faz xhamada da função específica # antes: rType
    else:
        for expr in methodExpr.children: # verifica cada expressão
            rType  = exprAnalyzer(expr) # antes: rType
        
    analyzer.lastTypeReturned = rType

    return rType  # antes: rType

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

    # verificar se atributo é inicializado
    if(attribute.children == []): # se não
        pass
    else: # se sim
        for c in attribute.children:
            rType = exprAnalyzer(c)  # antes: rType
            # verificar se tipo retornado corresponde ao tipo do atributo
        if (not analyzer.compatibleType(attribute._type, rType)): # depois por mensagem já no método de uma vez, só muda a mensagem de erro # antes: rType
            analyzer.addError(f"<{attribute.line}> '{attribute.getName()}' is defined as '{attribute._type}'. '{attribute._type}' is not assignable to '{rType}'.") # antes: rType
        else:
            # se o tipo for compatível, atribui o valor resultante a essa variável, atualizando na lsita de tipos
            analyzer.getTypes()[analyzer.classScope].attributes[analyzer.attributeScope].setValue(analyzer.lastValue)
        
def methodAnalyzer(method: Node):
    '''
    Análise de um método:
        - retorno deve corresponder ao tipo de retorno
    '''
    if(method.children == []):
        #Informar erro de valor Nulo não ser igual ao tipo a ser retornado
        pass
    else:
        rType = None # para guardar o retorno da última expressão
        for expr in method.children:
            rType = exprMethodAnalyzer(expr)   # guarda TIPO retornado

    # verificar se retorno da última expressão é o mesmo do declarado como retorno do método    
    if(method._type != rType):
        analyzer.addError(f"<{method.getLine()}> '{method.getName()}' returns type '{method._type}', but the last expression returned type '{rType}'")

def classAnalyzer(root:Node):
    '''
    SOBRE
    -----

    Função base para análise do programa. 
    Para cada classe declarada, verifica-se seus métodos e atributos 
    '''
    for j, _class in enumerate(root): # análise de cada classe do programa
        # Guardar cópia da estrutura da classe atual
        analyzer.push(analyzer.hasClass(_class.name))
        
        if(_class.inherit != "-"):
            # Guardar cópia da classe herdade (se tiver)
            analyzer.push(analyzer.hasClass(_class.inherit))
        indexMethod = 0
        indexAttribute = 0
        for i, feauture in enumerate(_class.children): # análise de feautures
            if(feauture.getLabel() == tag.METHOD):
                analyzer.setScope(j+5, indexMethod, -1)
                analyzer.push(analyzer.hasMethod(_class.name, feauture.name)) # guarda cópia do método 
                methodAnalyzer(feauture)
                indexMethod +=1
            elif(feauture.getLabel() == tag.ATTRIBUTE): 
                analyzer.setScope(j+5, -1,indexAttribute)
                attributeAnalyzer(feauture)
                indexAttribute +=1
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

    preAnalyzer()
    classAnalyzer(synTree)

    with open("ERROSEMANTICO.txt", "w") as file:
        for e in analyzer.errs:
            file.write(e+"\n")