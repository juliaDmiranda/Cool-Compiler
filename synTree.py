class Node():
    name  = ""
    _type = ""
    children = None
    def __init__(self, name, _type) -> None:
        self.name = name
        self._type = _type

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

class Operator(Node):
    '''
    Estrutura para operadores +, -, *, /, isvoid, ~, not

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
    
class If(Node):
    '''
    Estrutura para expressão new

    OBS.:
        - _type:  corresponde ... 
    '''
    def __init__(self, name, _type) -> None:
        super().__init__(name, _type)
        self.children = []
    def addChild(self, obj):
        if(len(self.children) == 3):
            print("Node If do not have more then 3 child")
        else:
            self.children.append(obj)
class While(Node):
    '''
    Estrutura para expressão while

    OBS.:
        - _type:  corresponde ... 
    '''
    def __init__(self, name, _type) -> None:
        super().__init__(name, _type)
        self.children = []

    def addChild(self, obj):
        if(len(self.children) == 2):
            print("Node While do not have more then 2 child")
        else:
            self.children.append(obj)
