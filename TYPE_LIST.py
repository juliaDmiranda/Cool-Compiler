import os
import synTree as ST
class Feature(ST.Node):
    """
    Classe responsável por armazenar informações de uma feature


    ISSUE: mudar o nome Feature para um nome mais genêrico para servir para referenciar formal
    """
    name = ""
    _type = None

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


class Method(ST.Node):
    """
    Classe responsável por armazenar informações de um método
    """
    name, _type = "","" 
    formals     = []
    qtdFormal   = 0
    scope       = None

    def __init__(self, _name, _type, _formals):
        self.name = _name
        self._type = _type
        self.formals = _formals
        self.qtdFormal = len(self.formals)

    def show(self):
        print(f"(M) {self.name}-{self._type}")
        if(self.formals != []):
            print(str(self.formals))

    def addChild(self, obj):
        if(self.children != None):
            print("Node METHOD do not have more then one child")
        else:
            self.children = obj  

class Attribute(ST.Node):
    """
    Função para armazenar informações de atributos de um método
    """
    name, _type = "","" 
    def __init__(self, _name, _type) -> None:
        self.name = _name
        self._type = _type

    def show(self):
        print("(A) " +  f" {self.name}-{self._type}\n")

    def addChild(self, obj):
        if(self.children != None):
            print("Node ATTRIBUTE do not have more then one child")
        else:
            self.children = obj  

class Type():
    """
    Classe responsável por armazenar e manipular um tipo em Cool
    """
    # adiciona features
        # métodos
        # atributos
    name        = ""
    parent      = ""
    methods     = []    
    attributes  = []

    def __init__(self, _name, _parent = ""):
        self.name   = _name
        if(_parent != ""): self.parent = _parent

        
    def newMethod(self,name, _type, _formals):
        # print(len(self.methods))
        self.methods.append(Method(name, _type, _formals))

    def newAttribute(self, name, _type):
        self.attributes.append(Attribute(name, _type))

    def show(self):
        print(f"(T) {self.name}({self.parent})")
        
        if(self.methods !=[]):
            # print(f"(M) {len(self.methods)}")
            for m in self.methods:
                m.show()
        if(self.attributes != []):
            # print(f"(A) {len(self.attributes)}")
            for a in self.attributes:
                a.show()

class Creator():
    '''
    Só é usado para formar a lista de tipos durante a análise sintática
    '''
    typeList = []
    
    def addType(self, obj):
        self.typeList.append(obj)

    def printTypes(self):
        os.system("CLS")
        for _type in self.typeList:
            _type.show()
            os.system("PAUSE")
            os.system("CLS")
