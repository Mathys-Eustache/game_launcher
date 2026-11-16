# games_logic/mots_fleches/grid_generator.py
import random
import json
import os

def charger_dictionnaire():
    """Charge les mots depuis le fichier JSON externe."""
    # Trouve le chemin exact du fichier json dans le même dossier que ce script
    dossier_actuel = os.path.dirname(__file__)
    chemin_fichier = os.path.join(dossier_actuel, 'dictionnaire.json')
    
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Sécurité : si le fichier manque, on met deux mots par défaut pour ne pas faire planter le jeu
        print("⚠️ Le fichier dictionnaire.json est introuvable !")
        return {"ERREUR": "Fichier manquant", "JSON": "À créer"}

# On charge le dictionnaire massif
DICTIONNAIRE = charger_dictionnaire()

def peut_placer(grille, mot, r, c, direction, taille):
    if direction == 'H':
        if c + len(mot) > taille: return False
        for i in range(len(mot)):
            if grille[r][c+i] != '.' and grille[r][c+i] != mot[i]: return False
            if grille[r][c+i] == '.':
                if r > 0 and grille[r-1][c+i] != '.': return False
                if r < taille-1 and grille[r+1][c+i] != '.': return False
    else: 
        if r + len(mot) > taille: return False
        for i in range(len(mot)):
            if grille[r+i][c] != '.' and grille[r+i][c] != mot[i]: return False
            if grille[r+i][c] == '.':
                if c > 0 and grille[r+i][c-1] != '.': return False
                if c < taille-1 and grille[r+i][c+1] != '.': return False
    return True

def generer_nouvelle_grille(taille=8):
    grille = [['.' for _ in range(taille)] for _ in range(taille)]
    clues_h = {}
    clues_v = {}
    
    mots_dispos = list(DICTIONNAIRE.keys())
    random.shuffle(mots_dispos)
    
    if not mots_dispos:
        return grille, clues_h, clues_v

    premier_mot = mots_dispos.pop(0)
    start_r, start_c = taille//2, (taille - len(premier_mot))//2
    for i, lettre in enumerate(premier_mot):
        grille[start_r][start_c+i] = lettre
    clues_h[(start_r, start_c)] = f"➡️ Horizontal : {DICTIONNAIRE[premier_mot]}"

    for mot in mots_dispos:
        place = False
        for r in range(taille):
            for c in range(taille):
                if grille[r][c] in mot: 
                    idx = mot.index(grille[r][c])
                    
                    start_vr = r - idx
                    if start_vr >= 0 and peut_placer(grille, mot, start_vr, c, 'V', taille):
                        for i, l in enumerate(mot): grille[start_vr+i][c] = l
                        clues_v[(start_vr, c)] = f"⬇️ Vertical : {DICTIONNAIRE[mot]}"
                        place = True
                        break
                        
                    start_hc = c - idx
                    if start_hc >= 0 and peut_placer(grille, mot, r, start_hc, 'H', taille):
                        for i, l in enumerate(mot): grille[r][start_hc+i] = l
                        clues_h[(r, start_hc)] = f"➡️ Horizontal : {DICTIONNAIRE[mot]}"
                        place = True
                        break
            if place: break

    return grille, clues_h, clues_v