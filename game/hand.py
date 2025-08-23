from game.cards import PlayingCard
from game.enums import Action, EndGameHandState


class Hand:
	def __init__(self, verbose = True):
		self.cards: list[PlayingCard] = []
		self.hand_stand = False
		self.end_game_state = EndGameHandState.Null
		self.took_first_action = False
		self.verbose = verbose
		self.hand_id = 0 # Used if we ever have splits
	
	def print_hand(self, user_name: str, dealer=False):
		"""Prints hand and current score representation."""
		if not self.verbose:
			return
		title = "Dealer" if dealer else "Player"
		print(f"{title} ({user_name}):")

		for card in self.cards:
			if card.visible:
				print(f"  {card}")
			else:
				print("  (Hidden Card)")

		# If hidden card exists, only reveal partial values
		if any(not card.visible for card in self.cards):
			val = self.get_partial_hand_value()
			print(f"  ➝ Total: {val}")
		else:
			value = self.get_hand_value()
			print(f"  ➝ Total: {value}")
		
		print("")

	def get_partial_hand_value(self):
		"""Return value of only visible cards (used for dealer's hidden card)."""
		total_low = 0
		total_high = 0
		for card in self.cards:
			if card.visible:
				total_low += card.value[0]
				total_high += card.value[1]

		if total_high > 21:
			total_high = total_low

		# If identical, just return int
		return total_low if total_low == total_high else (total_low, total_high)

	def get_hand_value(self, get_max_value = False):
		"""Return the value of the hand. 
		If an Ace makes 2 possibilities return a tuple, otherwise a single int."""
		total_low = 0
		total_high = 0 

		for card in self.cards:
			total_low += card.value[0]
			total_high += card.value[1]

		# If the "high" value busts, downgrade it to low
		if total_high > 21:
			total_high = total_low
		
		# If player has 21, return it
		if max(total_low, total_high) == 21:
			return 21

		# If equal, just return one int
		if total_low == total_high:
			return total_low
		else:
			if get_max_value:
				return max(total_low, total_high)
			return (total_low, total_high)
		
	