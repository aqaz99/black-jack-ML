from game.blackjack import Dealer
from game.player import Player
from simulator.random_player import RandyRanom


robbie = RandyRanom("Robbie", 500, False)
seth = Dealer("Seth", [robbie], False)

for i in range(10): 
	seth.play_round()
	print(robbie.end_game_state.name)