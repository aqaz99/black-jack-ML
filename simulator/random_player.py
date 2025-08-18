from game.enums import Actions
from game.player import Player
import random


class RandyRanom(Player):
	def get_possible_actions(self):
		available_actions = [
			Actions.Hit,
			Actions.Stand,
			
		]
		if not self.took_first_action: # Can't double after first deal
			available_actions.append(Actions.Double)

		if self.hand[0].value == self.hand[1].value: # Check split
			available_actions.append(Actions.Split)

		choice = random.choice(available_actions)
		if self.verbose:
			print(f"{self.name} {choice.name}'s")
		return choice.value