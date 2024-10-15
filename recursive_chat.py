import evaluation as ev

class TreeNode:
    def __init__(self, board, player, parametres, move_count=0):
        self.board = board  # Grille actuelle (un état du jeu)
        self.player = player  # Joueur actuel (1 pour X, -1 pour O)
        self.move_count = move_count  # Nombre de coups joués depuis le début de la partie
        self.children = []  # Enfants représentant les coups suivants possibles
        self.evaluation = None  # Valeur d'évaluation de cette position
        self.parametres = parametres

    def is_terminal(self):
        """Vérifie si la partie est terminée (victoire, défaite ou match nul)."""
        return check_winner(self.board, 1) or check_winner(self.board, -1) or 0 not in self.board

    def evaluate(self):
        """Évalue la position actuelle en utilisant Minimax pour trouver la pire valeur possible à chaque étape."""
        if self.is_terminal():
            # On renvoie une évaluation fixe si c'est une victoire ou une défaite
            if check_winner(self.board, 1):
                return 1  # Victoire de X
            elif check_winner(self.board, -1):
                return -1  # Victoire de O
            elif self.move_count == 9:
                return 0
            
                
        """intermediaire = ev.test(self.board, self.parametres)"""

        # Minimax: Si c'est le tour de X (player = 1), on maximise
        if self.player == 1:
            max_eval = ev.test(self.board, self.parametres)
            for child in self.children:
                eval_child = child.evaluate()  # Évaluer chaque enfant avec Minimax
                max_eval = min(max_eval, eval_child)
            self.evaluation = max_eval  # Ajouter l'évaluation intermédiaire à l'évaluation Minimax
            return self.evaluation

        # Minimax: Si c'est le tour de O (player = -1), on minimise
        else:
            min_eval = float('inf')
            for child in self.children:
                eval_child = child.evaluate()  # Évaluer chaque enfant avec Minimax
                min_eval = min(min_eval, eval_child)
            self.evaluation = min_eval  # Ajouter l'évaluation intermédiaire à l'évaluation Minimax
            return 1

    def expand(self, seen_boards):
        """Génère les enfants de cet état et évalue chaque position."""
        if self.is_terminal():
            # Si l'état est terminal, on ne génère pas d'enfants
            return
        
        # Chercher toutes les cases vides
        empty_indices = [i for i, cell in enumerate(self.board) if cell == 0]
        
        # Générer un enfant pour chaque case vide
        for index in empty_indices:
            new_board = self.board[:]
            new_board[index] = self.player  # Jouer sur cette case
            next_player = -1 if self.player == 1 else 1  # Changement de joueur
            
            # Trouver la grille canonique (plus petite parmi toutes les rotations/miroirs)
            canonical_board = find_canonical_board(new_board)

            # Si cette grille canonique a déjà été vue, on ne la traite pas
            if tuple(canonical_board) in seen_boards:
                continue

            # Ajouter cette grille aux grilles vues
            seen_boards.add(tuple(canonical_board))

            # Créer un nouvel enfant avec un move_count incrémenté
            child_node = TreeNode(new_board, next_player, move_count=self.move_count + 1, parametres = self.parametres)
            child_node.expand(seen_boards)  # Expansion récursive pour l'enfant
            
            # Ajouter cet enfant à la liste des enfants
            self.children.append(child_node)

    def best_move(self):
        """Retourne l'enfant avec la meilleure évaluation pour le joueur actuel (X ou O)."""
        if not self.children:
            return None

        # Si c'est le tour de X (player = 1), on choisit l'évaluation maximale
        if self.player == 1:
            best_child = max(self.children, key=lambda child: child.evaluation)
        # Si c'est le tour de O (player = -1), on choisit l'évaluation minimale
        else:
            best_child = min(self.children, key=lambda child: child.evaluation)
        
        return best_child


# Fonction pour vérifier un gagnant
def check_winner(board, player):
    win_conditions = [
        [0, 1, 2],  # Ligne du haut
        [3, 4, 5],  # Ligne du milieu
        [6, 7, 8],  # Ligne du bas
        [0, 3, 6],  # Colonne de gauche
        [1, 4, 7],  # Colonne du milieu
        [2, 5, 8],  # Colonne de droite
        [0, 4, 8],  # Diagonale principale
        [2, 4, 6]   # Diagonale secondaire
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

# Fonction pour faire tourner la grille de 90 degrés (sens horaire)
def rotate_board(board):
    return [board[6], board[3], board[0], 
            board[7], board[4], board[1], 
            board[8], board[5], board[2]]

# Fonction pour refléter la grille horizontalement (miroir)
def mirror_board(board):
    return [board[2], board[1], board[0],
            board[5], board[4], board[3],
            board[8], board[7], board[6]]

# Fonction pour trouver la grille canonique (la plus petite parmi les rotations et miroirs)
def find_canonical_board(board):
    boards = [board]  # L'originale
    current_board = board
    
    # Ajouter toutes les rotations
    for _ in range(3):
        current_board = rotate_board(current_board)
        boards.append(current_board)
    
    # Ajouter les miroirs et leurs rotations
    mirrored = mirror_board(board)
    boards.append(mirrored)
    current_board = mirrored
    for _ in range(3):
        current_board = rotate_board(current_board)
        boards.append(current_board)
    
    # Retourner la plus petite (celle qui vient en premier par ordre lexicographique)
    return min(boards)

"""# Exemple de grille partielle (1 pour X, -1 pour O, 0 pour vide)
initial_board = [
    1, -1, 1,
    0, -1, 0,
    0, 0, 0
]"""

def run(initial_board, param):

    # Créer la racine de l'arbre (le joueur actuel est 1 ou -1 en fonction du tour)
    root = TreeNode(initial_board, player=1,parametres = param, move_count=5)  # Le compteur de coups commence à 5 (car 5 coups ont été joués)

    # Créer un ensemble pour garder les grilles vues
    seen_boards = set()

    # Ajouter la grille initiale à l'ensemble des grilles vues
    seen_boards.add(tuple(find_canonical_board(initial_board)))

    # Générer l'arbre des possibilités et évaluer chaque position
    root.expand(seen_boards)
    root.evaluate()  # Évaluer l'arborescence en utilisant Minimax

    # Trouver le meilleur coup possible à partir de la position actuelle
    best_move = root.best_move()

    # Afficher la meilleure grille possible
    if best_move:
        print(f"Meilleur coup avec une évaluation de {best_move.evaluation}:")
        print(best_move.board[:3])
        print(best_move.board[3:6])
        print(best_move.board[6:])
    else:
        print("Pas de meilleur coup, partie terminée ou aucun coup possible.")
