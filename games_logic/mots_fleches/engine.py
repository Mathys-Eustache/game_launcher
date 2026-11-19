# games_logic/mots_fleches/engine.py
import tkinter as tk
from grid_generator import generer_nouvelle_grille

BG_COLOR = "#2c3e50"

class MotsFlechesGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mots Fléchés - Grilles Infinies")
        self.geometry("1024x768")
        self.configure(bg=BG_COLOR)
        
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.btn_menu = tk.Button(
            self, text="🏠 Menu", font=("Arial", 16, "bold"),
            command=self.destroy, bg="#e74c3c", fg="black",
            activebackground="#c0392b", activeforeground="white",
            highlightbackground="#e74c3c", padx=12, pady=6
        )
        self.btn_menu.place(relx=0.98, y=20, anchor="ne")
        self.btn_menu.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # --- CRÉATION DES 3 BOUTONS ---
        self.btn_restart = tk.Button(
            self, text="⏩ Nouvelle Grille", font=("Arial", 16, "bold"), 
            command=self.init_game, bg="#f1c40f", fg="black", padx=10, pady=5
        )
        self.btn_reveal_letter = tk.Button(
            self, text="💡 Révéler la case", font=("Arial", 16, "bold"), 
            command=self.reveal_letter, bg="#3498db", fg="black", padx=10, pady=5
        )
        self.btn_reveal_word = tk.Button(
            self, text="👁️ Révéler le mot", font=("Arial", 16, "bold"), 
            command=self.reveal_word, bg="#9b59b6", fg="black", padx=10, pady=5
        )
        
        self.grid_size = 8
        self.cell_size = 80
        self.margin_top = 120
        self.margin_left = (1024 - (self.grid_size * self.cell_size)) // 2
        
        self.init_game()
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<Key>", self.on_key_press)
        self.bind("<Configure>", self.on_resize)
        self.focus_force()

    def on_resize(self, event):
        if event.widget == self:
            self.draw_board()

    def init_game(self):
        self.grid_solution, self.clues_h, self.clues_v = generer_nouvelle_grille(self.grid_size)
        self.user_grid = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.selected_r = None
        self.selected_c = None
        self.direction = 'H' 
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        
        largeur_fenetre = self.winfo_width()
        if largeur_fenetre < 100: largeur_fenetre = 1024
            
        self.margin_left = (largeur_fenetre - (self.grid_size * self.cell_size)) // 2
        
        # Placement dynamique des boutons en bas de l'écran
        self.btn_restart.place(x=20, rely=0.9)
        self.btn_reveal_letter.place(relx=0.5, rely=0.9, anchor="center")
        self.btn_reveal_word.place(relx=0.98, rely=0.9, anchor="e")
        
        clue_text = "Cliquez sur une case blanche pour jouer"
        if self.selected_r is not None and self.selected_c is not None:
            clue_text = self.get_active_clue(self.selected_r, self.selected_c, self.direction)
            
        self.canvas.create_text(
            largeur_fenetre / 2, 50, text=clue_text, font=("Arial", 28, "bold"), 
            fill="yellow", justify="center", width=largeur_fenetre - 100
        )
        
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x1 = self.margin_left + c * self.cell_size
                y1 = self.margin_top + r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.grid_solution[r][c] == '.':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
                else:
                    bg_color = "white"
                    if self.is_in_active_word(r, c): bg_color = "#add8e6"
                    if r == self.selected_r and c == self.selected_c: bg_color = "yellow"
                        
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="black", width=2)
                    
                    letter = self.user_grid[r][c]
                    if letter:
                        self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=letter, font=("Arial", 36, "bold"))

    # --- NOUVELLES FONCTIONS D'AIDE ---
    
    def reveal_letter(self):
        """Révèle la lettre de la case actuellement sélectionnée."""
        if self.selected_r is not None and self.selected_c is not None:
            lettre_correcte = self.grid_solution[self.selected_r][self.selected_c]
            if lettre_correcte != '.':
                self.user_grid[self.selected_r][self.selected_c] = lettre_correcte
                self.move_selection(forward=True)
                self.draw_board()
                self.check_victory()

    def reveal_word(self):
        """Révèle toutes les lettres du mot actuellement en surbrillance bleue."""
        if self.selected_r is None or self.selected_c is None: return
        
        start_r, start_c = self.get_start_of_word(self.selected_r, self.selected_c, self.direction)
        r, c = start_r, start_c
        
        # Parcourt le mot jusqu'à trouver une case noire ou la fin de la grille
        while 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.grid_solution[r][c] != '.':
            self.user_grid[r][c] = self.grid_solution[r][c]
            if self.direction == 'H': c += 1
            else: r += 1
            
        self.draw_board()
        self.check_victory()

    # --- MÉCANIQUES EXISTANTES ---

    def on_click(self, event):
        c = (event.x - self.margin_left) // self.cell_size
        r = (event.y - self.margin_top) // self.cell_size
        
        if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
            if self.grid_solution[r][c] != '.':
                if self.selected_r == r and self.selected_c == c:
                    self.direction = 'V' if self.direction == 'H' else 'H'
                else:
                    self.selected_r = r
                    self.selected_c = c
                    if self.get_start_of_word(r, c, 'H') in self.clues_h:
                        self.direction = 'H'
                    else:
                        self.direction = 'V'
                self.draw_board()

    def on_key_press(self, event):
        if self.selected_r is None or self.selected_c is None: return
        char = event.keysym.upper()
        
        if len(char) == 1 and char.isalpha():
            self.user_grid[self.selected_r][self.selected_c] = char
            self.move_selection(forward=True)
            self.draw_board()
            self.check_victory()
            
        elif event.keysym == "BackSpace":
            self.user_grid[self.selected_r][self.selected_c] = ''
            self.move_selection(forward=False)
            self.draw_board()

    def move_selection(self, forward=True):
        step = 1 if forward else -1
        if self.direction == 'H':
            next_c = self.selected_c + step
            if 0 <= next_c < self.grid_size and self.grid_solution[self.selected_r][next_c] != '.':
                self.selected_c = next_c
        else:
            next_r = self.selected_r + step
            if 0 <= next_r < self.grid_size and self.grid_solution[next_r][self.selected_c] != '.':
                self.selected_r = next_r

    def get_start_of_word(self, r, c, direction):
        if direction == 'H':
            while c > 0 and self.grid_solution[r][c-1] != '.': c -= 1
        else:
            while r > 0 and self.grid_solution[r-1][c] != '.': r -= 1
        return (r, c)

    def is_in_active_word(self, r, c):
        if self.selected_r is None or self.selected_c is None: return False
        start_r, start_c = self.get_start_of_word(self.selected_r, self.selected_c, self.direction)
        check_r, check_c = self.get_start_of_word(r, c, self.direction)
        if self.direction == 'H' and r == self.selected_r and start_c == check_c: return True
        if self.direction == 'V' and c == self.selected_c and start_r == check_r: return True
        return False

    def get_active_clue(self, r, c, direction):
        start_pos = self.get_start_of_word(r, c, direction)
        if direction == 'H' and start_pos in self.clues_h: return self.clues_h[start_pos]
        elif direction == 'V' and start_pos in self.clues_v: return self.clues_v[start_pos]
        
        other_dir = 'V' if direction == 'H' else 'H'
        other_pos = self.get_start_of_word(r, c, other_dir)
        if other_dir == 'H' and other_pos in self.clues_h:
            self.direction = 'H'
            return self.clues_h[other_pos]
        elif other_dir == 'V' and other_pos in self.clues_v:
            self.direction = 'V'
            return self.clues_v[other_pos]
        return "Pas de définition"

    def check_victory(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid_solution[r][c] != '.' and self.user_grid[r][c] != self.grid_solution[r][c]:
                    return
        self.show_victory_screen()

    def show_victory_screen(self):
        self.canvas.delete("all")
        self.btn_restart.place_forget()
        self.btn_reveal_letter.place_forget()
        self.btn_reveal_word.place_forget()
        self.canvas.create_text(512, 300, text="🎉 FÉLICITATIONS ! 🎉\n\nGrille terminée !", font=("Arial", 40, "bold"), fill="yellow", justify="center")
        btn_replay = tk.Button(self, text="Générer une nouvelle grille", font=("Arial", 24, "bold"), bg="white", fg="black", command=self.init_game)
        btn_replay.place(relx=0.5, rely=0.6, anchor="center")

if __name__ == "__main__":
    app = MotsFlechesGame()
    app.mainloop()