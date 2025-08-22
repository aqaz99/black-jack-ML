from game.cards import  PlayingCard
from game.enums import Action
from game.hand import Hand


class Player:
	def __init__(self, name, starting_capital, verbose=True):
		self.name = name
		self.cash = starting_capital
		self.verbose = verbose
		self.hands = [Hand(verbose)]
		self.dealer_visible_card = PlayingCard
		self.action_map = {
			"Hit": 0, 
			"Stand": 0, 
			"Double": 0, 
			"Split":0
		}


	def get_possible_hand_actions(self, hand: Hand) -> Action:
		choice = Action.Hit
		available_actions = [
			Action.Hit,
			Action.Stand,
		]
		if not hand.took_first_action: # Can't double after first deal
			available_actions.append(Action.Double)

		if hand.cards[0].value == hand.cards[1].value: # Check split
			available_actions.append(Action.Split)

		if self.verbose:
			for action in available_actions:
				print(f"{action.value}) {action.name}")

		while True:
			try:
				choice = int(input("What would you like to do: "))
				if choice > len(available_actions):
					continue
				action = Action(choice) 
				break
			except ValueError:
				pass
		if self.verbose:
			print("-"*50)	
		
		self.action_map[action.name] += 1
		return action
	