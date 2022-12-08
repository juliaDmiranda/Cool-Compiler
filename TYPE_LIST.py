import os


class Feature():
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


class Method(Feature):
    """
    Classe responsável por armazenar informações de um método
    """
    # name, _type = "","" 
    formals     = []
    qtdFormal   = 0
    scopeId     = 0
    node        = None

    def __init__(self, _name, _Type, _formals,line, _id):
        super().__init__(_name, _Type)
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
    def __init__(self, _name, _type, line, _id) -> None:
        super().__init__(_name, _type)
        self.scopeId = _id
        self.line    = line

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

    def __init__(self, _name, _id,line, _parent = ""):
        self.name   = _name
        if(_parent != ""): self.parent = _parent
        self.scopeId = _id
        self.line = line

    def newMethod(self,name, _type, _formals,line, scope_id):
        # print(len(self.methods))
        self.methods.append(Method(name, _type, _formals,line, scope_id))

    def newAttribute(self, name, _type, line, _id):
        self.attributes.append(Attribute(name, _type, line, _id))

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
    hasMain  = False
    def addType(self, obj:Feature):
        if(obj.name.lower() == "main"):
            self.hasMain = True 
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

    def getClass(self, name, _id=False): # retorna quantas vezes a classe foi encontrada e o objeto inteiro
        cont = 0
        rtn  = False 
        for _type in self.typeList:
            if(_type.name == name):
                cont+=1
                if (not _id):
                    rtn = _type
                else:
                    if(_type.scopeId == _id):
                        rtn = _type
        return  rtn, cont

    def getMethod(self, name,classNameOrObj = "", _id= False):
        if(classNameOrObj != "" and isinstance(classNameOrObj,str)):
            obj, _ = self.getClass(classNameOrObj) # retorna a estrutura da classe onde o methodo está
        else:
            obj = classNameOrObj
        cont = 0
        rtn  = False

        for m in obj.methods: # procura o método
            if(m.name == name):
                cont+=1
                if (not _id):
                    rtn = m
                else:
                    if(m.scopeId == _id):
                        rtn = m

        return rtn, cont

    def getAttribute(self, className, name, obj = None, _id=False):
        if(obj == None):
            obj, _ = self.getClass(className) # retorna a estrutura da classe onde o atributo está
        cont = 0
        rtn  = False

        for a in obj.attributes: # procura o método
            if(a.name == name):
                cont+=1
                if (not _id):
                    rtn = a
                else:
                    if(a.scopeId == _id):
                        rtn = a

        return rtn, cont

    def hasID():
        '''
        Função para verificar se 
            - o método possui a variável usada
            - ou se, caso tenha 
        '''