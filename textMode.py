#!/usr/bin/env python

from helperFunctions import *
from cluePackage import *
from os.path import isfile
from sys import argv
import xml.etree.ElementTree as ET


def new_game():
  '''
  Prompts user for info necessary to start a new game, creates the game, and
  returns the game object.
  '''

  players = []
  userPlayer = None

  # Get basic player info.
  name = None
  print("Enter all players' names in turn order. Blank to end.")
  while name != '':
    name = raw_input("Player's name: ")
    if name != "":
      players.append(cluePlayer(name))
      if userPlayer == None and yn_input("Is this you? "):
        userPlayer = players[-1]


  # Choose the deck
  if yn_input("Would you like to use the standard deck? "):
    deck = None
  else:
    deckPath = ""
    while not isfile(deck):
      deckPath = raw_input("Please type the path to your custom deck: ")
      # This works because the screen is cleared immediately if the path is good.
      print("\nSorry, that's not a valid path, please try again.")
    deckElement = ET.parse(deckPath)
    deck = clueDeck(deckElement)
  clear()

  # Create the game object
  game = clueGame(players, userPlayer, deck)


  # Figure out which cards are in the user's hand.
  while True:
    userHand = []

    for card in game.deck:
      if len(userHand) < userPlayer.numCards:
        if yn_input("Do you have the {}, {}? ".format(card.category, card.name)):
          userHand.append(card)

    if len(userHand) >= userPlayer.numCards:
      break
    else:
      print("You didn't tell me enough cards. Let's start over.")

  game.set_user_hand(userHand)
  
  return game
  


if len(argv) > 1:
  game = import_game(argv[1])
#  TODO don't except exceptions until I know the import code is working.
#  try:
#    game = import_game(argv[1])
#  except:
#    print("{} is not a valid game file. Creating new game.\n".format(argv[1]))
#    game = new_game()
else:
  game = new_game()



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
  print("6. Export Game")
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
  elif option == '6':
    gamePath = raw_input("Filename: ")
    game.export(gamePath)      
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

