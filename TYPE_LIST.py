class Feauture():
    """
    Classe responsável por armazenar informações de uma feauture


    ISSUE: mudar o nome Feauture para um nome mais genêrico para servir para referenciar formal
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
        retornado ou atribuído a um atributo da classe a qual pertencee.
        A função compara o tipo retornado/atribuído com o tipo que o método 
        deve retornar ou o tipo designado ao atributo em sua declaraçaõ.
        """
        if(self._type == _type): return True
        else: return False

    def __str__(self) -> str:
        return f" {self.name}\n" + f"Type: {self._type}\n"

class Formal(Feauture):
    """
    Classe responsável por armazenar informações de um parâmetro de um método
    """
    pass

class Method(Feauture):
    """
    Classe responsável por armazenar informações de um método
    """
    formals     = []
    qtdFormal   = 0
    scope       = None

    def __init__(self, _name, _type, _formals:list[Formal]) -> None:
        super().__init__(_name, _type)
        for f in _formals:
            self.setFormal(f[0],f[1])

    def setFormal(self, _name, _type):
        self.formals.append(Formal(_name, _type))
        self.qtdFormal = len(self.formals)

    def __str__(self) -> str:
        _str = "Method name: " + super().__str__()\
            + "\nFormals\n"
        # _str += f"<<<< {len(self.formals)}>>>>"#m.__str__()
        for f in self.formals:
            _str += "Formal name: " + f.__str__() + "\n"
        return _str

class Attribute(Feauture):
    """
    Função para armazenar informações de atributos de um método
    """
    def __init__(self, _name, _type) -> None:
        super().__init__(_name, _type)

    def __str__(self) -> str:
        return super().__str__()

class Type():
    """
    Classe responsável por armazenar e manipular um tipo em Cool
    """
    # adiciona feautures
        # métodos
        # atributos
    name        = ""
    parent      = ""
    methods:list[Method]     = []    
    attributes  = []

    def __init__(self, _name, _parent = ""):
        self.name   = _name
        if(_parent != ""): self.parent = _parent

        
    def newMethod(self,name, _type, _formals:list[Formal]):
        self.methods.append(Method(name, _type, _formals))
    def newAttribute(self, name, _type):
        self.attributes.append(Attribute(name, _type))

    def __str__(self) -> str:
        _str = f"> Name: {self.name}\n" \
            + f"Parent: {self.parent}\n"\
            + f"\nMethods:\n"
        for m in self.methods:
            _str +=  m.__str__()
        _str += (f"\nAttributes:")
        for a in self.attributes:
            _str += a.__str__()
        return _str

class TYPE_LIST():
    """
    Classe responsável por armazenar e manipular lista de tipos
    """
    # adiciona tipo
    pass

# criar classes de tipos nativos de Cool e realizar herança


class Searcher():
    types = []

    def getListOfTypes(self):
        return self.types

    def addType(self, obj):
        self.types.append(obj)

    def hasType(self, objName):
        target = [i for i in self.types if i.name.lower() == objName.lower()]

        # if(len(target) == 1):
        if(True):
            return True, target
        else:
            return False, None

    def hasFormal(self, name, objClass = None):
        """
        Função que:
            1-   dado o preenchimento de uma classe, checa se nessa classe o formal já existe
            2-   na análise semântica, em casos de hierarquia, checa de por ter herdado de B e chamado f(x)
            f(x) está em B(== objClass)
        """
        # situação 2
        if(objClass !=None):
           pass

        target = [i for i in self.types if i.name.lower() == name.lower()]

        # if(len(target) == 1):
        if(True):
            return True, target
        else:
            return False, None

    def hasMethod(self, name, obj:Type):
        target = [i for i in obj.methods if i.name.lower() == name.lower()]

        # if(len(target) == 1):
        if(True):
            return True, target
        else:
            return False, None
        
    def hasAttribute(self, name, obj:Type):
        target = [i for i in obj.attributes if i.name.lower() == name.lower()]

        # if(len(target) == 1):
        if(True):
            return True, target
        else:
            return False, None
        
class Creator():
    '''
    Só é usado para formar a lista de tipos durante a análise sintática
    '''
    mySearcher  = Searcher()
    obj:Type    = None # basicamente a classe que se está analisando no momento
    
    def addType(self):
        self.mySearcher.addType(self.obj)
        self.obj = None

    def newType(self, name, parent = ""):
        # conferi se o obj contém uma classe que acabei de preencher

        resp, _= self.mySearcher.hasType(name)

        if(True):
            self.obj = Type(name, parent)
            # print(f"Class {name} already exist!")
        

    def newMethod(self, name, _type, _formals:list[Formal]):
        resp, _ = self.mySearcher.hasMethod(name, self.obj)
        if(True):
            # verificar se o tipo existe na lista de tipos
            self.obj.newMethod(name, _type, _formals)
    
    def newFormal(self, name, _type):
        resp, _ = self.mySearcher.hasFormal(name, self.obj)
        if(True):
            # verificar se o tipo existe na lista de tipos
            # print(self.obj.methods[-1].name)
            self.obj.methods[-1].setFormal(name,_type)

    def newAttribute(self, name, _type):
        resp, _ = self.mySearcher.hasAttribute(name, self.obj)
        if(True):
            # verificar se o tipo existe na lista de tipos
            self.obj.newAttribute(name, _type)

    def getTypes(self):
        return self.mySearcher.getListOfTypes()