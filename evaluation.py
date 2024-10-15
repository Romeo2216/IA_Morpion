import numpy as np
from tqdm import tqdm

"""np.random.seed(0)"""




def forward_propagation(X, parametres):
  
    activations = {'A0': X}

    C = len(parametres) // 2

    for c in range(1, C + 1):
        
        Z = parametres['W' + str(c)].dot(activations['A' + str(c - 1)]) + parametres['b' + str(c)]
        activations['A' + str(c)] = (1 / (1 + np.exp(-Z)))-0.5

    return activations


def predict(X, parametres):
  
    activations = forward_propagation(X, parametres)
    C = len(parametres) // 2
    Af = activations['A' + str(C)]

    return Af





def test(X, parametres):

    activations = predict(X,parametres)

    return activations[0,0]

"""X = np.zeros((9), dtype=int)

for i in range(15):
    print("{0:.1f}".format(test(X)*100) + "%")"""