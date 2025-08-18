from game import player
from game.cards import Deck
from game.enums import Action
from game.player import Player
import random


class RandyRanom(Player):
	def __init__(self, name, starting_capital, verbose=True):
		super().__init__(name, starting_capital=starting_capital, verbose=verbose)
		self.deck = Deck()
		self.players = player

	def get_possible_actions(self) -> Action:
		available_actions = [
			Action.Hit,
			Action.Stand,
		]
		if not self.took_first_action: # Can't double after first deal
			available_actions.append(Action.Double)

		# if self.hand[0].value == self.hand[1].value: # Check split
		# 	available_actions.append(Action.Split)

		choice = random.choice(available_actions)
		if self.verbose:
			print(f"{self.name} {choice.name}'s")
		self.action_chosen = choice
		self.action_map[choice.name] += 1
		return choice