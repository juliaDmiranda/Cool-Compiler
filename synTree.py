from enum import Enum, auto
import itertools

class tag (Enum):
    ATTRIBUTE   = auto()
    BRACKETS    = auto()
    BOOL        = auto()
    CLASS       = auto()
    CASE        = auto()
    CASEOPT     = auto()
    DOT         = auto()
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
    father = "-"

    def __init__ (self):
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
        if(isinstance(obj, Node)):
            obj.father = self.id
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
                return f"(f:{self.father}/id:{self.id})<{self.getLine()}>[{str(self.label.name)}] {self.getName()} : {self._type} : {self.formals}"
            except:
                return f"(f:{self.father}/id:{self.id})<{self.getLine()}>[{str(self.label.name)}]{self.getName()} : {self._type}"
        else:
            return f"(f:{self.father}/id:{self.id})<{self.getLine()}>[{str(self.label.name)}]{self.getName()} : {self._type}"
            

def showTree_aux(myTree:Node, file, print_ = False):
    try:
        if(type(myTree) != list):
            if(print_):
                print(myTree)
            file.write("\n"+str(myTree))
            if(type(myTree) == Node):
                if(myTree.children != None):
                    if(len(myTree.children) != 0):
                        for child in myTree.children:
                            file = showTree_aux(child, file)   
        return file
    except Exception as ex:
        print(ex.args)
        print("\n\n\n>>>>>>>>>>>>>",myTree.name)

def showTree(root, print_ = False):
    file = open("synTree", "w")
    for c in root:
        file = showTree_aux(c, file, print_)