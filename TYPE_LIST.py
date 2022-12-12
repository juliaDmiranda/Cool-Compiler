import os 
class Feature():
    """
    Classe responsável por armazenar informações de uma feature


    ISSUE: mudar o nome Feature para um nome mais genêrico para servir para referenciar formal
    """
    name = ""
    _type = None
    line = 0
    duplicated  = False # informa se a feauture já foi definido antes e está repetido

    def __init__(self, _name, _type) -> None:
        self.setName(_name)
        self.setType(_type)

    def setName(self, _name):
        self.name = _name

    def setType(self, _type):
        self._type = _type
    
    def compType(self, _type):
        """
        Função para ser utilizada na análise semântica quando souber o valor
        retornado ou atribuído a um atributo da classe a qual pertence.
        A função compara o tipo retornado/atribuído com o tipo que o método 
        deve retornar ou o tipo designado ao atributo em sua declaração.
        """
        if(self._type == _type): return True
        else: return False

    def __str__(self) -> str:
        return f" {self.name}-{self._type}\n"


class Method(Feature):
    """
    Classe responsável por armazenar informações de um método
    """
    # name, _type = "","" 
    formals     = []
    qtdFormal   = 0
    scopeId     = 0
    node        = None
    def __init__(self, _name, _Type, _formals,line, _id, duplicated=False):
        super().__init__(_name, _Type)
        self.duplicated = duplicated
        self.scopeId = _id
        self.formals = _formals
        self.qtdFormal = len(self.formals)
        self.line = line

    def show(self):
        print(f"(M) {self.name}-{self._type}")
        if(self.formals != []):
            print(str(self.formals))


    def toTree(self, noden):
        self.node = noden


class Attribute(Feature):
    """
    Função para armazenar informações de atributos de um método
    """
    node    = None
    line    = 0
    scopeId = 0
    def __init__(self, _name, _type, line, _id, duplicated = False) -> None:
        super().__init__(_name, _type)
        self.scopeId = _id
        self.line    = line
        self.duplicated = duplicated

    def show(self):
        print("(A) " + super().__str__())

    def toTree(self, noden):
        self.node = noden

class Type():
    """
    Classe responsável por armazenar e manipular um tipo em Cool
    """
    parent      = ""
    methods     = []    
    attributes  = []
    scopeId     = 0 
    duplicated  = False
    
    def __init__(self, _name, _id,line, _parent = ""):
        self.name   = _name
        if(_parent != ""): self.parent = _parent
        self.scopeId = _id
        self.line = line

    def newMethod(self,name, _type, _formals,line, scope_id):
        # verifica se o método já foi definido
        if(len([x for x in self.methods if name == x.name])!=0): # checar se já foi definida feauture com esse nome
            self.methods.append(Method(name, _type, _formals,line, scope_id, True))
        else:
            self.methods.append(Method(name, _type, _formals,line, scope_id))
    
    def alreadyDefined(self):
        self.duplicated = True

    def newAttribute(self, name, _type, line, _id):
        if(len([x for x in self.attributes if name == x.name])!=0):  # checar se já foi definida feauture com esse nome
            self.attributes.append(Attribute(name, _type, line, _id, True))
        else:
            self.attributes.append(Attribute(name, _type, line, _id))
    def getMethod(self, methodName):
        '''
        Parâmetro:
        ----------
        * name: nome da classe 

        Retorno
        -------
        * [] -> se o método não existe (False)
        * [Method] -> see o método existe
        '''
        return [m for m in self.methods if methodName == m.name]
    def getAttribute(self, attributeName):
        '''
        Parâmetro:
        ----------
        * name: nome da classe 

        Retorno
        -------
        * [] -> se o atributo não existe (False)
        * [Attribute] -> see o atributo existe
        '''
        return [a for a in self.attributes if attributeName == a.name]

        
        
    def show(self):
        print(f"(T) {self.name}({self.parent})")
        
        if(self.methods !=[]):
            for m in self.methods:
                m.show()

        if(self.attributes != []):
            for a in self.attributes:
                a.show()

# Criando as Basic Classes
Object_class    = Type("Object"  , 1001, 'BC')
Object_class.methods = [
    Method("about"          , "Object"      ,  []   ,1001, 'MBC'),
    Method("type_name"      , "String"      ,  []   ,1001, 'MBC'),
    Method("copy"           , "SELF_TYPE"   ,  []   ,1001, 'MBC')
]

IO_class        = Type("IO"      , 1002, 'BC')
IO_class.methods = [
    Method("out_string"  , "SELF_TYPE"   ,  [('x','String')]    ,1002, 'MBC'),
    Method("out_int"     , "SELF_TYPE"   ,  [("x","Int")]       ,1002, 'MBC'),
    Method("in_string"   , "String"      ,  []                  ,1002, 'MBC'),
    Method("in_int"      , "Int"         ,  []                  ,1002, 'MBC')
]
Int_class       = Type("Int"     , 1003, 'BC')

String_class    = Type("String"  , 1004, 'BC')
String_class.methods = [
    Method("length" , "Int"    ,  []   ,1001, 'MBC'),
    Method("concat" , "String" ,  [('s','String')]   ,1001, 'MBC'),
    Method("substr" , "String" ,  [('i','Int'),('l','Int')]   ,1001, 'MBC')
]
Bool_class      = Type("Bool"    , 1005, 'BC')

class Creator():
    '''
    Só é usado para formar a lista de tipos durante a análise sintática
    '''

    typeList = [Object_class, IO_class, Int_class, String_class, Bool_class]
    
    def addType(self, obj:Type):
        if(len([x for x in self.typeList if obj.name == x.name])!=0):
            obj.alreadyDefined()
            self.typeList.append(obj)
        else:
            self.typeList.append(obj)

    def printTypes(self):
        os.system("PAUSE")
        os.system("CLS")
        for _type in self.typeList:
            _type.show()
            os.system("PAUSE")
            os.system("CLS")

    def uniqueType(self, obj):
        if(len([_type.name for _type in self.typeList if _type.name.lower() == obj.name.lower()]) == 1):
            True
        else:
            print(f" len == {len([_type.name for _type in self.typeList if _type.name.lower() == obj.name.lower()])}")
            False

    def getClass(self, name, _id=-1): # retorna quantas vezes a classe foi encontrada e o objeto inteiro
        '''
        Parâmetro:
        ----------
        * name: nome da classe 
        
        Retorno
        -------
        * [] -> se o tipo não existe (False)
        * [Type] -> se o tipo existe

        '''

        return [c for c in self.typeList if name == c.name]

    def hasID():
        '''
        Função para verificar se 
            - o método possui a variável usada
            - ou se, caso tenha 
        '''
