from game.cards import Deck, PlayingCard
from game.hand import Hand
from game.player import Player
from game.enums import Action, EndGameHandState

# What if player gets blackjack at same time as deal
# What if split is a blackjack

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
		
		self.hands[0].print_hand(self.name,True)
		for player in self.players:
			if player.hands[0].get_hand_value(True) == 21:
				if self.verbose:
					player.hands[0].print_hand(player.name)
					print(f"{player.name} gets a blackjack!")
					player.hands[0].end_game_state = EndGameHandState.Win
				return True
		return False
	
	def final_dealing_period_for_dealer(self):
		dealer_hand_value = self.hands[0].get_hand_value()
		if type(dealer_hand_value) == tuple: # Has an ace
			if(dealer_hand_value[0] < 17 and dealer_hand_value[1] < 17):
				if self.verbose:
					print("------------------ Dealer Hits -------------------")
				self.deal_card(self.hands[0])
				self.hands[0].print_hand(self.name, True)
				self.final_dealing_period_for_dealer()
				return
			
			dealer_hand_value = max(dealer_hand_value[0], dealer_hand_value[1])

		else: # No ace
			if(dealer_hand_value < 17):
				if self.verbose:
					print("------------------ Dealer Hits -------------------")
				self.deal_card(self.hands[0])
				self.hands[0].print_hand(self.name, True)
				self.final_dealing_period_for_dealer()
				return

		if dealer_hand_value > 21:
			if self.verbose:
				print("----------------- Dealer Busts -------------------")
		else:
			for player in self.players:
				for hand in player.hands:
					end_output = ""	
					if dealer_hand_value > hand.get_hand_value(True):
						end_output += f"Dealer Beats {player.name}"
						padding_count = 48 - len(end_output)
						hand.end_game_state = EndGameHandState.DealerWin
					elif dealer_hand_value == hand.get_hand_value(True):
						end_output += f"{player.name} pushes"
						padding_count = 48 - len(end_output)
						hand.end_game_state = EndGameHandState.Push
					else:
						end_output += f"{player.name} beats the dealer"
						padding_count = 48 - len(end_output)
						hand.end_game_state = EndGameHandState.Win

					
					hand.print_hand(self.name)
					if self.verbose:
						print(f"{'-'*(padding_count//2)} {end_output} {'-'*(padding_count//2)}")


	def play_individual_player_hands(self, player: Player):
		# Need to figure out how to display hands that win or lose after standing after a split. 
		# make it smart so it works also when we don't split

		for hand in player.hands: # While each hand isn't done we continue
			if not hand.hand_stand and hand.end_game_state == EndGameHandState.Null:
				if self.verbose:
					hand.print_hand(player.name)
					print("-"*50)
				
				action = player.get_possible_hand_actions(hand)
				if action == Action.Hit:
					self.apply_card_action(player, hand=hand)
					hand_value = hand.get_hand_value()
					if (isinstance(hand_value, tuple) and 21 in hand_value) or hand_value == 21:
						break
					# If bust, also break
					if (isinstance(hand_value, tuple) and min(hand_value) > 21) or (not isinstance(hand_value, tuple) and hand_value > 21):
						break
				elif action == Action.Double:
					self.apply_card_action(player, hand=hand)
					break
				elif action == Action.Stand:
					hand.hand_stand = True
					break
				elif action == Action.Split:
					pass
		
		# while hands_to_play:
		# 	hand = hands_to_play.pop(0)
		# 	hand_obj = Hand()
		# 	for c in hand:
		# 		hand_obj.append(c)
		# 	player.hand.clear()
		# 	player.hand.extend(hand_obj)

		# 	while True:
		# 		if len(hands_to_play) > 0:
		# 			print("------------------ Split Hand --------------------")
		# 		if self.verbose:
		# 			player.print_hand(self.name)
		# 			print("-"*50)


				# action = player.get_possible_hand_actions()
				# if action == Action.Hit:
				# 	self.apply_card_action(player)
				# 	hand_value = player.get_hand_value()
				# 	if (isinstance(hand_value, tuple) and 21 in hand_value) or hand_value == 21:
				# 		break
				# 	# If bust, also break
				# 	if (isinstance(hand_value, tuple) and min(hand_value) > 21) or (not isinstance(hand_value, tuple) and hand_value > 21):
				# 		break
				# elif action == Action.Double:
				# 	self.apply_card_action(player)
				# 	break
				# elif action == Action.Stand:
				# 	break
				# elif action == Action.Split:
		# 			# Take both cards out, split into two new hands
		# 			card1, card2 = player.hand[0], player.hand[1]

		# 			# First split hand: card1 + 1 new card
		# 			self.deal_card(player)
		# 			new_hand1 = Hand()
		# 			new_hand1.extend([card1, player.hand.pop()])

		# 			# Second split hand: card2 + 1 new card
		# 			self.deal_card(player)
		# 			new_hand2 = Hand()
		# 			new_hand2.extend([card2, player.hand.pop()])


		# 			# Add both to the queue for further play
		# 			hands_to_play.append(new_hand1)
		# 			hands_to_play.append(new_hand2)
		# 			break
		# 		else:
		# 			break
			
		# 	# Optionally, keep track of outcomes here (win, bust, etc.)
		# 	results.append(player.end_game_state)
		# # Optionally: player.hand = hands_to_play (final state for later use)
		# return results

	def playing_period(self):
		for player in self.players:
			self.play_individual_player_hands(player)

	def apply_card_action(self, player: Player, hand: Hand):
		"""Helper to deal, print, and handle busting logic."""
		hand.took_first_action = True
		self.deal_card(hand)
		self.hands[0].print_hand(self.name, True)

		hand_value = hand.get_hand_value()
		if isinstance(hand_value, tuple):
			# collect all values in the tuple that are non-busted
			value = max([v for v in hand_value if v <= 21], default=min(hand_value))
		else:
			value = hand_value

		if value > 21:
			end_output = f"{player.name} Busts"
			padding_count = 48 - len(end_output)
			if self.verbose:
				hand.print_hand(self.name)
				print(f"{'-'*(padding_count//2)} {end_output} {'-'*(padding_count//2)}")
			hand.end_game_state = EndGameHandState.Bust


	def cleanup_period(self):
		pass
	
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
			if all(
				hand.end_game_state == EndGameHandState.Bust
				for player in self.players
				for hand in player.hands
			):
				return
			if self.verbose:
				print("-------- The Dealer flips his hidden card --------")
				print("-"*50)
			for card in self.hands[0].cards:
				if isinstance(card, PlayingCard):
					card.visible = True
			self.hands[0].print_hand(self.name, True)
			self.final_dealing_period_for_dealer()


james = Player("James", 500)
seth = Dealer("Seth", [james])

seth.play_round()