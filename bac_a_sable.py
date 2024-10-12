import numpy as np
from tqdm import tqdm

def initialisation(dimensions):
    
    parametres = {}
    C = len(dimensions)



    for c in range(1, C):
        parametres['W' + str(c)] = np.random.randn(dimensions[c], dimensions[c - 1])*10
        parametres['b' + str(c)] = np.random.randn(dimensions[c], 1)*10
    return parametres

def forward_propagation(X, parametres):
  
  activations = {'A0': X}

  C = len(parametres) // 2

  for c in range(1, C + 1):

    Z = parametres['W' + str(c)].dot(activations['A' + str(c - 1)]) + parametres['b' + str(c)]
    activations['A' + str(c)] = 1 / (1 + np.exp(-Z))

  return activations

def score(grille):

    if np.abs(grille[0,0]) == 99:
        return False

    for i in range(3):
        if grille[i,0] == grille[i,1] == grille[i,2] != 0:
            return True
        
    for j in range(3):
        if grille[0,j] == grille[1,j] == grille[2,j] != 0:
            return True

    if grille[0,0] == grille[1,1] == grille[2,2] != 0:
        return True
    
    if grille[0,2] == grille[1,1] == grille[2,0] != 0:
        return True
    
    return False

def predict(X, parametres):
  activations = forward_propagation(X, parametres)
  C = len(parametres) // 2
  Af = activations['A' + str(C)]
  return Af

def update(parametres, learning_rate, dimensions):

    new_parametre = parametres.copy()

    C = len(new_parametre) // 2
    
    for c in range(1, C + 1):
        new_parametre['W' + str(c)] = new_parametre['W' + str(c)] + np.random.randn(dimensions[c], dimensions[c - 1])*learning_rate
        new_parametre['b' + str(c)] = new_parametre['b' + str(c)] + np.random.randn(dimensions[c], 1)*learning_rate

    return new_parametre

def generation(nombre_joueur = 5, parametres_list = 0, victoire = 1, defaite = -2):
   
    X_total = np.zeros((nombre_joueur,nombre_joueur,9), dtype=int)
    classement = np.zeros(nombre_joueur)

    for i in range(9):  
        for j in range(X_total.shape[1]):          

            Y = predict(X_total[j].T, parametres_list[j]).T

            X_total[j,np.arange(X_total.shape[1]),np.argmax(Y - np.abs(X_total[j]), axis=1)] = 1

            

            X_total[j,j,0] = 99

            for l in range(X_total.shape[1]):                    
                if score(X_total[j,l].reshape(3,3)) == 1:
                                        
                    X_total[j,l,0] = 99

                    classement[j] += victoire
                    classement[l] += defaite

        X_total = -X_total.swapaxes(0, 1)

    return classement

def init(nombre_joueur = 5, dimensions = list((9, 9))):
    
    parametres_list = np.empty(nombre_joueur,dtype=dict)

    for i in range(parametres_list.shape[0]):
        parametres_list[i] = initialisation(dimensions)

    return parametres_list

def mutation(parametres_list = 0, classement = 0, nombre_joueur = 5, learning_rate = 10, dimensions = list((9,9))):


    parametres_darwin = parametres_list[np.argmax(classement)]

    new_parametres_list = np.empty(nombre_joueur,dtype=dict)


    new_parametres_list[0] = parametres_darwin
    for i in range(1,parametres_list.shape[0]):
        new_parametres_list[i] = update(parametres_darwin, learning_rate, dimensions)


    return new_parametres_list

def multi_evaluation(parametre_darwin = 0):

    parametre = init(nombre_joueur=99)

    parametre = np.insert(parametre, [0], parametre_darwin, axis= None)

    
     
    classement = generation(nombre_joueur = 100, parametres_list = parametre, victoire=0, defaite=-1)

     
    print(str(classement[0]/2)  +  " %")
    
def calcul(nombre_joueur = 100, nombre_génération = 100000, learning_rate = 10, dimensions = list((9, 9, 9, 9, 9))):

    parametres_list = init(nombre_joueur, dimensions)

    for t in tqdm(range(nombre_génération)):

        classement = generation(nombre_joueur, parametres_list)

        

        parametres_list = mutation(parametres_list, classement, nombre_joueur, learning_rate, dimensions)

        

        if t%10 == 0 and t != 0:

            parametres_darwin = parametres_list[np.argmax(classement)]
            multi_evaluation(parametre_darwin = parametres_darwin)

        if t%10 == 0 and t != 0:

            fichier = open("data.txt", "a")
            fichier.write(str(parametres_darwin))
            fichier.close()

    

    return parametres_darwin


fichier = open("data.txt", "w")
fichier.write(str(""))
fichier.close()

parametre_final = calcul()

fichier = open("data.txt", "a")
fichier.write(str(parametre_final))
fichier.close()


