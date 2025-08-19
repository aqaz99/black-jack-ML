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

		ace_value = 11
		action_choice = ""
		# - Hard hands

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
		for i in range(4, 7):
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


		# - Soft Hands

		soft_map = {}

		# A,2-A,3
		for hv in range(2, 4):
			for dealer in range(2, 5):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		for hv in range(2, 4):
			for dealer in range(5, 7):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(2, 4):
			for dealer in range(7, 12):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit		

		# A,4-A,5
		for hv in range(4, 6):
			for dealer in range(2, 4):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		for hv in range(4, 6):
			for dealer in range(4, 7):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(4, 6):
			for dealer in range(7, 12):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit
		
		# A,6
		for hv in range(6, 7):
			for dealer in range(2, 3):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		for hv in range(6, 7):
			for dealer in range(3, 7):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(6, 7):
			for dealer in range(7, 12):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		# A,7
		for hv in range(7, 8):
			for dealer in range(2, 7):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(7, 8):
			for dealer in range(7, 9):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Stand

		for hv in range(7, 8):
			for dealer in range(9, 12):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		# A,8+
		for hv in range(8, 10):
			for dealer in range(2, 12):
				soft_map[((hv+1,hv+ace_value), dealer)] = Action.Stand

		# - Pair hands
		pairs_map = {}

		# 2, 2
		for dealer in range(2, 8):
			pairs_map[(4, dealer)] = Action.Split
		for dealer in range(8, 12):
			pairs_map[(4, dealer)] = Action.Hit

		# 3, 3
		for dealer in range(2, 8):
			pairs_map[(6, dealer)] = Action.Split
		for dealer in range(8, 12):
			pairs_map[(6, dealer)] = Action.Hit

		# 4, 4
		for dealer in range(2, 5):
			pairs_map[(8, dealer)] = Action.Hit
		for dealer in range(5, 7):
			pairs_map[(8, dealer)] = Action.Split
		for dealer in range(7, 12):
			pairs_map[(8, dealer)] = Action.Hit

		# 5, 5
		for dealer in range(2, 10):
			pairs_map[(10, dealer)] = Action.Double
		for dealer in range(10, 12):
			pairs_map[(10, dealer)] = Action.Hit

		# 6, 6
		for dealer in range(2, 7):
			pairs_map[(12, dealer)] = Action.Split
		for dealer in range(7, 12):
			pairs_map[(12, dealer)] = Action.Hit

		# 7, 7
		for dealer in range(2, 8):
			pairs_map[(14, dealer)] = Action.Split
		for dealer in range(8, 12):
			pairs_map[(14, dealer)] = Action.Hit

		# 8, 8
		for dealer in range(2, 12):
			pairs_map[(16, dealer)] = Action.Split

		# 9, 9
		for dealer in range(2, 7):
			pairs_map[(18, dealer)] = Action.Split

		pairs_map[(18, 7)] = Action.Stand

		for dealer in range(8, 10):
			pairs_map[(18, dealer)] = Action.Split

		for dealer in range(10, 12):
			pairs_map[(18, dealer)] = Action.Stand

		# 10, 10
		for dealer in range(2, 12):
			pairs_map[(20, dealer)] = Action.Stand


		# 11, 11
		for dealer in range(2, 12):
			pairs_map[(2, dealer)] = Action.Split


		hand_val = self.get_hand_value()
		if isinstance(hand_val, tuple):
			return soft_map[(hand_val, dealer_upcard)]
		elif self.hand[0].value == self.hand[1].value:
			return pairs_map[(hand_val, dealer_upcard)]
		else:
			return hard_map[(hand_val, dealer_upcard)]

