# games_logic/solitaire/rules.py

# L'ordre officiel des cartes du Solitaire
VALEURS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def est_rouge(suit):
    """Vérifie si la carte est de couleur rouge."""
    return suit in ['♥', '♦']

def is_valid_foundation_move(carte, fondation):
    """
    Règle pour les 4 cases en haut à droite (Fondations) :
    - Si c'est vide, il faut un As ('A').
    - Sinon, il faut le même signe et la valeur juste au-dessus.
    """
    if not fondation:
        return carte.value == 'A'
    
    carte_sommet = fondation[-1]
    
    # Doit être du même signe (ex: Cœur sur Cœur)
    if carte.suit != carte_sommet.suit:
        return False
        
    # Doit être la valeur strictement supérieure (ex: 3 sur 2)
    return VALEURS.index(carte.value) == VALEURS.index(carte_sommet.value) + 1

def is_valid_tableau_move(carte, carte_cible):
    """
    Règle pour les colonnes principales (Tableau) :
    - Si la case est vide, il faut un Roi ('K').
    - Sinon, il faut une couleur alternée (Rouge/Noir) et la valeur juste en dessous.
    """
    if carte_cible is None:
        return carte.value == 'K'
        
    # Les couleurs doivent être différentes (Rouge sur Noir, ou Noir sur Rouge)
    if est_rouge(carte.suit) == est_rouge(carte_cible.suit):
        return False
        
    # La carte posée doit être la valeur strictement inférieure (ex: 9 sur 10)
    return VALEURS.index(carte.value) == VALEURS.index(carte_cible.value) - 1