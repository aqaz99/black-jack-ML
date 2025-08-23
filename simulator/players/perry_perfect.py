from game import player
from game.blackjack import Dealer
from game.cards import Deck, PlayingCard
from game.enums import Action, Suit
from game.hand import Hand
from game.player import Player


class PerryPerfect(Player):
	def __init__(self, name, starting_capital, verbose=True):
		super().__init__(name, starting_capital=starting_capital, verbose=verbose)
		self.deck = Deck()
		self.players = player
		self.hard_map = {}
		self.soft_map = {}
		self.pairs_map = {}
		self.init_maps()

	def get_possible_hand_actions(self, hand: Hand) -> Action:
		available_actions = [
			Action.Hit,
			Action.Stand,
		]

		if not hand.took_first_action: # Can't double after first deal
			available_actions.append(Action.Double)

		if self.verbose:
			hand.print_hand(self.name)
		if hand.cards[0].value == hand.cards[1].value: # Check split
			available_actions.append(Action.Split)


		# Always take higher value from dealer card, if it's an ace we take the 11. 
		# We only do this because of how it is setup below with our maps, we treat ace as 11
		choice = self.get_perfect_play(self.dealer_visible_card.value[1], hand)
		if self.verbose:
			print(f"{self.name} {choice.name}'s")
		self.action_chosen = choice
		self.action_map[choice.name] += 1
		return choice
	
	def init_maps(self):
		
		ace_value = 11
		# - Hard hands
		# (Our Hand value, dealer upcard)
		# 3-8
		for hv in range(2, 9):
			for dealer in range(2, 12):
				self.hard_map[(hv, dealer)] = Action.Hit

		# 9 
		self.hard_map[(9, 2)] = Action.Hit
		for i in range(3, 7):
			self.hard_map[(9, i)] = Action.Double
		for i in range(7, 12):
			self.hard_map[(9, i)] = Action.Hit

		# 10
		for i in range(2, 10):
			self.hard_map[(10, i)] = Action.Double
		for i in range(10, 12):
			self.hard_map[(10, i)] = Action.Hit
		
		# 11
		for i in range(2, 12):
			self.hard_map[(11, i)] = Action.Double

		# 12
		for i in range(2, 4):
			self.hard_map[(12, i)] = Action.Hit
		for i in range(4, 7):
			self.hard_map[(12, i)] = Action.Stand
		for i in range(7, 12):
			self.hard_map[(12, i)] = Action.Hit

		# 13-16
		for hv in range(13, 17):
			for dealer in range(2, 7):
				self.hard_map[(hv, dealer)] = Action.Stand
			
			for dealer in range(7, 12):
				self.hard_map[(hv, dealer)] = Action.Hit
		
		# 17 Always Stand
		for hv in range(17, 22):
			for dealer in range(2, 12):
				self.hard_map[(hv, dealer)] = Action.Stand


		# - Soft Hands
		# A,2-A,3
		for hv in range(2, 4):
			for dealer in range(2, 5):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		for hv in range(2, 4):
			for dealer in range(5, 7):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(2, 4):
			for dealer in range(7, 12):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit		

		# A,4-A,5
		for hv in range(4, 6):
			for dealer in range(2, 4):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		for hv in range(4, 6):
			for dealer in range(4, 7):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(4, 6):
			for dealer in range(7, 12):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit
		
		# A,6
		for hv in range(6, 7):
			for dealer in range(2, 3):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		for hv in range(6, 7):
			for dealer in range(3, 7):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(6, 7):
			for dealer in range(7, 12):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		# A,7
		for hv in range(7, 8):
			for dealer in range(2, 7):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Double

		for hv in range(7, 8):
			for dealer in range(7, 9):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Stand

		for hv in range(7, 8):
			for dealer in range(9, 12):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Hit

		# A,8+
		for hv in range(8, 10):
			for dealer in range(2, 12):
				self.soft_map[((hv+1,hv+ace_value), dealer)] = Action.Stand

		# - Pair hands
		# 2, 2
		for dealer in range(2, 8):
			self.pairs_map[(4, dealer)] = Action.Split
		for dealer in range(8, 12):
			self.pairs_map[(4, dealer)] = Action.Hit

		# 3, 3
		for dealer in range(2, 8):
			self.pairs_map[(6, dealer)] = Action.Split
		for dealer in range(8, 12):
			self.pairs_map[(6, dealer)] = Action.Hit

		# 4, 4
		for dealer in range(2, 5):
			self.pairs_map[(8, dealer)] = Action.Hit
		for dealer in range(5, 7):
			self.pairs_map[(8, dealer)] = Action.Split
		for dealer in range(7, 12):
			self.pairs_map[(8, dealer)] = Action.Hit

		# 5, 5
		for dealer in range(2, 10):
			self.pairs_map[(10, dealer)] = Action.Double
		for dealer in range(10, 12):
			self.pairs_map[(10, dealer)] = Action.Hit

		# 6, 6
		for dealer in range(2, 7):
			self.pairs_map[(12, dealer)] = Action.Split
		for dealer in range(7, 12):
			self.pairs_map[(12, dealer)] = Action.Hit

		# 7, 7
		for dealer in range(2, 8):
			self.pairs_map[(14, dealer)] = Action.Split
		for dealer in range(8, 12):
			self.pairs_map[(14, dealer)] = Action.Hit

		# 8, 8
		for dealer in range(2, 12):
			self.pairs_map[(16, dealer)] = Action.Split

		# 9, 9
		for dealer in range(2, 7):
			self.pairs_map[(18, dealer)] = Action.Split

		self.pairs_map[(18, 7)] = Action.Stand

		for dealer in range(8, 10):
			self.pairs_map[(18, dealer)] = Action.Split

		for dealer in range(10, 12):
			self.pairs_map[(18, dealer)] = Action.Stand

		# 10, 10
		for dealer in range(2, 12):
			self.pairs_map[(20, dealer)] = Action.Stand


		# 11, 11
		for dealer in range(2, 12):
			self.pairs_map[(2, dealer)] = Action.Split



	def get_perfect_play(self, dealer_upcard: PlayingCard, hand: Hand) -> Action:
		hand_val = hand.get_hand_value()
		if isinstance(hand_val, tuple):
			return self.soft_map[(hand_val, dealer_upcard)]
		elif not hand.took_first_action and hand.cards[0].value == hand.cards[1].value:
			return self.pairs_map[(hand_val, dealer_upcard)]
		else:
			return self.hard_map[(hand_val, dealer_upcard)]

