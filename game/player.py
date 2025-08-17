from cards import PlayingCard
from enums import Actions


class Player:
	def __init__(self, name, starting_capital):
		self.name = name
		self.cash = starting_capital
		self.hand: list[PlayingCard] = []
	
	def print_hand(self, dealer = False):
		value = [0, 0]
		hand = ""
		if dealer:
			hand = f"Dealer ({self.name}):\n  "
		else:
			hand = f"Player ({self.name}):\n  "
		for card in self.hand:
			if card.visible:
				hand += f"{card.__str__()}\n  "
				value[0] += card.value[0]
				value[1] += card.value[1]
			else:
				hand += "(Hidden Card)\n  "

		print(hand)
		if any(not card.visible for card in self.hand):
			if value[0] == value[1]:
				print("  ➝ Total:", value[0])
			else:
				print(f"  ➝ Total: ({value[0]}, {value[1]})")
		else:
			if value[0] == value[1]:
				print("  ➝ Total:", value[0])
			else:
				print(f"  ➝ Total: ({value[0]}, {value[1]})")

		
	def print_possible_actions(self):
		available_actions = [
			Actions.Hit,
			Actions.Stand,
			Actions.Double
		]

		if self.hand[0].value == self.hand[1].value: # Check split
			available_actions.append(Actions.Split)

		for action in available_actions:
			print(f"{action.value}) {action.name}")

		while True:
			try:
				choice = int(input("What would you like to do: "))
				if choice > len(available_actions):
					continue
				action = Actions(choice) 
				break
			except ValueError:
				pass