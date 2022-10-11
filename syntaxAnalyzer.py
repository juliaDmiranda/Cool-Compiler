import class_
import syntaxFun as SF
import Program_class as PC

def showErrors(err):
    aux = [a for a in  err if not a==[]]
    if aux==[]:
        print("No syntax error in the program")
    else:
        print("Syntax Error\n"+('-'*30)+"\n")
        for e in aux:
            print(e)

def switchTokens(l):
    if(l == []):
        print("No code recoganized")
    # primeira chamada do programa deve conter uma class
    else:
        myProgram = SF.program(l)
        showErrors(myProgram.err)
