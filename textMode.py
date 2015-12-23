#!/usr/bin/env python

from helperFunctions import *
from cluePackage import *
from os.path import isfile

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

if yn_input("Would you like to use the standard deck? "):
	deck = "standard.deck"
else:
	deck = ""
	while not isfile(deck):
		deck = raw_input("Please type the path to your custom deck: ")
		# This works because the screen will be cleared immediately if the path is good.
		print("\nSorry, that's not a valid path, please try again.")
clear()

game = clueGame(playerNames, userPlayer, deck)

userCardCount = game.players[userPlayer].numCards

while True:
	userHand = []

	for card in game.deck:
		if len(userHand) < userCardCount:
			if yn_input("Do you have the {}, {}? ".format(card.category, card.name)):
				userHand.append(card)

	if len(userHand) >= userCardCount:
		break
	else:
		print("You didn't tell me enough cards. Let's start over.")
		
clear()

game.set_user_hand(userHand)

# -------------Keep the guessing going forever-------------------
while True:

	clear()

	currentName = game.currentPlayer.name
	print("It is {}'s turn.".format(currentName))
	
	print("1. {} made a guess.".format(currentName))
	print("2. {} passed his turn.".format(currentName))
	print("")
	print("3. Data Table.")
	print("4. Game History.")
	print("5. Disproofs.")
	print("")
	option = int_input("Choose an option: ")
	
	if option == 1:
		pass # This code comes later, after the else clause.
	elif option == 2:
		game.pass_turn()
		continue
	elif option == 3:
		print_hands(game)
		raw_input("\n\nPress enter to continue... ")
		continue
	elif option == 4:
		print_history(game)
		raw_input("\n\nPress enter to continue... ")
		continue
	elif option == 5:
		print_disproofs(game)
		continue
	else:
		raw_input("That isn't a valid option. Press any key to continue... ")
	
	
	# They made a guess
	guess = []

	for category in game.deck.categories:
		cards = game.deck.get_cards_by_category(category)
		names = []
		for card in cards:
			names.append(card.name)
		card = int_choice("Which {} did {} guess?".format(category, game.currentPlayer.name), cards, names)
		guess.append(card)
			
	disprover = int_choice("Who had a disproving card? ", game.players, playerNames)
			
	if game.currentPlayer == game.userPlayer:
		names = []
		for card in guess:
			names.append(card.name)
		cardSeen = int_choice("Which card did you see?", guess, names)
	else:
		cardSeen = None

	game.take_turn(guess, disprover, cardSeen)
	
	
	
	
	
