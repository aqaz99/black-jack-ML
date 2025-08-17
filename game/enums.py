from enum import Enum

class Suit(Enum):
	Clubs = 1
	Diamonds = 2
	Hearts = 3
	Spades = 4

class Actions(Enum):
	Hit = 1
	Stand = 2
	Double = 3
	Split = 4