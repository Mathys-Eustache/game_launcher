# games_logic/mahjong/engine.py
import tkinter as tk
from board import PlateauMahjong

BG_COLOR = "#2c3e50"
TILE_W = 60
TILE_H = 72
OFFSET_X = 212
OFFSET_Y = 110
Z_SHIFT = 6  # Décalage visuel 3D entre les étages

class MahjongGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mahjong - Senior Edition")
        self.geometry("1024x768")
        self.configure(bg=BG_COLOR)

        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.plateau = PlateauMahjong()
        self.selected_tile = None
        self.hint_pair = []

        # --- BOUTONS ---
        self.btn_restart = tk.Button(
            self, text="🔄 Nouvelle Partie", font=("Arial", 16, "bold"),
            command=self.init_game, bg="#f1c40f", fg="black", padx=10, pady=5
        )
        self.btn_restart.place(x=20, y=20)

        self.btn_hint = tk.Button(
            self, text="💡 Indice", font=("Arial", 16, "bold"),
            command=self.afficher_indice, bg="#3498db", fg="black", padx=10, pady=5
        )
        self.btn_hint.place(x=240, y=20)

        self.lbl_restantes = tk.Label(
            self, text="Tuiles restantes : 144", font=("Arial", 18, "bold"),
            bg=BG_COLOR, fg="white"
        )
        self.lbl_restantes.place(relx=0.98, y=25, anchor="ne")

        self.btn_relancer_fin = tk.Button(
            self, text="🔄 Recommencer", font=("Arial", 20, "bold"),
            command=self.init_game, bg="#e74c3c", fg="white"
        )

        self.canvas.bind("<Configure>", lambda event: self.draw_board())
        self.draw_board()

    def init_game(self):
        self.btn_relancer_fin.place_forget()
        self.canvas.delete("end_ui")
        self.selected_tile = None
        self.hint_pair = []
        self.plateau = PlateauMahjong()
        self.draw_board()

    def get_tile_style(self, type_tuile):
        """Retourne (symbole, texte, couleur) ultra-lisible pour chaque tuile."""
        if type_tuile.startswith("Bambou"):
            return "🎋", type_tuile.split()[1], "#27ae60"
        elif type_tuile.startswith("Cercle"):
            return "🔵", type_tuile.split()[1], "#2980b9"
        elif type_tuile.startswith("Caractere"):
            return "🀄", type_tuile.split()[1], "#c0392b"
        elif type_tuile.startswith("Vent"):
            direction = type_tuile.split()[1][0]  # N, S, E, O
            return "🧭", direction, "#34495e"
        elif type_tuile == "Dragon Rouge":
            return "🐉", "R", "#e74c3c"
        elif type_tuile == "Dragon Vert":
            return "🐉", "V", "#2ecc71"
        elif type_tuile == "Dragon Blanc":
            return "⬜", "B", "#7f8c8d"
        return "?", "", "black"

    def get_tile_coords(self, tuile):
        """Calcule la position (x, y) centrée dynamiquement selon la taille de la fenêtre."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1:
            w, h = 1024, 768

        # La base fait 10 tuiles de large et 8 tuiles de haut
        offset_x = (w - 10 * TILE_W) / 2
        offset_y = (h - 8 * TILE_H) / 2 + 25  # +25 pour laisser la place aux boutons en haut

        x = offset_x + tuile.x * TILE_W - tuile.z * Z_SHIFT
        y = offset_y + tuile.y * TILE_H - tuile.z * Z_SHIFT
        return x, y

    def draw_board(self):
        self.canvas.delete("tile")
        tuiles_actives = [t for t in self.plateau.tuiles if t.active]
        self.lbl_restantes.config(text=f"Tuiles restantes : {len(tuiles_actives)}")

        # Tri par étage (z), puis ligne (y), puis colonne (x) pour un rendu 3D propre
        tuiles_triees = sorted(tuiles_actives, key=lambda t: (t.z, t.y, t.x))

        for t in tuiles_triees:
            x, y = self.get_tile_coords(t)
            libre = self.plateau.est_tuile_libre(t)

            # Ombre / épaisseur 3D en bas et à droite
            self.canvas.create_rectangle(
                x + 4, y + 4, x + TILE_W + 4, y + TILE_H + 4,
                fill="#7f8c8d", outline="#2c3e50", tags="tile"
            )

            # Couleur de fond et bordure selon l'état
            if t == self.selected_tile:
                bg_tile = "#fef9e7"
                outline_col = "#f1c40f"
                width = 4
            elif t in self.hint_pair:
                bg_tile = "#e8f8f5"
                outline_col = "#2ecc71"
                width = 4
            else:
                bg_tile = "#ffffff" if libre else "#d5dbdb"
                outline_col = "#2c3e50"
                width = 1

            # Face de la tuile
            self.canvas.create_rectangle(
                x, y, x + TILE_W, y + TILE_H,
                fill=bg_tile, outline=outline_col, width=width, tags="tile"
            )

            symbole, valeur, couleur = self.get_tile_style(t.type_tuile)

            # Numéro / Lettre en haut
            self.canvas.create_text(
                x + TILE_W / 2, y + 18,
                text=valeur, font=("Arial", 16, "bold"), fill=couleur, tags="tile"
            )
            # Symbole au centre-bas
            self.canvas.create_text(
                x + TILE_W / 2, y + 48,
                text=symbole, font=("Arial", 22), fill=couleur, tags="tile"
            )

    def trouver_paire_disponible(self):
        """Cherche une paire jouable sur le plateau. Retourne (t1, t2) ou None."""
        libres = [t for t in self.plateau.tuiles if t.active and self.plateau.est_tuile_libre(t)]
        for i in range(len(libres)):
            for j in range(i + 1, len(libres)):
                if libres[i].type_tuile == libres[j].type_tuile:
                    return libres[i], libres[j]
        return None

    def afficher_indice(self):
        paire = self.trouver_paire_disponible()
        if paire:
            self.hint_pair = [paire[0], paire[1]]
            self.draw_board()

    def verifier_etat_partie(self):
        tuiles_actives = [t for t in self.plateau.tuiles if t.active]
        
        if not tuiles_actives:
            self.canvas.create_rectangle(212, 284, 812, 484, fill="#27ae60", outline="white", width=4, tags="end_ui")
            self.canvas.create_text(
                512, 350,
                text="🎉 VICTOIRE ! 🎉\nToutes les tuiles ont été retirées !",
                font=("Arial", 24, "bold"), fill="white", justify="center", tags="end_ui"
            )
            self.btn_relancer_fin.place(relx=0.5, rely=0.56, anchor="center")
            return

        if not self.trouver_paire_disponible():
            self.canvas.create_rectangle(212, 284, 812, 484, fill="#34495e", outline="white", width=4, tags="end_ui")
            self.canvas.create_text(
                512, 350,
                text="Il n'y a plus de paires disponibles !\nOn mélange et on recommence ?",
                font=("Arial", 24, "bold"), fill="white", justify="center", tags="end_ui"
            )
            self.btn_relancer_fin.place(relx=0.5, rely=0.56, anchor="center")

    def on_click(self, event):
        tuiles_actives = [t for t in self.plateau.tuiles if t.active]
        # On parcourt dans l'ordre inverse du dessin pour cliquer la tuile la plus haute
        tuiles_triees = sorted(tuiles_actives, key=lambda t: (t.z, t.y, t.x), reverse=True)

        tuile_cliquee = None
        for t in tuiles_triees:
            x, y = self.get_tile_coords(t)
            if x <= event.x <= x + TILE_W and y <= event.y <= y + TILE_H:
                tuile_cliquee = t
                break

        if not tuile_cliquee:
            self.selected_tile = None
            self.draw_board()
            return

        # Si la tuile est bloquée, on ignore le clic
        if not self.plateau.est_tuile_libre(tuile_cliquee):
            return

        self.hint_pair = []  # On efface l'indice dès que le joueur clique

        if self.selected_tile is None:
            self.selected_tile = tuile_cliquee
        elif self.selected_tile == tuile_cliquee:
            self.selected_tile = None
        else:
            if self.plateau.retirer_paires(self.selected_tile, tuile_cliquee):
                self.selected_tile = None
                self.draw_board()
                self.verifier_etat_partie()
                return
            else:
                # Si les deux tuiles ne correspondent pas, on sélectionne la nouvelle
                self.selected_tile = tuile_cliquee

        self.draw_board()

if __name__ == "__main__":
    app = MahjongGame()
    app.mainloop()