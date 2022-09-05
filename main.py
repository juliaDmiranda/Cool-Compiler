import re, class_, sys

                                            # Processamento de List #

removeNone = lambda line : list(filter(None, line)) # Remover ''

                                            # Processamento de String #

removeLineComment = lambda line : line.partition('--')[0] # Remover comentários de linha - Retorna string

def removeBlockComment(line):
    pattern = "([^\"]\\S*|\".+?\")\\s*"

    # Tem (* *)?
    if (re.match(pattern, line)):
        
    # Tem (*
        # Mais de 1
            # Raise Erro
        # 1 
            # Remove comentário
            # Marca :Achou comentário de bloco
    # Tem *)
        # Mais de 1
            # Erro
        # 1 
            # Verifica se tem comentário acima
                # Tem
                    # Remove comentário
                    # Achou comentário de bloco
                # não 
                    # Raise Erro
    pass

spaceSymbols =  lambda line : line.replace("\n", " ").replace("@", " @ ")\
                .replace(",", " , ").replace('"', ' " ').replace("(", " ( ")\
                .replace(")"," ) ").replace(";", " ; ").replace("}", " } ")\
                .replace("{", " { ").replace(":", " : ").replace(".", " . ") # Espaçar símbolos para split - Retorna string


# Função para separar tokens de cada linha, mantendo unidas as strings que em Cool são qualquer estrutura na forma "...".
# Não é aceito como String a utilização '...'
# Retorna lista contendo tokens, sem tratar comentário em bloco, string
splitLine = lambda line: removeNone(spaceSymbols(removeLineComment(line)).split(" ")) 

def readProgram(fileName):
    '''
    Função que lê arquivo de programa escrito em Cool
    Retorna uma lista de instâncias de Token() para cada linha
    '''
    code = [] # list of tokens

    with open(fileName, 'r') as file:
        program = file.readlines()

        for num, line in enumerate(program, start=0):
            # Remover Comentários
            removeBlockComment(line)

            temp = splitLine(line) # tokens criados
            
        
        # FORMAR LISTA DE CLASSES
        # code.append([class_.Token(str, num+1) for str in temp])

    return code

# ler arquivo
    # para cada linha
        # Ajeitar string
            # remover comentário
            # remover \n ()

if __name__ == "__main__":
    fileName    =  sys.argv[1]
    
    cd = readProgram(fileName)
    for i in cd:
        for j in i:
            print(j)