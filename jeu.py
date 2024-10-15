import numpy as np
import evaluation as ev
import recursive_chat as rc

def init_parametres(dimensions):
    
    parametres = {}
    C = len(dimensions)   

    for c in range(1, C):

        parametres['W' + str(c)] = np.random.randn(dimensions[c], dimensions[c - 1])
        parametres['b' + str(c)] = np.random.randn(dimensions[c], 1)
           
    return parametres

def init(dimensions = list((9, 9, 9, 1))):
  
    parametres = init_parametres(dimensions)

    return parametres


def calcul(X, parametres, profondeur = 1):

    arbre_p = rc.run(X, parametres)


for i in range(100):
    X = [1, 0, -1,
        0, -1, 0,
        0, 0, 1]
            
                
    calcul(X,init())
    