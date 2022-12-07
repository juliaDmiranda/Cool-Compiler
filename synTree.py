from enum import Enum, auto
import itertools

class tag (Enum):
    ATTRIBUTE   = auto()
    BRACKETS    = auto()
    BOOL        = auto()
    CLASS       = auto()
    CASE        = auto()
    CASEOPT     = auto()
    EXPRL       = auto()
    FUNCALL     = auto()
    FUNCALLID   = auto()
    FORMALS     = auto()
    IF          = auto()
    ID          = auto()
    ISVOID      = auto()
    INTEGER     = auto()
    LET         = auto()
    LETOPT      = auto()
    METHOD      = auto()
    MULTEXPR    = auto()
    NEW         = auto()
    NOT         = auto()
    OPE         = auto()
    PARENTHESIS = auto()
    SETID       = auto()
    STRING      = auto()
    TIDE        = auto()
    WHILE       = auto()
class Node():
    id_obj = itertools.count()
    label, token ,children,_type, line = None,None, None, None, None # para a análise semântica
    name = ""

    def __init__ (self, fatherId):
        self.father = fatherId
        self.id = next(Node.id_obj)

    def setLabel(self, label):
        if(isinstance(label, str)):
            if(label == "INTEGER"):
                label = tag.INTEGER
            elif(label == "STRING"):
                label = tag.STRING
            elif(label == "TRUE" or label == "FALSE"):
                label = tag.BOOL
        self.label = label
    
    def setType(self, type):
        self._type = type

    def setName(self, name):
        self.name = name

    def setInherit(self, father):
        self.inherit = father

    def setLine(self, line):
        self.line = line

    def addChild(self, obj="NULL", hasFormals = False):
        if(self.children == None):
            self.children = []
        if(hasFormals):
            self.formals = obj
        else:
            self.children.append(obj)
    
    def getName(self):
        return self.name
    
    def getLine(self):
        return self.line

    def getLabel(self):
        return self.label

    def __str__(self) -> str:
        if (self.label == tag.METHOD):
            try:
                return f"<{self.getLine()}>[{str(self.label.name)}] {self.getName()} : {self._type} : {self.formals}"
            except:
                return f"<{self.getLine()}>[{str(self.label.name)}]{self.getName()} : {self._type}"
        else:
            return f"<{self.getLine()}>[{str(self.label.name)}]{self.getName()} : {self._type}"
            

def showTree_aux(myTree:Node):
    try:
        if(type(myTree) != list):
            print(myTree)
            if(type(myTree) == Node):
                if(myTree.children != None):
                    if(len(myTree.children) != 0):
                        for child in myTree.children:
                            showTree_aux(child)      
        # elif(len(myTree.children) != 0):
        #     print("ENTREIIIIIIIIIIIII")
        #     for child in myTree.children:
        #         showTree_aux(child)
    except Exception as ex:
        print(ex.args)
        print("\n\n\n>>>>>>>>>>>>>",myTree.name)
def showTree(root):
    for c in root:
        showTree_aux(c)
# class Attribution(Node):
#     '''
#     Estrutura para ID <- expr

#     OBS.:
#         - _type:  corresponde ao retorno da expressão
#     '''
#     def addChild(self, obj):
#         if(len(self.children) == 1):
#             print("Node attribution do not have more then 1 child")
#         else:
#             self.children.append(obj)


# class Operator(Node):
#     '''
#     Estrutura para operadores +, -, *, /, isvoid, ~, not

#     OBS.:
#         - _type:  corresponde ao retorno da expressão
#     '''
#     def addChild(self, obj):
#         if(len(self.children) == 1):
#             print("Node operator do not have more then 1 child")
#         else:
#             super().addChild(obj)

# class If(Node):
#     '''
#     Estrutura para expressão if

#     OBS.:
#         - _type:  corresponde ... 
#     '''

#     def addChild(self, obj):
#         if(len(self.children) == 3):
#             print("Node If do not have more then 3 child")
#         else:
#             super().addChild(obj)
    
#     def __str__(self):
#         return f"(IF)\n"

# class Terminals(Node):
#     def addChild(self, obj):
#         super().addChild(obj)

# class While(Node):
#     '''
#     Estrutura para expressão while

#     OBS.:
#         - _type:  corresponde ... 
#     '''
#     def addChild(self, obj):
#         if(len(self.children) == 2):
#             print("Node While do not have more then 2 child")
#         else:
#             super().addChild(obj)

# class ID(Node):
#     def addChild(self, obj):
#         if(len(self.children) == 1):
#             print("Node ID do not have more then 1 child")
#         else:
#             super().addChild(obj)

# class Parenthesis(Node):
#     def addChild(self, obj):
#         super().addChild(obj)