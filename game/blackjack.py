from cards import Deck

# Dealer / GameManager 
# Runs game loop, deals cards, etc
class Dealer :
	def __init__(self):
		self.deck = Deck()

	def say_hello(self):
		print("Yo")
	
	def shuffle_deck(self):
		self.deck.reset_deck()





seth = Dealer()
print(seth.deck)
# print(seth.deck.print_deck())
