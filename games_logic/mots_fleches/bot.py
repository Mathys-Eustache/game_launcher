# games_logic/mots_fleches/bot.py
import tkinter as tk
import traceback
from engine import MotsFlechesGame

class FauxClic:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class FauxClavier:
    def __init__(self, keysym):
        self.keysym = keysym

def lancer_bot_testeur():
    app = MotsFlechesGame()
    app.title("🤖 BOT DE TEST - MOTS FLÉCHÉS (Grilles Infinies)")

    # On prépare la liste des cases dynamiques APRÈS la génération de la grille aléatoire
    cases_a_remplir = []
    for r in range(app.grid_size):
        for c in range(app.grid_size):
            if app.grid_solution[r][c] != '.':
                cases_a_remplir.append((r, c, app.grid_solution[r][c]))

    stats = {
        "lettres_placees": 0,
        "erreurs_critiques": 0,
        "tours_joues": 0,
        "total_cases": len(cases_a_remplir)
    }

    def afficher_compte_rendu():
        print("\n" + "="*50)
        print("📊 COMPTE-RENDU FINAL DU BOT TESTEUR (MOTS FLÉCHÉS)")
        print("="*50)
        print(f"🔄 Actions simulées  : {stats['tours_joues']}")
        print(f"✅ Lettres placées   : {stats['lettres_placees']} / {stats['total_cases']}")
        print(f"❌ Erreurs critiques : {stats['erreurs_critiques']}")
        
        victoire = True
        # On utilise maintenant app.grid_size pour vérifier la grille
        for r in range(app.grid_size):
            for c in range(app.grid_size):
                if app.grid_solution[r][c] != '.' and app.user_grid[r][c] != app.grid_solution[r][c]:
                    victoire = False

        if victoire:
            print("🏆 Résultat de la partie : GRILLE TERMINÉE ET VALIDÉE !")
        elif stats['erreurs_critiques'] > 0:
            print("⚠️ Résultat de la partie : INSTABLE (Des erreurs se sont produites)")
        else:
            print("🛑 Résultat de la partie : INCOMPLET")
        print("="*50 + "\n")
        
        app.quit()

    def tour_du_bot():
        if not cases_a_remplir:
            # S'il a fini, on laisse 1 seconde pour admirer l'écran de victoire puis on affiche le rapport
            app.after(1000, afficher_compte_rendu)
            return

        stats["tours_joues"] += 1
        r, c, lettre_correcte = cases_a_remplir.pop(0)

        try:
            # Le bot s'adapte automatiquement à la taille de l'écran grâce aux variables dynamiques de l'app
            clic_x = app.margin_left + (c * app.cell_size) + (app.cell_size // 2)
            clic_y = app.margin_top + (r * app.cell_size) + (app.cell_size // 2)
            app.on_click(FauxClic(clic_x, clic_y))
            
            app.on_key_press(FauxClavier(lettre_correcte))
            
            print(f"✅ [{stats['tours_joues']}] TEST RÉUSSI : Clic sur ({r},{c}) -> Lettre '{lettre_correcte}'")
            stats["lettres_placees"] += 1

        except Exception as e:
            print(f"❌ ERREUR CRITIQUE DÉTECTÉE sur la case ({r}, {c}) : {e}")
            stats["erreurs_critiques"] += 1
            traceback.print_exc()

        app.after(300, tour_du_bot)

    print("🚀 Lancement du Bot Testeur (Compatible Grilles Infinies)...")
    app.after(1000, tour_du_bot)
    app.mainloop()

if __name__ == "__main__":
    lancer_bot_testeur()