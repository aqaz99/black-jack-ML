from enum import Enum
import random

number_card_names = {
	1: "Ace",
	2: "Two",
	3: "Three",
	4: "Four",
	5: "Five",
	6: "Six",
	7: "Seven",
	8: "Eight",
	9: "Nine",
	10: "Ten",
}
face_card_names = ["Jack", "Queen", "King"]

class Suit(Enum):
	CLUBS = 1
	DIAMONDS = 2
	HEARTS = 3
	SPADES = 4

class PlayingCard:
	def __init__(self, name, value: tuple, suit: Suit):
		self.name = name
		self.suit = suit
		self.value = value
		
		def __str__(self):
			return f"{self.name} of {self.suit}"
	


class Deck:
	def __init__(self):
		self.cards: list[PlayingCard] = []

	def shuffle(self):
		random.shuffle(self.cards)

	def reset_deck(self):
		self.cards.clear()

		for suit_val in Suit:
			for i in range(1, 14):
				if i == 1:  # Ace
					self.cards.append(PlayingCard(number_card_names[i], (1, 11), suit_val))
				elif i <= 10:  # Number
					self.cards.append(PlayingCard(number_card_names[i], (i, i), suit_val))
				else:  # Face
					self.cards.append(PlayingCard(face_card_names[i-11], (10, 10), suit_val))
					
		for card in self.cards:
			print(card)
