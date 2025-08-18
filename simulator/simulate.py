from game.blackjack import Dealer
from game.player import Player
from simulator.random_player import RandyRanom

verbose = True
robbie = RandyRanom("Robbie", 500, verbose)
seth = Dealer("Seth", [robbie], verbose)

game_tracker = {
	"hands": {	
		"Null": 0, 
		"Win": 0, 
		"Push": 0, 
		"Bust": 0, 
		"DealerWin":0
	},
	"actions": {
		"Hit": 0, 
		"Stand": 0, 
		"Double": 0, 
		"Split":0
	}
}
for i in range(10): 
	seth.play_round()
	game_tracker["hands"][robbie.end_game_state.name] += 1
	for key, val in robbie.action_map.items():
		game_tracker["actions"][key] += val

for key, val in game_tracker["hands"].items():
	print(key, val)

for key, val in game_tracker["actions"].items():
	print(key, val)