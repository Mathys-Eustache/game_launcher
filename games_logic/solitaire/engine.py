# games_logic/solitaire/engine.py
import tkinter as tk
from cards import Deck
from rules import is_valid_tableau_move, is_valid_foundation_move

BG_COLOR = "#2c3e50"
CARD_WIDTH = 100
CARD_HEIGHT = 140

class SolitaireGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solitaire - Senior Edition")
        self.geometry("1024x768")
        self.configure(bg=BG_COLOR)
        
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.selected_card = None
        self.selected_source = None
        self.selected_source_idx = None
        self.drag_data = None 
        self.is_animating = False
        
        self.btn_restart = tk.Button(
            self, text="🔄 Nouvelle Partie", font=("Arial", 16, "bold"), 
            command=self.init_game, bg="#f1c40f", fg="black", padx=10, pady=5
        )
        self.btn_restart.place(x=20, y=20)
        
        self.btn_auto_finish = tk.Button(
            self, text="✨ Ranger automatiquement", font=("Arial", 16, "bold"),
            command=self.auto_complete_game, bg="#2ecc71", fg="black", padx=10, pady=5
        )
        
        self.btn_relancer_stuck = tk.Button(
            self, text="🔄 Recommencer", font=("Arial", 20, "bold"),
            command=self.init_game, bg="#e74c3c", fg="white"
        )
        
        self.init_game()
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def init_game(self):
        self.btn_auto_finish.place_forget()
        self.btn_relancer_stuck.place_forget()
        self.canvas.delete("stuck_ui")
        self.is_animating = False
        self.selected_card = None
        self.drag_data = None
        
        self.full_deck = Deck()
        self.full_deck.shuffle()
        
        self.foundations = [[], [], [], []]
        self.tableaus = [[], [], [], [], [], [], []]
        self.deck = []
        self.waste = []
        
        for i in range(7):
            for j in range(i + 1):
                carte = self.full_deck.draw()
                if j == i:
                    carte.face_up = True 
                else:
                    carte.face_up = False
                self.tableaus[i].append(carte)
                
        while self.full_deck.cards:
            self.deck.append(self.full_deck.draw())
            
        self.draw_board()

    def draw_board(self):
        if self.is_animating: return 
        self.canvas.delete("card")
        
        dragged_cards = []
        if self.drag_data and self.drag_data.get("active"):
            dragged_cards = self.drag_data["cards"]
            
        y_top = 90
        
        for i in range(4):
            x = 400 + i * (CARD_WIDTH + 20)
            self.canvas.create_rectangle(x, y_top, x + CARD_WIDTH, y_top + CARD_HEIGHT, outline="white", tags="card")
            if self.foundations[i] and self.foundations[i][-1] not in dragged_cards:
                self.draw_card(self.foundations[i][-1], x, y_top)
                
        x_deck = 50
        self.canvas.create_rectangle(x_deck, y_top, x_deck + CARD_WIDTH, y_top + CARD_HEIGHT, outline="white", tags="card")
        if self.deck:
            self.draw_card(self.deck[-1], x_deck, y_top)
            
        x_waste = 180
        if self.waste and self.waste[-1] not in dragged_cards:
            self.draw_card(self.waste[-1], x_waste, y_top)
            
        for i, colonne in enumerate(self.tableaus):
            x = 100 + i * (CARD_WIDTH + 20)
            y_carte = 260
            
            self.canvas.create_rectangle(x, y_carte, x + CARD_WIDTH, y_carte + CARD_HEIGHT, outline="gray", tags="card")
            
            for carte in colonne:
                if carte not in dragged_cards:
                    self.draw_card(carte, x, y_carte)
                y_carte += 40 if carte.face_up else 15

    def draw_card(self, carte, x, y, tags="card"):
        est_selectionnee = (self.selected_card == carte)
        couleur_bord = "yellow" if est_selectionnee else "black"
        epaisseur = 5 if est_selectionnee else 1

        if not carte.face_up:
            self.canvas.create_rectangle(x, y, x + CARD_WIDTH, y + CARD_HEIGHT, fill="#2980b9", outline="white", width=3, tags=tags)
            self.canvas.create_text(x + CARD_WIDTH/2, y + CARD_HEIGHT/2, text="🌟", font=("Arial", 40), fill="white", tags=tags)
        else:
            self.canvas.create_rectangle(x, y, x + CARD_WIDTH, y + CARD_HEIGHT, fill="white", outline=couleur_bord, width=epaisseur, tags=tags)
            color = "red" if carte.suit in ['♥', '♦'] else "black"
            
            # --- CORRECTION EXACTE : Chiffre et symbole côte à côte ---
            # La marge gauche est réduite, la police agrandie, et on supprime le \n
            self.canvas.create_text(
                x + 5, y + 5, 
                text=f"{carte.value} {carte.suit}", 
                font=("Arial", 22, "bold"), 
                fill=color, 
                anchor="nw", 
                tags=tags
            )
            
            # Le gros symbole central, abaissé légèrement pour équilibrer la carte
            self.canvas.create_text(
                x + CARD_WIDTH/2, y + CARD_HEIGHT/2 + 15, 
                text=carte.suit, 
                font=("Arial", 50), 
                fill=color, 
                anchor="center",
                tags=tags
            )

    def has_valid_moves(self):
        if self.deck: return True
        for col in self.tableaus:
            if col and not col[-1].face_up: return True
        if self.waste:
            carte = self.waste[-1]
            for f in self.foundations:
                if is_valid_foundation_move(carte, f): return True
            for col in self.tableaus:
                cible = col[-1] if col else None
                if is_valid_tableau_move(carte, cible): return True
        for src_idx, col in enumerate(self.tableaus):
            if not col: continue
            for f in self.foundations:
                if is_valid_foundation_move(col[-1], f): return True
            for j, carte in enumerate(col):
                if carte.face_up:
                    for dest_idx, dest_col in enumerate(self.tableaus):
                        if src_idx != dest_idx:
                            cible = dest_col[-1] if dest_col else None
                            if is_valid_tableau_move(carte, cible):
                                if j == 0 and carte.value == 'K' and not cible: continue
                                return True
        return False

    def verifier_etat_partie(self):
        cartes_cachees = any(not carte.face_up for colonne in self.tableaus for carte in colonne)
        if not cartes_cachees and not self.deck and not self.waste:
            self.btn_auto_finish.place(relx=0.5, rely=0.9, anchor="center")
            return
        if not self.has_valid_moves():
            self.canvas.create_rectangle(212, 284, 812, 484, fill="#34495e", outline="white", width=4, tag="stuck_ui")
            self.canvas.create_text(
                512, 350, 
                text="Il n'y a plus de cartes à jouer !\nOn mélange et on recommence ?", 
                font=("Arial", 24, "bold"), fill="white", justify="center",
                tag="stuck_ui"
            )
            self.btn_relancer_stuck.place(relx=0.5, rely=0.56, anchor="center")

    def get_card_at_pos(self, event_x, event_y):
        if 180 <= event_x <= 180 + CARD_WIDTH and 90 <= event_y <= 90 + CARD_HEIGHT and self.waste:
            return "waste", None, self.waste[-1], 180, 90
        for i in range(4):
            fx = 400 + i * (CARD_WIDTH + 20)
            if fx <= event_x <= fx + CARD_WIDTH and 90 <= event_y <= 90 + CARD_HEIGHT and self.foundations[i]:
                return "foundation", i, self.foundations[i][-1], fx, 90
        for i, colonne in enumerate(self.tableaus):
            tx = 100 + i * (CARD_WIDTH + 20)
            if tx <= event_x <= tx + CARD_WIDTH:
                y_carte = 260
                y_positions = []
                for c in colonne:
                    y_positions.append(y_carte)
                    y_carte += 40 if c.face_up else 15
                for j in reversed(range(len(colonne))):
                    cy = y_positions[j]
                    if cy <= event_y <= cy + CARD_HEIGHT:
                        return "tableau", i, colonne[j], tx, cy
        return None, None, None, 0, 0

    def get_drop_target(self, x, y):
        if 50 <= y <= 240:
            for i in range(4):
                fx = 400 + i * (CARD_WIDTH + 20)
                if fx - 20 <= x <= fx + CARD_WIDTH + 20: 
                    return "foundation", i
        if y >= 200:
            for i in range(7):
                tx = 100 + i * (CARD_WIDTH + 20)
                if tx - 20 <= x <= tx + CARD_WIDTH + 20:
                    return "tableau", i
        return None, None

    def attempt_move(self, card_to_move, src, src_idx, dest, dest_idx):
        moved = False
        cards_to_move = [card_to_move]
        if src == "tableau":
            col = self.tableaus[src_idx]
            cards_to_move = col[col.index(card_to_move):]
        if dest == "foundation":
            if len(cards_to_move) == 1 and is_valid_foundation_move(card_to_move, self.foundations[dest_idx]):
                self.foundations[dest_idx].append(card_to_move)
                moved = True
        elif dest == "tableau":
            cible = self.tableaus[dest_idx][-1] if self.tableaus[dest_idx] else None
            if is_valid_tableau_move(card_to_move, cible):
                self.tableaus[dest_idx].extend(cards_to_move)
                moved = True
        if moved:
            if src == "waste": self.waste.pop()
            elif src == "foundation": self.foundations[src_idx].pop()
            elif src == "tableau":
                col = self.tableaus[src_idx]
                del col[col.index(card_to_move):]
        return moved

    def on_press(self, event):
        if self.is_animating: return
        self.drag_data = None
        if 50 <= event.x <= 50 + CARD_WIDTH and 90 <= event.y <= 90 + CARD_HEIGHT:
            self.selected_card = None 
            if self.deck:
                carte = self.deck.pop()
                carte.face_up = True
                self.waste.append(carte)
            elif self.waste:
                self.deck = self.waste[::-1]
                self.waste = []
                for c in self.deck: c.face_up = False
            self.draw_board()
            self.verifier_etat_partie()
            return
        src, idx, card, cx, cy = self.get_card_at_pos(event.x, event.y)
        if src == "tableau" and card and not card.face_up:
            if self.tableaus[idx][-1] == card:
                card.face_up = True
                self.selected_card = None
                self.draw_board()
                self.verifier_etat_partie()
            return
        if self.selected_card:
            drop_src, drop_idx = self.get_drop_target(event.x, event.y)
            if drop_src:
                if self.attempt_move(self.selected_card, self.selected_source, self.selected_source_idx, drop_src, drop_idx):
                    self.selected_card = None
                    self.draw_board()
                    self.verifier_etat_partie()
                    return
            self.selected_card = None
            self.draw_board()
        if card and card.face_up:
            cards = [card]
            if src == "tableau":
                col = self.tableaus[idx]
                cards = col[col.index(card):]
            self.drag_data = {
                "source": src, "idx": idx, "card": card, "cards": cards,
                "start_x": cx, "start_y": cy,
                "offset_x": event.x - cx, "offset_y": event.y - cy,
                "active": False
            }

    def on_drag(self, event):
        if not self.drag_data: return
        if not self.drag_data["active"]:
            self.drag_data["active"] = True
            self.selected_card = None
            self.draw_board() 
        self.canvas.delete("dragged")
        cur_x = event.x - self.drag_data["offset_x"]
        cur_y = event.y - self.drag_data["offset_y"]
        for i, carte in enumerate(self.drag_data["cards"]):
            self.draw_card(carte, cur_x, cur_y + (i * 40), tags="dragged")

    def on_release(self, event):
        if not self.drag_data: return
        if self.drag_data["active"]:
            self.canvas.delete("dragged")
            drop_src, drop_idx = self.get_drop_target(event.x, event.y)
            if drop_src:
                self.attempt_move(self.drag_data["card"], self.drag_data["source"], self.drag_data["idx"], drop_src, drop_idx)
            self.drag_data = None
            self.draw_board()
            self.verifier_etat_partie()
        else:
            self.selected_card = self.drag_data["card"]
            self.selected_source = self.drag_data["source"]
            self.selected_source_idx = self.drag_data["idx"]
            self.drag_data = None
            self.draw_board()

    def auto_complete_game(self):
        if self.is_animating: return
        self.btn_auto_finish.place_forget() 
        mouvement_fait = False
        for col_idx, colonne in enumerate(self.tableaus):
            if colonne:
                carte = colonne[-1]
                for fond_idx, fondation in enumerate(self.foundations):
                    if is_valid_foundation_move(carte, fondation):
                        self.foundations[fond_idx].append(self.tableaus[col_idx].pop())
                        mouvement_fait = True
                        self.draw_board()
                        break
            if mouvement_fait: break
        if mouvement_fait:
            self.after(200, self.auto_complete_game)
        else:
            self.canvas.create_text(512, 384, text="🎉 VICTOIRE ! 🎉", font=("Arial", 50, "bold"), fill="yellow")

if __name__ == "__main__":
    app = SolitaireGame()
    app.mainloop()