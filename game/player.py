from cards import PlayingCard


class Player:
	def __init__(self, name, starting_capital):
		self.name = name
		self.cash = starting_capital
		self.hand: list[PlayingCard] = []
	
	def print_hand(self):
		hand = f"{self.name}'s hand contains: "
		for card in self.hand:
			hand += card.__str__()

		print(hand)