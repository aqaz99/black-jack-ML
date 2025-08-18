from game.blackjack import Dealer
from game.player import Player


james = Player("James", 500)
seth = Dealer("Seth", players=[james])

seth.play_round()
