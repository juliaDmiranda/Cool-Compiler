import lexicalAnalyzer as LA
import sys

fileName    =  sys.argv[1]

tokens = LA.readNtokenize(fileName)

LA.printTokens(tokens)
