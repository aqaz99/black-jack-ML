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
		print("")
		for player in self.players:
			player.print_hand()

	def playing_period(self):
		for player in self.players:
			player.print_possible_actions()
			


	def cleanup_period(self):
		pass
	
	def play_round(self):
		print("-"*50)
		print("-"*19, "New Round", "-"*20)
		print("-"*50)
		self.dealing_period()
		print("-"*50)
		self.playing_period()




james = Player("James", 500)
seth = Dealer("Seth", players=[james])

seth.play_round()



