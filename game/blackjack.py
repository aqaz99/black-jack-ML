from cards import Deck
from player import Player

# Dealer / GameManager 
# Runs game loop, deals cards, etc
class Dealer :
	def __init__(self):
		self.deck = Deck()

	def say_hello(self):
		print("Yo")

	def deal_card(self, recieving_player: Player):
		recieving_player.hand.append(self.deck.remove_card())
	
	def shuffle_deck(self):
		self.deck.reset_deck()
	


seth = Dealer()
james = Player("James", 500)
print(seth.deck)
seth.deal_card(james)
james.print_hand()
print(seth.deck)



