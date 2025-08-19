from game import player
from game.blackjack import Dealer
from game.cards import Deck, PlayingCard
from game.enums import Action, Suit
from game.player import Player
import random


class PerryPerfect(Player):
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



		if self.verbose:
			print(f"{self.name} {choice.name}'s")
		self.action_chosen = choice
		self.action_map[choice.name] += 1
		return choice
	

	def get_perfect_play(self, dealer_upcard) -> Action:

		action_choice = ""
		# (Our Hand value, dealer upcard)
		hard_map = {}
		# 3-8
		for hv in range(2, 9):
			for dealer in range(2, 12):
				hard_map[(hv, dealer)] = Action.Hit

		# 9 
		hard_map[(9, 2)] = Action.Hit
		for i in range(3, 7):
			hard_map[(9, i)] = Action.Double
		for i in range(7, 12):
			hard_map[(9, i)] = Action.Hit

		# 10
		for i in range(2, 10):
			hard_map[(10, i)] = Action.Double
		for i in range(10, 12):
			hard_map[(10, i)] = Action.Hit
		
		# 11
		for i in range(2, 12):
			hard_map[(11, i)] = Action.Double

		# 12
		for i in range(2, 4):
			hard_map[(12, i)] = Action.Hit
		for i in range(3, 7):
			hard_map[(12, i)] = Action.Stand
		for i in range(7, 12):
			hard_map[(12, i)] = Action.Hit

		# 13-16
		for hv in range(13, 17):
			for dealer in range(2, 7):
				hard_map[(hv, dealer)] = Action.Stand
			
			for dealer in range(7, 12):
				hard_map[(hv, dealer)] = Action.Hit
		
		# 17 Always Stand
		for hv in range(17, 22):
			for dealer in range(2, 12):
				hard_map[(hv, dealer)] = Action.Stand


		action_choice = hard_map[(self.get_hand_value(), dealer_upcard)]

		soft_map = {

		}
		pairs_map = {

		}

		return action_choice