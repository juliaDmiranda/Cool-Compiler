class Node():
    # name  = ""# inútil
    # _type = ""# inútil
    children = None
    # def __init__(self, name, _type) -> None:
    #     self.name = name
    #     self._type = _type

    def addChild(self, obj):
        pass

# class Exprs(Node):
#     '''
#     Estrutura para {expr;}
#     '''
#     def __init__(self, name, _type) -> None:
#         super().__init__(name, _type)
#         self.children = []
#     def addChild(self, obj):
#         self.children.append(obj)
    
class Class (Node):
    '''
    Estrutura para operadores OBJ

    OBS.:
        - _type:  corresponde ao retorno da expressão
    '''
    def __init__(self, name, _type) -> None:
        super().__init__(name, _type)

    def addChild(self, obj):
        if(self.children != None):
            print("Node operator do not have more then one child")
        else:
            self.children = obj
class Attribution(Node):
    '''
    Estrutura para ID <- expr

    OBS.:
        - _type:  corresponde ao retorno da expressão
    '''
    def __init__(self, name) -> None:
        self.idName = name

    def addChild(self, obj):
        if(self.children != None):
            print("Node attribution do not have more then one child")
        else:
            self.children = obj
class Operator(Node):
    '''
    Estrutura para operadores +, -, *, /, isvoid, ~, not

    OBS.:
        - _type:  corresponde ao retorno da expressão
    '''
    opType = None
    opName = None 
    def __init__(self, name, _type) -> None:
        self.opName = name
    def addChild(self, obj):
        if(self.children != None):
            print("Node operator do not have more then one child")
        else:
            self.children = obj
    
class If(Node):
    '''
    Estrutura para expressão new

    OBS.:
        - _type:  corresponde ... 
    '''
    _type = None
    def __init__(self, name=0, _type=0) -> None:
        self.children = []
    def addChild(self, obj):
        if(len(self.children) == 3):
            print("Node If do not have more then 3 child")
        else:
            self.children.append(obj)

class Terminals():
    value = None
    _type = None

    def __init__(self, value, _type) -> None:
        self.value = 0
        self._type = _type

class While(Node):
    '''
    Estrutura para expressão while

    OBS.:
        - _type:  corresponde ... 
    '''
    def __init__(self, name=0, _type=0) -> None:
        # super().__init__(name, _type)
        self.children = []

    def addChild(self, obj):
        if(len(self.children) == 2):
            print("Node While do not have more then 2 child")
        else:
            self.children.append(obj)

