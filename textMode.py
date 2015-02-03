#!/usr/bin/env python

from helperFunctions import *
from clue import *

clear()

playerNames = []
name = None
userPlayer = -1
print("Enter all players' names in turn order. Blank to end.")
while True:
	name = raw_input("Player's name: ")
	if userPlayer == -1 and yn_input("Is this you? "):
		userPlayer = len(playerNames)
	if name == "":
		break
	playerNames.append(name)

print("For this game we will be using the standard deck.") #TODO allow using a nonstandard deck.
raw_input("Press Enter to continue...")
clear()

game = clueGame(playerNames, userPlayer)

userCardCount = game.players[userPlayer].numCards

while True:
	userHand = []

	for category in game.deck.keys():
		for card in game.deck[category]:
			if len(userHand) < userCardCount:
				if yn_input("Do you have the {}, {}? ".format(category, card)):
					userHand.append(card)

	if len(userHand) >= userCardCount:
		break
	else:
		print("You didn't tell me enough cards. Let's start over.")
		
clear()

game.set_user_hand(userHand)

# -------------Keep the guessing going forever-------------------
while True:

	currentName = game.players[game.currentPlayer].name
	print("It is {}'s turn.".format(currentName))
	
	print("1. {} Made a guess.".format(currentName))
	print("2. {} Didn't make a guess.".format(currentName))
	print("3. Show data table so far.")
	option = int_input("Choose as option: ")
	
	if option == 1:
		pass
	elif option == 2:
		game.pass_turn()
		clear()
		continue
	elif option == 3:
		clear()
		print_hands(game)
		raw_input("\n\nPress enter to continue... ")
		continue
	else:
		raw_input("That isn't a valid option. Press any key to continue... ")
	
	guess = []
	
	for category in game.deck.keys():
		while True:
			card = raw_input("Which {} did she guess? ".format(category))
			if card in game.deck[category]:
				guess.append(card)
				break
			print("That's not a {}. ".format(category)),
			
	while guess != None:
		disprover = raw_input("Who had a disproving card? ")
		if disprover in playerNames:
			disprover = playerNames.index(disprover)
			break
		print("That's not a valid player. "),
			
	if game.currentPlayer == game.userPlayer and guess != None:
		while True:
			card = raw_input("What card did you see? ")
			if card in game.deck:
				break
			print("That's not a card in the deck. "),
	else:
		cardSeen = None

	game.take_turn(guess, disprover, cardSeen)
	
	
	
	
	
