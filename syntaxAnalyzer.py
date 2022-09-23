import class_
import syntaxFunc

# verifica class
def CLASS_ID_func(line, err=[]):
    pass

def switchTokens(line, err=[]):
    for token in line:
        try:
            # func = globals()[token.id.value[:-2:]+"_func"] # para quando a função está no módulo
            func = getattr(syntaxFunc, [token.id.value[:-2:]+"_func"])
            line, err = func(line, err)
        except KeyError:
            pass 
            # função coringa
            # por que daria Esse erro?
        # cada chamada retorna a lista consumida atualizada
        # ao fim chamamos novamente a função passando essa linha atualizada
        # se ao sair a linha estiver vazia()
            # sai do for antes que bagunce tudo
        pass
