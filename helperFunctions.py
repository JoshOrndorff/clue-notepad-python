from os import system, name

def int_input(prompt):
	"""
		Allows the user to input an integer,
		and asks for another try if a non-integer is entered.
	"""
	answer = raw_input(prompt)
	try:
		answer = int(answer)
		return answer
	except ValueError:
		int_input("That isn't a integer dude, please try again. ")

def yn_input(prompt):
	"""
		Allows the user to answer yes / no questions,
		and asks for another try if a non-integer is entered.
	"""
	answer = raw_input(prompt).lower()
	if answer in ["yes", "y"]:
		return True
	elif answer in ["no", "n"]:
		return False
	else:
		yn_input("Please type yes, no, y, or n. ")

def clear():
	''' Simple cross-platform screen clearing function'''
	system('cls' if name == 'nt' else 'clear')
	

def print_hands(game):
	
	# Print the title row
	print(" " * 12 + "\t"),
	for player in game.players:
		print(player.name + "\t\t"),

	for category in game.deck.get_categories():
		print("\n--------{}-------".format(category)),
		for card in game.deck:
			if card.category == category:
				print("\n{0:>12}\t".format(card.name)),
				for player in game.players:
					if card in player.has:
						print("Have It\t\t"),
					elif card in player.hasnt:
						print("Nope   \t\t"),
					else:
						print("?????\t\t"),






