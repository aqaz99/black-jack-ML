from cards import PlayingCard


class Player:
	def __init__(self, name, starting_capital):
		self.name = name
		self.cash = starting_capital
		self.hand: list[PlayingCard] = []
	
	def print_hand(self):
		value = [0, 0]
		hand = f"{self.name}'s hand contains:"
		for card in self.hand:
			if card.visible:
				if hand[-1] == ":":
					hand += f" "
				else:
					hand += f", "
				hand += f"{card.__str__()}"
				value[0] += card.value[0]
				value[1] += card.value[1]
			else:
				hand += ", (Hidden Card)"


		if any(not card.visible for card in self.hand):
			if value[0] == value[1]:
				print(f"{hand} - ({value[0]})")
			else:
				print(f"{hand} - ({value[0]}, {value[1]})")
		else:
			print(f"{hand} - ({value[0]})")