import sys
import lexicalAnalyzer as LA
import syntaxAnalyzer as SA
from class_ import Token
def printDiferente(aux):
    print(next(aux))
try:
    fileName    =  sys.argv[1]
except:
    fileName      =  "cool_programs/primes.cl"
tokens = LA.readNtokenize(fileName)
LA.printTokens(tokens)
try:
    l = []
    for i in tokens:
        for j in i:
            l.append(j)

    SA.switchTokens(l)
    
except StopIteration:
    print("Erro amigo")