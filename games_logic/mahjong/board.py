# games_logic/mahjong/board.py
import random

# Les 34 types de tuiles classiques (chacun présent 4 fois = 136 tuiles)
TUILES_TYPES = [
    f"Bambou {i}" for i in range(1, 10)
] + [
    f"Cercle {i}" for i in range(1, 10)
] + [
    f"Caractere {i}" for i in range(1, 10)
] + [
    "Vent Nord", "Vent Sud", "Vent Est", "Vent Ouest",
    "Dragon Rouge", "Dragon Vert", "Dragon Blanc"
]

class Tuile:
    def __init__(self, id_tuile, type_tuile, x, y, z):
        self.id = id_tuile
        self.type_tuile = type_tuile
        # Coordonnées 3D : x (colonne), y (ligne), z (étage)
        self.x = x  
        self.y = y  
        self.z = z  
        self.active = True # Devient False quand la tuile est retirée

class PlateauMahjong:
    def __init__(self):
        self.tuiles = []
        self.generer_plateau()

    def generer_plateau(self):
        """Génère une pyramide de 136 tuiles (adaptée et symétrique)."""
        paquet = TUILES_TYPES * 4
        random.shuffle(paquet)
        
        self.tuiles = []
        id_compteur = 0
        
        # Étage 0 (Base) : 10x8 = 80 tuiles
        for y in range(8):
            for x in range(10):
                self.tuiles.append(Tuile(id_compteur, paquet.pop(), x, y, 0))
                id_compteur += 1
                
        # Étage 1 : 8x5 = 40 tuiles (centrées)
        for y in range(1, 6):
            for x in range(1, 9):
                self.tuiles.append(Tuile(id_compteur, paquet.pop(), x, y, 1))
                id_compteur += 1
                
        # Étage 2 : 4x3 = 12 tuiles (centrées)
        for y in range(2, 5):
            for x in range(3, 7):
                self.tuiles.append(Tuile(id_compteur, paquet.pop(), x, y, 2))
                id_compteur += 1
                
        # Étage 3 (Sommet) : 2x2 = 4 tuiles
        for y in range(3, 5):
            for x in range(4, 6):
                self.tuiles.append(Tuile(id_compteur, paquet.pop(), x, y, 3))
                id_compteur += 1

    def est_tuile_libre(self, tuile):
        """
        Règle officielle du Mahjong :
        1. Aucune tuile ne doit être posée DIRECTEMENT au-dessus d'elle (z + 1).
        2. Elle doit être libre à GAUCHE (x - 1) OU à DROITE (x + 1) sur son propre étage (z).
        """
        if not tuile.active:
            return False

        bloque_dessus = False
        bloque_gauche = False
        bloque_droite = False

        for autre in self.tuiles:
            if not autre.active or autre.id == tuile.id:
                continue
                
            # Vérifie s'il y a une tuile juste au-dessus
            if autre.z == tuile.z + 1 and autre.x == tuile.x and autre.y == tuile.y:
                bloque_dessus = True
                
            # Vérifie les voisins immédiats sur le MÊME étage
            if autre.z == tuile.z and autre.y == tuile.y:
                if autre.x == tuile.x - 1:
                    bloque_gauche = True
                if autre.x == tuile.x + 1:
                    bloque_droite = True

        # Jouable si rien au-dessus ET (libre à gauche OU libre à droite)
        return not bloque_dessus and (not bloque_gauche or not bloque_droite)

    def retirer_paires(self, tuile1, tuile2):
        """Retire deux tuiles si elles sont identiques et libres."""
        if tuile1.type_tuile == tuile2.type_tuile and self.est_tuile_libre(tuile1) and self.est_tuile_libre(tuile2):
            tuile1.active = False
            tuile2.active = False
            return True
        return False