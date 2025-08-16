from cards import Deck, PlayingCard
from player import Player

# Dealer / GameManager 
# Runs game loop, deals cards, etc
class Dealer(Player):
	def __init__(self, name, players: list[Player]):
		self.name = name
		self.deck = Deck()
		self.hand: list[PlayingCard] = []
		self.players = players

	def deal_card(self, recieving_player: Player):
		recieving_player.hand.append(self.deck.remove_card())
	
	def shuffle_deck(self):
		self.deck.reset_deck()
	
	
	def play_round(self):
		# Don't need to refresh deck everytime, just for now
		while True:
			self.shuffle_deck()
			while len(self.hand) < 2:
				for player in self.players:
					self.deal_card(player)
					player.print_hand()
				self.deal_card(self)
			print(self.print_hand())
			
			action = input("What would you like to do?")



james = Player("James", 500)
seth = Dealer("Seth", players=[james])

seth.play_round()
# print(seth.deck)
# seth.deal_card(james)
# james.print_hand()
# print(seth.deck)



