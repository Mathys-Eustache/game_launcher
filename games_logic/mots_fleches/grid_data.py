# games_logic/mots_fleches/grid_data.py

# Grille de solution (4x4)
# '.' représente une case noire inaccessible
GRID_SOLUTION = [
    ['C', 'H', 'A', 'T'],
    ['O', '.', 'V', '.'],
    ['U', 'N', 'E', 'S'],
    ['P', '.', 'C', '.']
]

# Définitions associées aux lignes (Horizontal) et colonnes (Vertical)
# Format : (ligne, colonne): "Définition"
CLUES_HORIZONTAL = {
    (0, 0): "1 Horizontal : Félin domestique",
    (2, 0): "3 Horizontal : Articles féminins pluriels"
}

CLUES_VERTICAL = {
    (0, 0): "1 Vertical : Action de trancher",
    (0, 2): "3 Vertical : En compagnie de"
}

# Constantes de style pour l'interface
CELL_SIZE = 100
MARGIN_TOP = 150
MARGIN_LEFT = 312 # Pour centrer la grille 4x4 (1024 - 400)/2
BG_COLOR = "#2c3e50" # Bleu nuit reposant pour les yeux