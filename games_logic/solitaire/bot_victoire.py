# games_logic/solitaire/bot_victoire.py
import tkinter as tk
from engine import SolitaireGame
from cards import Card

def forcer_victoire():
    app = SolitaireGame()
    app.title("🏆 BOT DE TEST - VICTOIRE COMPLÈTE")

    # 1. On vide complètement le plateau de base
    app.deck = []
    app.waste = []
    app.tableaus = [[], [], [], [], [], [], []]
    app.foundations = [[], [], [], []]

    # 2. On remplit les 4 fondations de l'As jusqu'à la Dame (Q)
    valeurs = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q']
    symboles = ['♥', '♦', '♣', '♠']

    for i, symbole in enumerate(symboles):
        for val in valeurs:
            c = Card(symbole, val)
            c.face_up = True
            app.foundations[i].append(c)

    # 3. On place les 4 Rois restants sur le tableau
    for i, symbole in enumerate(symboles):
        c = Card(symbole, 'K')
        c.face_up = True
        app.tableaus[i].append(c)

    app.draw_board()

    def finir_la_partie():
        mouvement = False
        
        # Le bot cherche un Roi et le déplace dans sa fondation
        for col in range(4):
            if app.tableaus[col]:
                carte = app.tableaus[col][-1]
                if app.attempt_move(carte, "tableau", col, "foundation", col):
                    print(f"✅ Le bot a rangé le Roi de {carte.suit} !")
                    mouvement = True
                    break
        
        app.draw_board()
        
        # Vérifie si les 4 fondations sont pleines (13 cartes chacune)
        if all(len(f) == 13 for f in app.foundations):
            print("\n🏆 VICTOIRE COMPLÈTE DÉTECTÉE !")
            app.canvas.create_text(512, 384, text="🎉 VICTOIRE ! 🎉", font=("Arial", 50, "bold"), fill="yellow")
        elif mouvement:
            # On continue de jouer 1 seconde plus tard
            app.after(1000, finir_la_partie)

    print("🚀 Lancement du Bot Victoire (Il va ranger les 4 Rois restants)...")
    app.after(1000, finir_la_partie)
    app.mainloop()

if __name__ == "__main__":
    forcer_victoire()