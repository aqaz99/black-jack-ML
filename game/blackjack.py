from game.cards import Deck
from game.player import Player
from game.enums import Action, EndGameState



# Dealer / GameManager 
# Runs game loop, deals cards, etc
class Dealer(Player):
	def __init__(self, name, players: list[Player], verbose = True):
		super().__init__(name, starting_capital=0, verbose=verbose)
		self.deck = Deck()
		self.players = players

	def deal_card(self, recieving_player: Player, visible = True):
		card = self.deck.remove_card()
		card.visible = visible
		recieving_player.hand.append(card)
	
	
	def shuffle_deck(self):
		self.deck.reset_deck()
	
	def betting_period(self):
		pass

	def dealing_period(self):
		# Don't need to refresh deck everytime, just for now
		self.shuffle_deck()
		dealer_card_visible = True
		while len(self.hand) < 2:
			for player in self.players:
				self.deal_card(player)
			self.deal_card(self, dealer_card_visible)
			dealer_card_visible = False
		
		self.print_hand(True)
		for player in self.players:
			player.print_hand()
			if player.get_hand_value(True) == 21:
				if self.verbose:
					print(f"{player.name} gets a blackjack!")
					player.end_game_state = EndGameState.Win
				return True
		return False
	
	def set_player_endgame_state(self, state: EndGameState):
		for player in self.players:
			if player.end_game_state == EndGameState.Null:
				player.end_game_state = state

			if not player.end_game_state == EndGameState.Bust:
				player.end_game_state = state
	
	def final_dealing_period_for_dealer(self):
		dealer_hand_value = self.get_hand_value()
		if type(dealer_hand_value) == tuple: # Has an ace
			if(dealer_hand_value[0] < 17 and dealer_hand_value[1] < 17):
				if self.verbose:
					print("------------------ Dealer Hits -------------------")
				self.deal_card(self)
				self.print_hand(True)
				self.final_dealing_period_for_dealer()
				return
			
			dealer_hand_value = max(dealer_hand_value[0], dealer_hand_value[1])

		else: # No ace
			if(dealer_hand_value < 17):
				if self.verbose:
					print("------------------ Dealer Hits -------------------")
				self.deal_card(self)
				self.print_hand(True)
				self.final_dealing_period_for_dealer()
				return

		if dealer_hand_value > 21:
			if self.verbose:
				print("----------------- Dealer Busts -------------------")
			self.set_player_endgame_state(EndGameState.Win)
		else:
			for player in self.players:
				end_output = ""
				if dealer_hand_value > player.get_hand_value(True):
					self.set_player_endgame_state(EndGameState.DealerWin)
					end_output += f"Dealer Beats {player.name}"
					padding_count = 48 - len(end_output)
				elif dealer_hand_value == player.get_hand_value(True):
					self.set_player_endgame_state(EndGameState.Push)
					end_output += f"{player.name} pushes"
					padding_count = 48 - len(end_output)
				else:
					self.set_player_endgame_state(EndGameState.Win)
					end_output += f"{player.name} beats the dealer"
					padding_count = 48 - len(end_output)
				
				player.print_hand()
				if self.verbose:
					print(f"{'-'*(padding_count//2)} {end_output} {'-'*(padding_count//2)}")

	def playing_period(self):
		"""
		Handle each player's turn until they stand or bust.
		"""
		for player in self.players:
			while not player.end_game_state == EndGameState.Bust:
				action = player.get_possible_actions()

				if action == Action.Hit:
					self.apply_card_action(player)
					hand_value = player.get_hand_value()
					if isinstance(hand_value, tuple):
						has_21 = 21 in hand_value
					else:
						has_21 = hand_value == 21

					if has_21:
						break

				elif action == Action.Double:
					self.apply_card_action(player)
					break  

				elif action == Action.Stand:
					break

				else:
					if self.verbose:
						print(f"Unknown action: {action}")
					break


	def apply_card_action(self, player: Player):
		"""Helper to deal, print, and handle busting logic."""
		player.took_first_action = True
		self.deal_card(player)
		self.print_hand(True)
		player.print_hand()

		hand_value = player.get_hand_value()
		if isinstance(hand_value, tuple):
			# collect all values in the tuple that are non-busted
			value = max([v for v in hand_value if v <= 21], default=min(hand_value))
		else:
			value = hand_value

		if value > 21:
			end_output = f"{player.name} Busts"
			padding_count = 48 - len(end_output)
			if self.verbose:
				print(f"{'-'*(padding_count//2)} {end_output} {'-'*(padding_count//2)}")
			player.end_game_state = EndGameState.Bust


	def cleanup_period(self):
		pass
	
	def play_round(self):
		# Reset players end game state
		self.hand.clear()
		for player in self.players:
			player.end_game_state = EndGameState.Null
			player.hand.clear()
			player.took_first_action = False
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
			if self.verbose:
				print("-"*50)
			self.playing_period()
			if all(player.end_game_state == EndGameState.Bust for player in self.players):
				return
			if self.verbose:
				print("-------- The Dealer flips his hidden card --------")
				print("-"*50)
			for card in self.hand:
				card.visible = True
			self.print_hand(True)
			self.final_dealing_period_for_dealer()


# james = Player("James", 500)
# seth = Dealer("Seth", [james])

# seth.play_round()