import os
import syntaxFun as SF
import synTree as st
# import syntaxFun_bf as SF

def showTree_aux(myTree:st.Node, file, print_ = False):
    try:
        if(type(myTree) != list):
            if(print_):
                print(myTree)
            file.write("\n"+str(myTree))
            if(type(myTree) == st.Node):
                if(myTree.children != []):
                    for i in myTree.children:
                        file = showTree_aux(i, file)   
        return file
    except Exception as ex:
        os.system('PAUSE')
        print(ex.args)
        print("\n\n\n>>>>>>>>>>>>>",myTree.name)
        print("\n\n\n>>>>>>>>>>>>>",type(file))

# def show(root):
#     if(isinstance(root, st.Node)):
#         print(root.children)
#         if root.children != []:
#             for i in root.children:
#                 show(i)

def showTree(root, print_ = False):
    file = open("synTree", "w")
    for c in root:
        showTree_aux(c, file)

def showErrors(err):
    aux = [a for a in  err if not a==[]]
    if aux==[]:
        print("No syntax error in the program")
    else:
        print("Syntax Error\n"+('-'*30)+"\n")
        for e in aux:
            print(e)
    os.system("PAUSE")
    os.system("CLS")

def switchTokens(l):
    if(l == []):
        print("No code recoganized")
    # primeira chamada do programa deve conter uma class
    else:
        data = SF.program(l)
        err = data[0].getErr() 
        synTree   = data[3] 
        typeList  = data[1][0]

        return typeList, synTree, err
