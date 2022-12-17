import sys
import lexicalAnalyzer as LA
import syntaxAnalyzer as SYA
import semAnalyzer as SEA


try:
    fileName    =  sys.argv[1]
except:
    # fileName      =  "exemplos/ex1.cl"
    fileName      =  "exemplos/cTb1.cl"
    # fileName      =  "cool_programs/book.cl"


tokens = LA.readNtokenize(fileName)   # Análise léxica
LA.printTokens(tokens)

try:
    l = []
    for i in tokens:
        for j in i:
            l.append(j)

    typeList, synTree, synErr = SYA.switchTokens(l) # Análise Sintática

    SYA.showErrors(synErr)  
    # typeList.printTypes() 
    SYA.showTree(synTree)   
    
except StopIteration:
    print("Erro")

SEA.sem(typeList, synTree) # Análise semântica