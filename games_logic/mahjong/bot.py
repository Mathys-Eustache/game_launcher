# games_logic/mahjong/bot.py
import traceback
from engine import MahjongGame, TILE_W, TILE_H

class FauxClic:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def lancer_bot_mahjong():
    app = MahjongGame()
    app.title("🤖 BOT DE TEST - MAHJONG")

    stats = {
        "paires_retirees": 0,
        "erreurs_critiques": 0
    }

    def afficher_compte_rendu():
        restantes = len([t for t in app.plateau.tuiles if t.active])
        print("\n" + "=" * 50)
        print("📊 COMPTE-RENDU FINAL DU BOT MAHJONG")
        print("=" * 50)
        print(f"✅ Paires retirées   : {stats['paires_retirees']}")
        print(f"🀄 Tuiles restantes  : {restantes}")
        print(f"❌ Erreurs critiques : {stats['erreurs_critiques']}")

        if restantes == 0:
            print("🏆 Résultat : VICTOIRE ! (Le pop-up vert doit être affiché)")
        else:
            print("🛑 Résultat : PARTIE BLOQUÉE (Le pop-up de blocage doit être affiché)")
        print("=" * 50)
        print("👀 La fenêtre reste ouverte pour observer le résultat.\n")

    def tour_du_bot():
        try:
            paire = app.trouver_paire_disponible()

            if not paire:
                afficher_compte_rendu()
                return

            t1, t2 = paire

            # Simule un vrai clic sur la première tuile
            x1, y1 = app.get_tile_coords(t1)
            app.on_click(FauxClic(x1 + TILE_W / 2, y1 + TILE_H / 2))

            # Simule un vrai clic sur la deuxième tuile
            x2, y2 = app.get_tile_coords(t2)
            app.on_click(FauxClic(x2 + TILE_W / 2, y2 + TILE_H / 2))

            stats["paires_retirees"] += 1
            print(f"✅ [{stats['paires_retirees']}] Paire retirée : {t1.type_tuile}")

        except Exception as e:
            print(f"❌ ERREUR CRITIQUE DÉTECTÉE : {e}")
            stats["erreurs_critiques"] += 1
            traceback.print_exc()

        # Vérifie si la partie continue
        restantes = len([t for t in app.plateau.tuiles if t.active])
        if restantes == 0 or not app.trouver_paire_disponible():
            afficher_compte_rendu()
        else:
            app.after(150, tour_du_bot)

    print("🚀 Lancement du Bot Testeur Mahjong...")
    app.after(500, tour_du_bot)
    app.mainloop()

if __name__ == "__main__":
    lancer_bot_mahjong()