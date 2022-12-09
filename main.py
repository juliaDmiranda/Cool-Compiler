import sys
import lexicalAnalyzer as LA
import syntaxAnalyzer as SYA
import semAnalyzer as SEA


try:
    fileName    =  sys.argv[1]
except:
    fileName      =  "cool_programs/book.cl"


tokens = LA.readNtokenize(fileName)   # Análise léxica
LA.printTokens(tokens)

try:
    l = []
    for i in tokens:
        for j in i:
            l.append(j)

    typeList, synTree, synErr = SYA.switchTokens(l) # Análise Sintática

    # SYA.showErrors(synErr)  # printa erros
    # typeList.printTypes()   # prita lista de tipos
    SYA.showTree(synTree)   # passa para arquivo
    
except StopIteration:
    print("Erro")

SEA.main(typeList, synTree) # Análise semântica