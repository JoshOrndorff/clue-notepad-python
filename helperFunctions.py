from os import system, name

def int_input(prompt, min = None, max = None):
  """
    Allows the user to input an integer,
    and asks for another try if a non-integer is entered.
  """
  answer = raw_input(prompt)
  try:
    answer = int(answer)
  except ValueError:
    answer = int_input("That isn't a integer dude, please try again. ", min, max)

  while min and answer < min:
    answer = int_input("Number must be at least {}. ".format(min), min, max)

  while max and answer > max:
    answer = int_input("Number must not be more than {}. ".format(max), min, max)

  return answer

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
    return yn_input("Please type yes, no, y, or n. ")

def clear():
  ''' Simple cross-platform screen clearing function'''
  system('cls' if name == 'nt' else 'clear')

def int_choice(prompt, choices, texts = None):

  if texts == None:
    texts = choices
  elif len(texts) != len(choices):
    raise ValueError("Choices and Texts must be the same length. ")

  print(prompt)

  for i in range(len(choices)):
    print("{}. {}".format(i, texts[i]))

  numAnswer = int_input("Choose an integer. ", 0, len(choices) - 1)
  
  return choices[numAnswer]
  
def explain_guessing():
  print("Explanation is not yet implemented. Sorry. Good Luck.")

def print_hands(game):
  '''
  Prints all known information about players' hands.
  '''

  # Print the title row
  print(" " * 13 + "\t"),
  for player in game.players:
    print("{0:>13}".format(player.name)),

  for category in game.deck.categories:
    print("\n--------{}-------".format(category)),
    for card in game.deck:
      if card.category == category:
        print("\n{0:>13}\t".format(card.name)),
        for player in game.players:
          if card in player.has:
            print("{0:>13}".format("  Have It ")),
          elif card in player.hasnt:
            print("{0:>13}".format("Don't Have")),
          else:
            print("{0:>13}".format("?-?-?-?-?-")),

def print_history(game):
  '''
  Prints the record of all turns in the game so far.
  '''

  if len(game.history) == 0:
    print("No turns yet")
    return


  for turn in game.history:
    if turn["guess"] == None: # Passed turn
      print("{} passed.".format(turn["guesser"].name))

    elif turn["disprover"] != None: # Normal turn
      print("{} guessed [{}, {}, {}] and {} showed a card.".format(\
      turn["guesser"].name,\
      turn["guess"][0].name, turn["guess"][1].name, turn["guess"][2].name,\
      turn["disprover"].name\
      ))

    else: # Winning
      print("{} guessed [{}, {}, {}] and won.".format\
           (turn["guesser"].name, turn["guess"][0], turn["guess"][1], turn["guess"][2]))
      

def print_disproofs(game):
  '''
  Prints a list of all of a player's disproofs.

  A disproof is a list of cards of which the player has at least one as
  evidenced by the player having shown an unknown card earlier in the game.
  '''

  for player in game.players:
    print("---{}'s disproofs---".format(player.name))
    if len(player.disproofs) == 0:
      print("{} has no disproofs.\n".format(player.name))
      continue
    for disproof in player.disproofs:
      for card in disproof:
        print("{0:>12}\t".format(card.name)),
      print("")

def parse_guess(shorthand, deck):
  '''
  Returns a list of cards (one from each category) given a shorthand string.
  Raises a ValueError if shorthand string is not valid.
  '''
  guess = []
  sortedGuess = []
  
  # Split shorthand into individual entries, and make sure the number is correct.
  shorthand = shorthand.lower().split()
  if len(shorthand) != len(deck.categories):
    raise ValueError("Shorthand must contain exactly {} entries.".format(len(deck)))
    
  # Find a card that "matches" each shorthand entry
  for item in shorthand:
    matchedOne = False
    for card in deck:
      # Compute the possible matching names. This is not trivial because of two-word cards.
      toMatch = card.name.lower().split()
      for x in toMatch:
        x = x[:len(item)]
        if item == x:
          if not matchedOne:
            guess.append(card)
            matchedOne = True
          else:
            raise ValueError("Shorthand item {} is not unique.".format(item))
  
  # Make sure there is one card from each category
  for category in deck.categories:
    cardFound = False
    for card in guess:
      if card in deck.get_cards_by_category(category):
        cardFound = True
        # And put them in the correct order.
        sortedGuess.append(card)
    if not cardFound:
      raise ValueError("No card found in category, {}.".format(category))
  
  return sortedGuess









