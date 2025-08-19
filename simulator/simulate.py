from game.blackjack import Dealer
from game.cards import PlayingCard
from game.enums import Suit
from game.player import Player
from simulator.players.perry_perfect import PerryPerfect
from simulator.players.randy_random import RandyRandom

# Run command: python3 -m simulator.simulate
def simulate_perry():
	hard_perfect_string = "HHHHHHHHHHHHHHHHHHHHHDDDDHHHHHDDDDDDDDHHDDDDDDDDDDHHSSSHHHHHSSSSSHHHHHSSSSSHHHHHSSSSSHHHHHSSSSSHHHHHSSSSSSSSSS"
	soft_perfect_string = "HHHDDHHHHHHHHDDHHHHHHHDDDHHHHHHHDDDHHHHHHDDDDHHHHHDDDDDSSHHHSSSSSSSSSS"
	pairs_perfect_string = "PPPPPPHHHHPPPPPPHHHHHHHPPHHHHHDDDDDDDDHHPPPPPHHHHHPPPPPPHHHHPPPPPPPPPPPPPPPSPPSSSSSSSSSSSSPPPPPPPPPP"

	perry = PerryPerfect("Perry", 1000)

	hard_text = ""
	# Test hard hand
	for i in range(5, 16):
		perry.hand = [PlayingCard("", (2, 2), suit=Suit.Hearts), PlayingCard("", (i, i), suit=Suit.Hearts)]
		for j in range(2, 12):
			play = perry.get_perfect_play(j).name[0]
			hard_text += play

	ace_text = ""
	# Test Aces / soft hand
	for i in range(2, 9):
		perry.hand = [PlayingCard("Ace", (1, 11), suit=Suit.Hearts), PlayingCard("", (i, i), suit=Suit.Hearts)]
		for j in range(2, 12):
			play = perry.get_perfect_play(j).name[0]
			ace_text += play
	
	pair_text = ""
	# Test pairs
	for i in range(2, 12):
		if i <= 10:
			perry.hand = [PlayingCard("", (i, i), suit=Suit.Hearts), PlayingCard("", (i, i), suit=Suit.Hearts)]
		else:
			perry.hand = [PlayingCard("Ace", (1, 11), suit=Suit.Hearts), PlayingCard("Ace", (1, 11), suit=Suit.Hearts)]

		for j in range(2, 12):
			play = perry.get_perfect_play(j)
			if play.name == "Split":
				play = "P"
			else:
				play = play.name[0]
			pair_text += play
		
	print("Hard Test:", hard_text == hard_perfect_string)
	print("Soft Test:", ace_text == soft_perfect_string)
	print("Pair Test:", pair_text == pairs_perfect_string)

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