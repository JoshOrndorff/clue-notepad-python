#!/usr/bin/env python

from helperFunctions import *
from cluePackage import *
from os.path import isfile

clear()

# Get basic player info.
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


# Choose the deck
if yn_input("Would you like to use the standard deck? "):
  deck = "standard.deck"
else:
  deck = ""
  while not isfile(deck):
    deck = raw_input("Please type the path to your custom deck: ")
    # This works because the screen is cleared immediately if the path is good.
    print("\nSorry, that's not a valid path, please try again.")
clear()

# Create the game object
game = clueGame(playerNames, userPlayer, deck)


# Figure out which cards are in the user's hand.
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
  print  ("")
  print("1. Explain how to guess.".format(currentName))
  print("2. Pass turn.")
  print("3. Data Table.")
  print("4. Game History.")
  print("5. Disproofs.")
  print("")
  option = raw_input(" Enter a guess or choose an option: ")
  
  if option == '1':
    explain_guessing()
    raw_input("\n\nPress enter to continue...")
    continue
  elif option == '2':
    game.pass_turn()
    continue
  elif option == '3':
    print_hands(game)
    raw_input("\n\nPress enter to continue...")
    continue
  elif option == '4':
    print_history(game)
    raw_input("\n\nPress enter to continue...")
    continue
  elif option == '5':
    print_disproofs(game)
    raw_input("\n\nPress enter to continue...")
    continue
  
  
  # They made an actual guess
  try:
    guess = parse_guess(option, game.deck)
  except ValueError:
    raw_input("That is not a valid guess. Press enter to continue...")
    continue

  disprover = int_choice("Who had a disproving card? ", game.players[:]+[None], playerNames[:]+["Nobody"])
      
  if game.currentPlayer == game.userPlayer and disprover != None:
    names = []
    for card in guess:
      names.append(card.name)
    cardSeen = int_choice("Which card did you see?", guess, names)
  else:
    cardSeen = None

  game.take_turn(guess, disprover, cardSeen)
  
  
  
  
  
