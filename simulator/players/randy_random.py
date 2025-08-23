from game import player
from game.cards import Deck
from game.enums import Action
from game.hand import Hand
from game.player import Player
import random


class RandyRandom(Player):
	def __init__(self, name, starting_capital, verbose=True):
		super().__init__(name, starting_capital=starting_capital, verbose=verbose)
		self.deck = Deck()
		self.players = player

	def get_possible_hand_actions(self, hand: Hand) -> Action:
		available_actions = [
			Action.Hit,
			Action.Stand,
		]

		if not hand.took_first_action: # Can't double after first deal
			available_actions.append(Action.Double)

		if hand.cards[0].value == hand.cards[1].value: # Check split
			available_actions.append(Action.Split)

		choice = random.choice(available_actions)
		if self.verbose:
			print(f"{self.name} {choice.name}'s")
		self.action_chosen = choice
		self.action_map[choice.name] += 1
		return choice