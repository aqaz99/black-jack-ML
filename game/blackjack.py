from cards import Deck, PlayingCard
from player import Player
from enums import Actions



# Dealer / GameManager 
# Runs game loop, deals cards, etc
class Dealer(Player):
	def __init__(self, name, players: list[Player]):
		self.name = name
		self.deck = Deck()
		self.hand: list[PlayingCard] = []
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
				print(f"{player.name} gets a blackjack!")
				return True
		return False
	
	def final_dealing_period_for_dealer(self):
		dealer_hand_value = self.get_hand_value()
		if type(dealer_hand_value) == tuple: # Has an ace
			if(dealer_hand_value[0] < 17 and dealer_hand_value[1] < 17):
				print("------------------ Dealer Hits -------------------")
				self.deal_card(self)
				self.print_hand(True)
				self.final_dealing_period_for_dealer()
				return
			
			dealer_hand_value = max(dealer_hand_value[0], dealer_hand_value[1])

		else: # No ace
			if(dealer_hand_value < 17):
				print("------------------ Dealer Hits -------------------")
				self.deal_card(self)
				self.print_hand(True)
				self.final_dealing_period_for_dealer()
				return

		if dealer_hand_value > 21:
			print("----------------- Dealer Busts -------------------")
		else:
			for player in self.players:
				end_output = ""
				if dealer_hand_value > player.get_hand_value(True):
					end_output += f"Dealer Beats {player.name}"
					padding_count = 48 - len(end_output)
				elif dealer_hand_value == player.get_hand_value(True):
					end_output += f"{player.name} pushes"
					padding_count = 48 - len(end_output)
				else:
					end_output += f"{player.name} beats the dealer"
					padding_count = 48 - len(end_output)
				
				player.print_hand()
				print(f"{'-'*(padding_count//2)} {end_output} {'-'*(padding_count//2)}")


		



	def playing_period(self):
		"""
		Return true if the player is in / chose stand
		Return false if the player busted
		"""
		for player in self.players:
			if not player.busted:
				action = player.get_possible_actions()
				if action == Actions.Hit.value:
					self.deal_card(player)
					self.print_hand(True)
					player.print_hand()
					if player.get_hand_value() > 21:
						print("Bust!")
						player.busted = True
						return 
					self.playing_period()
		
				elif action == Actions.Stand.value:
					return 
				else:
					print(action)



	def cleanup_period(self):
		pass
	
	def play_round(self):
		print("-"*50)
		print("-"*19, "New Round", "-"*20)
		print("-"*50)
		if not self.dealing_period(): # All Players won
			print("-"*50)
			self.playing_period()
			if all(player.busted for player in self.players):
				print("Dealer wins")
				return
			print("-------- The Dealer flips his hidden card --------")
			print("-"*50)
			for card in self.hand:
				card.visible = True
			self.print_hand(True)
			self.final_dealing_period_for_dealer()





james = Player("James", 500)
seth = Dealer("Seth", players=[james])

seth.play_round()



