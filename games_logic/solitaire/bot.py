# games_logic/solitaire/bot.py
import tkinter as tk
import traceback
from engine import SolitaireGame

class FauxClic:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def lancer_bot_testeur():
    app = SolitaireGame()
    app.title("🤖 BOT DE TEST - SOLITAIRE (Test du message de blocage)")

    stats = {
        "mouvements_reussis": 0,
        "erreurs_critiques": 0,
        "tours_joues": 0,
        "limite_tours": 150,
        "historique": [] # Mémoire à court terme (10 coups)
    }

    def afficher_compte_rendu():
        print("\n" + "="*50)
        print("📊 COMPTE-RENDU FINAL DU BOT TESTEUR")
        print("="*50)
        print(f"🔄 Tours joués       : {stats['tours_joues']} / {stats['limite_tours']}")
        print(f"✅ Actions réussies  : {stats['mouvements_reussis']}")
        print(f"❌ Erreurs critiques : {stats['erreurs_critiques']}")
        
        victoire = all(len(f) == 13 for f in app.foundations)
        bloque = not app.has_valid_moves()
        
        if victoire:
            print("🏆 Résultat : VICTOIRE !")
        elif bloque:
            print("🛑 Résultat : PARTIE BLOQUÉE (Le pop-up doit être affiché à l'écran !)")
        else:
            print("⚠️ Résultat : ARRÊT (Limite de 150 tours atteinte)")
        print("="*50)
        print("👀 La fenêtre reste ouverte pour que tu puisses observer le plateau.\n")

    def tour_du_bot():
        mouvement_effectue = False
        stats["tours_joues"] += 1

        try:
            # TEST 1 : Retourner une carte face cachée
            if not mouvement_effectue:
                for col in range(7):
                    if app.tableaus[col] and not app.tableaus[col][-1].face_up:
                        app.tableaus[col][-1].face_up = True
                        print(f"✅ [{stats['tours_joues']}] TEST RÉUSSI : Carte retournée Tableau {col+1}")
                        mouvement_effectue = True
                        stats["historique"].clear()
                        break

            # TEST 2 : Tableau vers Fondations
            if not mouvement_effectue:
                for col in range(7):
                    if app.tableaus[col] and app.tableaus[col][-1].face_up:
                        carte = app.tableaus[col][-1]
                        for f in range(4):
                            if app.attempt_move(carte, "tableau", col, "foundation", f):
                                print(f"✅ [{stats['tours_joues']}] TEST RÉUSSI : Tableau {col+1} -> Fondation {f+1}")
                                mouvement_effectue = True
                                stats["historique"].clear()
                                break
                    if mouvement_effectue: break

            # TEST 3 : Défausse vers Fondations
            if not mouvement_effectue and app.waste:
                carte = app.waste[-1]
                for f in range(4):
                    if app.attempt_move(carte, "waste", None, "foundation", f):
                        print(f"✅ [{stats['tours_joues']}] TEST RÉUSSI : Défausse -> Fondation {f+1}")
                        mouvement_effectue = True
                        stats["historique"].clear()
                        break

            # TEST 4 : Tableau vers Tableau
            if not mouvement_effectue:
                for col_source in range(7):
                    if not app.tableaus[col_source]: continue
                    
                    idx_visible = 0
                    while idx_visible < len(app.tableaus[col_source]) and not app.tableaus[col_source][idx_visible].face_up:
                        idx_visible += 1
                        
                    if idx_visible < len(app.tableaus[col_source]):
                        carte_a_bouger = app.tableaus[col_source][idx_visible]
                        
                        if idx_visible > 0 or (idx_visible == 0 and carte_a_bouger.value != 'K' or len(app.tableaus[col_source]) > 1):
                            for col_dest in range(7):
                                if col_source != col_dest:
                                    mvt = (col_source, col_dest)
                                    if mvt not in stats["historique"][-10:]:
                                        if app.attempt_move(carte_a_bouger, "tableau", col_source, "tableau", col_dest):
                                            print(f"✅ [{stats['tours_joues']}] TEST RÉUSSI : Tableau {col_source+1} -> Tableau {col_dest+1}")
                                            mouvement_effectue = True
                                            stats["historique"].append(mvt)
                                            break
                    if mouvement_effectue: break

            # TEST 5 : Défausse vers Tableau
            if not mouvement_effectue and app.waste:
                carte = app.waste[-1]
                for col_dest in range(7):
                    if app.attempt_move(carte, "waste", None, "tableau", col_dest):
                        print(f"✅ [{stats['tours_joues']}] TEST RÉUSSI : Défausse -> Tableau {col_dest+1}")
                        mouvement_effectue = True
                        stats["historique"].clear()
                        break

            # TEST 6 : Clic sur la Pioche
            if not mouvement_effectue:
                print(f"🔄 [{stats['tours_joues']}] TEST : Pioche cliquée")
                app.on_press(FauxClic(60, 100))
                mouvement_effectue = True
                stats["historique"].clear()

            if mouvement_effectue:
                stats["mouvements_reussis"] += 1

        except Exception as e:
            print(f"❌ ERREUR CRITIQUE DÉTECTÉE : {e}")
            stats["erreurs_critiques"] += 1
            traceback.print_exc()

        # Met à jour le visuel ET affiche le pop-up si bloqué
        app.draw_board()
        app.verifier_etat_partie()
        
        victoire = all(len(f) == 13 for f in app.foundations)
        bloque = not app.has_valid_moves()
        
        # Arrêt si gagné, bloqué, ou limite atteinte
        if victoire or bloque or stats["tours_joues"] >= stats["limite_tours"]:
            afficher_compte_rendu()
        else:
            app.after(50, tour_du_bot)

    print("🚀 Lancement du Bot Testeur (150 tours max)...")
    app.after(500, tour_du_bot)
    app.mainloop()

if __name__ == "__main__":
    lancer_bot_testeur()