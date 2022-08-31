import sys

def printProgramElements():
    '''
    Prints each token of the program followed by theirs identifiers  
    '''
    pass

def classifyTokens(line):
    '''
    Function that receive a line of a Cool program and classify each token of that line
    '''
    pass
    
def readProgram(fileName):
    '''
    Function to read the program in Cool and store in a list wich elements are lines of code
    '''
    code = []
    with open(fileName, 'r') as file:    
        line = file.readlines()

        print(line)
        '''
        Considering that the grammer do not make a 
        restriction about space where you can use 
        it or not between symbols, I must check if
        after split strings, there are any digit or special symbol on it
        My be use regex would make it easier
        '''


fileName    = sys.argv[1]

identifier = [] # list of dictionary. Think in classify each line in a list to mark the numeration of the line in one take

readProgram(fileName)
    