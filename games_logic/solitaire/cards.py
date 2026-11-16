# games_logic/solitaire/cards.py
import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit     # '♥', '♦', '♣', '♠'
        self.value = value   # 'A', '2', '3', ..., 'K'
        self.face_up = False # Par défaut, la carte est cachée

class Deck:
    def __init__(self):
        suits = ['♥', '♦', '♣', '♠']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        """Mélange les cartes."""
        random.shuffle(self.cards)

    def draw(self):
        """Tire une carte du paquet."""
        if self.cards:
            return self.cards.pop()
        return None