from cards import PlayingCard
from enums import Actions


class Player:
	def __init__(self, name, starting_capital):
		self.name = name
		self.cash = starting_capital
		self.hand: list[PlayingCard] = []
		self.busted = False
	
	def get_hand_value(self, get_max_value = False):
		"""Return the value of the hand. 
		If an Ace makes 2 possibilities return a tuple, otherwise a single int."""
		total_low = 0
		total_high = 0 

		for card in self.hand:
			total_low += card.value[0]
			total_high += card.value[1]

		# If the "high" value busts, downgrade it to low
		if total_high > 21:
			total_high = total_low

		# If equal, just return one int
		if total_low == total_high:
			return total_low
		else:
			if get_max_value:
				return max(total_low, total_high)
			return (total_low, total_high)
	
	def print_hand(self, dealer=False):
		"""Prints hand and current score representation."""
		title = "Dealer" if dealer else "Player"
		print(f"{title} ({self.name}):")

		for card in self.hand:
			if card.visible:
				print(f"  {card}")
			else:
				print("  (Hidden Card)")

		# If hidden card exists, only reveal partial values
		if any(not card.visible for card in self.hand):
			val = self.get_partial_value()
			print(f"  ➝ Total: {val}")
		else:
			value = self.get_hand_value()
			print(f"  ➝ Total: {value}")

		
		print("")

	def get_partial_value(self):
		"""Return value of only visible cards (used for dealer’s hidden card)."""
		total_low = 0
		total_high = 0
		for card in self.hand:
			if card.visible:
				total_low += card.value[0]
				total_high += card.value[1]

		if total_high > 21:
			total_high = total_low

		# If identical, just return int
		return total_low if total_low == total_high else (total_low, total_high)

	def get_possible_actions(self):
		choice = ""
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
		print("-"*50)	
		return choice