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

class EndGameState(Enum):
	Null = 0
	Win = 1
	Push = 2
	Bust = 3
	DealerWin = 4