from game.cards import Deck, PlayingCard
from game.hand import Hand
from game.player import Player
from game.enums import Action, EndGameHandState

# What if player gets blackjack at same time as deal
# What if split is a blackjack
# Run command: python3 -m game.blackjack


# Dealer / GameManager 
# Runs game loop, deals cards, etc
class Dealer(Player):
	def __init__(self, name, players: list[Player], verbose = True):
		super().__init__(name, starting_capital=0, verbose=verbose)
		self.deck = Deck()
		self.verbose = verbose
		self.players = players

	def deal_card(self, recieving_hand: Hand, visible = True):
		card = self.deck.remove_card()
		card.visible = visible
		recieving_hand.cards.append(card)
	
	
	def shuffle_deck(self):
		self.deck.reset_deck()
	
	def betting_period(self):
		pass

	def dealing_period(self):
		# Don't need to refresh deck everytime, just for now
		self.shuffle_deck()
		dealer_card_visible = True
		while len(self.hands[0].cards) < 2:
			for player in self.players:
				self.deal_card(player.hands[0])
			self.deal_card(self.hands[0], dealer_card_visible)
			if dealer_card_visible: # Add first card to all players visiblity
				for player in self.players:
					player.dealer_visible_card = self.hands[0].cards[0]
			dealer_card_visible = False
		
		for player in self.players:
			if player.hands[0].get_hand_value(True) == 21:
				if self.verbose:
					self.hands[0].print_hand(self.name,True)
					player.hands[0].print_hand(player.name)
					print(f"{player.name} gets a blackjack!")
				player.hands[0].end_game_state = EndGameHandState.Win
				return True
		return False
	
	def final_dealing_period_for_dealer(self):
		dealer_hand_value = self.hands[0].get_hand_value()
		if type(dealer_hand_value) == tuple: # Has an ace
			# Should hit on soft 17
			if dealer_hand_value == (6, 17) or (dealer_hand_value[0] < 17 and dealer_hand_value[1] < 17):
				self.deal_card(self.hands[0])
				if self.verbose:
					print("------------------ Dealer Hits -------------------")
					self.hands[0].print_hand(self.name, True)
				self.final_dealing_period_for_dealer()
				return
			
			dealer_hand_value = max(dealer_hand_value[0], dealer_hand_value[1])

		else: # No ace
			if(dealer_hand_value < 17):
				self.deal_card(self.hands[0])
				if self.verbose:
					print("------------------ Dealer Hits -------------------")
					self.hands[0].print_hand(self.name, True)
				self.final_dealing_period_for_dealer()
				return

		if dealer_hand_value > 21:
			for player in self.players:
				for hand in player.hands:
					if hand.end_game_state == EndGameHandState.Null:
						hand.end_game_state = EndGameHandState.Win
		else:
			for player in self.players:
				for hand in player.hands:
					if dealer_hand_value > hand.get_hand_value(True) and hand.end_game_state != EndGameHandState.Bust:
						hand.end_game_state = EndGameHandState.DealerWin
					elif dealer_hand_value == hand.get_hand_value(True):
						hand.end_game_state = EndGameHandState.Push
					else:
						hand.end_game_state = EndGameHandState.Win


	def play_individual_player_hands(self, player: Player):
		# Need to figure out how to display hands that win or lose after standing after a split. 
		# make it smart so it works also when we don't split

		for hand in player.hands: # While each hand isn't done we continue
			if not hand.hand_stand and hand.end_game_state == EndGameHandState.Null:
				# If it was a split hand, less than two cards, need to deal more
				if self.verbose:
					self.hands[0].print_hand(self.name, True)

				if len(hand.cards) < 2:
					self.deal_card(hand)
				if self.verbose:
					hand.print_hand(player.name)
					print("-"*50)
				
				action = player.get_possible_hand_actions(hand)
				if action == Action.Hit:
					self.apply_card_action(player, hand=hand)
					hand_value = hand.get_hand_value(True) # Get Max value if user has ace
					if (isinstance(hand_value, tuple) and 21 in hand_value) or hand_value == 21:
						continue
					# If bust, also continue
					if (isinstance(hand_value, tuple) and min(hand_value) > 21) or (not isinstance(hand_value, tuple) and hand_value > 21):
						hand.end_game_state = EndGameHandState.Bust
						continue
					if hand_value < 21:
						self.play_individual_player_hands(player)
				elif action == Action.Double:
					self.apply_card_action(player, hand=hand)
				elif action == Action.Stand:
					hand.hand_stand = True
				elif action == Action.Split:
					# Delete the hand that existed (use hand id) then add two new hands
					card1, card2 = hand.cards[0], hand.cards[1]

					player.hands.remove(hand)
					
					new_hand1 = Hand()
					new_hand1.cards.append(card1)

					new_hand2 = Hand()
					new_hand2.cards.append(card2)


					player.hands.append(new_hand1)
					player.hands.append(new_hand2)

					self.play_individual_player_hands(player)


	def playing_period(self):
		for player in self.players:
			self.play_individual_player_hands(player)

	def apply_card_action(self, player: Player, hand: Hand):
		"""Helper to deal, print, and handle busting logic."""
		hand.took_first_action = True
		self.deal_card(hand)
		# self.hands[0].print_hand(self.name, True)

		hand_value = hand.get_hand_value()
		if isinstance(hand_value, tuple):
			# collect all values in the tuple that are non-busted
			value = max([v for v in hand_value if v <= 21], default=min(hand_value))
		else:
			value = hand_value

		if value > 21:
			hand.end_game_state = EndGameHandState.Bust


	def cleanup_period(self):
		pass
	
	def print_all_hand_results(self):
		if self.verbose:
			print("-"*50)
			print("-"*19, "Round Over", "-"*19)
		for player in self.players:
			for index, hand in enumerate(player.hands):
				if self.verbose:
					print("-"*50)
					self.hands[0].print_hand(self.name, True, True)
				end_output = ""
				if hand.end_game_state == EndGameHandState.DealerWin:
					end_output = f"{index}) Dealer beats {player.name}"
				else:
					end_output = f"{index}) {player.name} {'Pushes' if hand.end_game_state == EndGameHandState.Push else hand.end_game_state.name+'s'}"
				padding_count = 48 - len(end_output)
				if self.verbose:
					hand.print_hand(player.name)
					print(f"{'-'*(padding_count//2)} {end_output} {'-'*(padding_count//2)}")

	def play_round(self):
		# Reset players end game state
		self.hands = [Hand()]
		for player in self.players:
			player.hands = [Hand()]
			player.dealer_visible_card = PlayingCard
			player.action_map = {
				"Hit": 0, 
				"Stand": 0, 
				"Double": 0, 
				"Split":0
			}
		if self.verbose:
			print("-"*50)
			print("-"*19, "New Round", "-"*20)
			print("-"*50)

		if not self.dealing_period(): # All Players won
			self.playing_period()
			all_busted = not any(
				hand.end_game_state != EndGameHandState.Bust
				for player in self.players
				for hand in player.hands
			)
			if not all_busted:
				if self.verbose:
					print("-------- The Dealer flips his hidden card --------")
					print("-"*50)
				for card in self.hands[0].cards:
					if isinstance(card, PlayingCard):
						card.visible = True
				if self.verbose:
					self.hands[0].print_hand(self.name, True)
				self.final_dealing_period_for_dealer()

		self.print_all_hand_results()



# james = Player("James", 500)
# seth = Dealer("Seth", [james])

# seth.play_round()