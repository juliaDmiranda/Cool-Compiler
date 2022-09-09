'''
Programa que realiza a análise léxica de um código em Cool
'''
from hashlib import new
import re, class_, sys

removeNone = lambda line : list(filter(None, line)) # Remover ''

spaceSymbols =  lambda line : line.replace("\n", " ").replace("@", " @ ").replace("*", " * ")\
                .replace(",", " , ").replace('"', ' " ').replace("(", " ( ").replace("/", " / ")\
                .replace(")"," ) ").replace(";", " ; ").replace("}", " } ")\
                .replace("{", " { ").replace(":", " : ").replace(".", " . ").replace("--"," -- ") # Espaçar símbolos para split - Retorna string

removeLineComment = lambda line : line.partition('--')[0] # Remover comentários de linha - Retorna string
def removeLineComment(line):
    try:
        commentSymb = line.index("--")
        return line[:commentSymb:]
    except:
        return line
searchAsterisk  = False
searchClose     = False
openComment     = False
def removeBlockComments(line):
    global searchAsterisk
    global searchClose
    global openComment
    newList = []
    ant = ""
    # elemento por elemento
    for token in line:
        if (searchClose):
            if(token != ")"):
                # ignora
                ant = token
                openComment = True
            else:
                if(ant == "*"):         # anterior é *
                    # (?)não procura mais *
                    # não procura mais fecha
                    searchClose = False
                    openComment = False
                else:
                    ant = token
        elif(searchAsterisk):
            if(token == "*"): # sim# proximo é *? 
                # ignora
                searchClose     = True # procura fecha
                searchAsterisk  = False
            else:# não
                if(ant=="("):
                    newList.append("(")     # append (
                newList.append(token)   # append atual
                searchAsterisk  = False # não procura mais *
        else:    # acha (
            if(token=="("):
                searchAsterisk = True
                ant = token
            else:
                newList.append(token)
        
    if(searchClose):
        if (openComment):
            pass
        else:
            openComment = True

    return newList
removeComments = lambda line : removeLineComment(removeBlockComments(line))

splitLine = lambda line: line.split(" ") 

stringOpen = False
def isolateString(line):
    '''
    Function to isolate Strings
    "..." or "... or  "
    '''
    global stringOpen
    newline = []
    tempStr = ""
    # percorre elem a elem
    for token in line:
        # é "?
        if(token != '"'):               # não
            if(not stringOpen):
                newline.append(token)       # add na lista
            else:
                tempStr     = tempStr + " " + token    # soma string vazia
        else:                           # é
            if (not stringOpen):        # se String não aberta
                tempStr     = tempStr + token    # soma string vazia
                stringOpen  = True      # marca string aberta
            else:                       # se string aberta
                if(stringOpen):
                    stringOpen  = False     # desmarca String aberta
                tempStr     = tempStr + " " + token    # soma string vazia
                newline.append(tempStr) # add str acumulado na lista
                tempStr = ""            # vazia str de apoio
    if(stringOpen):
        if(tempStr[-1::]=="\\"):
            newline.append(tempStr)
        else: raise Exception(r'Error!Missing one ". Did you mean "...\"? ')
    return newline

def readNtokenize(fileName):
    '''
    Function that reads and tokenizes a given Cool program
    '''
    code = [] # list of list of tokens

    with open(fileName, 'r') as file:
        program = file.readlines()

        for num, line in enumerate(program, start=0):
            # line = removeComments(line)
            line = spaceSymbols(line)
            temp = splitLine(line) # tokens criados
            temp = removeNone(temp) # remover ''
            temp = isolateString(temp)
            temp = removeComments(temp)
            if len(temp)!=0: # não conta lista vazia
                code.append([class_.Token(str, num+1) for str in temp if str.strip()])
        if(openComment):
            raise Exception("Error! Unclosed block comment")    
    
    return code

def printTokens(tokensID):
    for i in tokensID:
        for j in i:
            print(j)

if __name__ == "__main__":
    fileName    =  sys.argv[1]
    
    cd = readNtokenize(fileName)
    print(cd)
    printTokens(cd)
