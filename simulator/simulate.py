from game.blackjack import Dealer
from game.cards import PlayingCard
from game.enums import Suit
from game.player import Player
from simulator.players.perry_perfect import PerryPerfect
from simulator.players.randy_random import RandyRandom

# Run command: python3 -m simulator.simulate
def simulate_perry():
    perry = PerryPerfect("Perry", 1000)
    perry.hand = [PlayingCard("Four", (4, 4), suit=Suit.Hearts), PlayingCard("Five", (5, 5), suit=Suit.Hearts)]
    # seth = Dealer("Seth", [perry])
    print(perry.get_perfect_play(6))

def simulate_randy():
	verbose = False
	game_count = 100000
	robbie = RandyRandom("Robbie", 1000, verbose)
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
	for i in range(game_count): 
		seth.play_round()
		game_tracker["hands"][robbie.end_game_state.name] += 1
		for key, val in robbie.action_map.items():
			game_tracker["actions"][key] += val


	hand_items = [(k, v) for k, v in game_tracker["hands"].items() if k != "Null"]
	action_items = list(game_tracker["actions"].items())


	action_total = sum(val for _, val in action_items)

	max_len = max(len(hand_items), len(action_items))
	hand_items += [("", "")] * (max_len - len(hand_items))
	action_items += [("", "")] * (max_len - len(action_items))

	end_output = f"Total Games: {game_count}"
	padding_count = 30 - len(end_output)
	print("-" * 31)
	print(f"{'-'*(padding_count//2)} {end_output} {'-'*(padding_count//2)}")
	print("-" * 31)

	for (hand_key, hand_val), (action_key, action_val) in zip(hand_items, action_items):
		if hand_key:
			hand_perc = f"{100*hand_val/game_count:.1f}%" if game_count else "0%"
			hand_print = f"{hand_key}: {hand_val} ({hand_perc})"
		else:
			hand_print = ""
		if action_key:
			action_perc = f"{100*action_val/action_total:.1f}%" if action_total else "0%"
			action_print = f"{action_key}: {action_val} ({action_perc})"
		else:
			action_print = ""
		print(f"| {hand_print:<16} | {action_print:<14} |")
	print("-" * 31)	


simulate_perry()