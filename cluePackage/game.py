from player import cluePlayer
from deck import *
import xml.etree.ElementTree as ET

class clueGame(object):

  def __init__(self, players, userPlayer, deck = None):

    # Set up players
    if len(players) > 0:
      self.players = players
    else:
      raise ValueError("Player list cannot be empty.")

    # Load the deck
    if deck == None:
      self.deck = get_standard_deck()
    else:
      self.deck = deck

    # Determine how many cards each player gets
    minCardsPerHand = (len(self.deck) - len(self.deck.categories)) // len(players)
    playersWithExtraCard = (len(self.deck) - len(self.deck.categories)) % len(players)
    
    for player in self.players:
      if self.players.index(player) < playersWithExtraCard:
        player.numCards = minCardsPerHand + 1 
      else:
        player.numCards = minCardsPerHand
    
    # Validate the user player
    if userPlayer in self.players:
      self.userPlayer = userPlayer
    else:
      raise ValueError("userPlayer must be a player in the current game.")

    # Final initializing
    self.currentPlayer = self.players[0]
    self.history = []
    self.solution = []

  def pass_turn(self):
    '''
    This is a turn when the player does not make it to a room.
    '''
    self.history.append({"guesser": self.currentPlayer,\
                           "guess": None,\
                       "disprover": None,\
                        "cardSeen": None})

    self.next_player()
    
  def take_turn(self, guess, disprover = None, cardSeen = None):

    '''
      This is a normal turn where player makes a guess and disprover shows
      a card. NOTE: If no cards are shown but the game is not won because
      the guesser himself holds one of the cards guessed, disprover should
      equal the player guessing. If the game is in fact won, disprover should
      be None.
      
      Guess is a list of cards.

      This function or pass_turn must be called for each and every turn.
    '''

    # Ensure arguments are compatible
    if self.currentPlayer != self.userPlayer and cardSeen != None:
      raise ValueError("Cannot specify cardSeen unless it is users turn to guess.")
    if self.currentPlayer == self.userPlayer and disprover != self.currentPlayer and cardSeen == None:
      raise ValueError("Must specify cardSeen, when another player shows you a card.")

    # Ensure guess contains one card from each category
    if not len(guess) == len(self.deck.categories):
      raise ValueError("Guess must contain the same number of cards as categories in the deck.")
    for category in self.deck.categories:
      cards = self.deck.get_cards_by_category(category)
      categoryOK = False
      for card in guess:
        if card in cards:
          categoryOK = True
          break
      if not categoryOK:
        raise ValueError("Guess must contain one card from each category.")

    # Make sure nobody (except maybe the disprover) has the cardSeen.
    for otherPlayer in self.players:
      if otherPlayer != disprover:
        for testCard in otherPlayer.has:
          if cardSeen == testCard:
            raise ConflictingDataError("{} showed {}, but it is known to be in {}'s hand.".format(disprover.name, card.name, otherPlayer.name))

    # Add an entry to the game history (Slicing guess to copy it)
    self.history.append({"guesser": self.currentPlayer,\
                           "guess": guess[:],\
                       "disprover": disprover,\
                        "cardSeen": cardSeen})

    # When user sees a specific card note it.
    if cardSeen != None:
      self.new_info(disprover, cardSeen, True)

    # User doesn't see a specific card, and disprover is not known to have a guessed card.
    elif not bool(set(guess) & set(disprover.has)):  # Stole this intersection code from: http://stackoverflow.com/a/3170067/4184410
      # Remove cards known to be in hands other than the disprover's.
      for player in self.players:
        if player != disprover:
          for card in player.has:
            if card in guess:
              guess.remove(card)
      # Remove cards known to be in the solution
      for card in self.solution:
        if card in guess:
          guess.remove(card)
      # If the guess (after elemination) is not already in the disproof list
      if guess not in disprover.disproofs:
        disprover.disproofs.append(guess)

    # Figure out which players didn't show.
    numCurrent   = self.players.index(self.currentPlayer)
    numDisprover = self.players.index(disprover)
    if numCurrent < numDisprover:
      noShows = self.players[numCurrent + 1 : numDisprover]
    else:
      # This case also works when the guesser is the disprover
      noShows = self.players[: numDisprover] + self.players[numCurrent + 1 :]

    # Players who didn't show, should not have any of the guessed cards.
    for player in noShows:
      for card in guess:
        self.new_info(player, card, False)

    self.optimize()
    self.next_player()

  def optimize(self):
    '''Checks for completed process of elimination results
    And also does other general maintenance'''
    
    # Flag used to determine whether to make recursive optimization call.
    changes = False

    # Things that need to happen for each player.
    for player in self.players:    
      # If a player is known to have the correct number of cards, 
      # he does not have any other cards.
      if len(player.has) == player.numCards:
        for card in self.deck:
          if card not in player.has and card not in player.hasnt:
            self.new_info(player, card, False)
    
      # If a player is known to be without the maximum number of cards,
      # he has all remaining unknown cards.
      elif len(self.deck) - len(player.hasnt) - len(self.deck.categories) == player.numCards:
        for card in self.deck:
          if card not in player.has and card not in player.hasnt:
            self.new_info(player, card, True)

      # Any disproofs of length 1 are now known information.
      for disproof in player.disproofs:
        if len(disproof) == 1: # If any disproofs contain only one card
          self.new_info(player, disproof[0], True)
          
    # Any cards that are known not to be in any players' hands are in the solution.
    for card in self.deck:
      inSolution = True
      for player in self.players:
        if card not in player.hasnt:
          inSolution = False
      if inSolution and card not in self.solution:
        self.solution.append(card)          

    # Do I need to loop through all cards with known locations and remove them from
    # disproofs? Or is it impossible for them to have gotten there in the first place.
    # No, I don't. Whenever a card location is learned it is removed from all existing disproofs.
    
    # Sanity Check: At least one card in each category is not in the hands.
    # TODO: After the program is known to work, move this to the else clause
    # of the recursive call so it is only run once per turn (to help performance).
    for category in self.deck.categories:
      allFoundSoFar = True
      for card in self.deck.get_cards_by_category(category):
        for player in self.players:
          if card in player.has:
            break
          else:
            allFoundSoFar = False
      if allFoundSoFar:
        raise ConflictingDataError("All cards in {} category are known to be in players' hands.".format(category))
    
    # Finally, the recursive call
    if changes:
      self.optimize()

  def new_info(self, player, card, has):
    '''
    Updates all players' hands and disproofs when new information is
    discovered. Generally this method is only used internally.

    Processing that can be completed in one pass goes here. Processing that
    must happen recursively should go in optimize.
    
    Also for specifying additional information manually that does not come up
    during regular game play. For example if a card is turned up by accident,
    or there is table talk during the game.
    '''

    # TODO add a force argument in case the user is correcting invalid data
    # becuase, for example, a player forgot to show a card.

    if type(has) != bool:
      raise TypeError("Argument, has, must be Boolean (True or False).")

    # Player has the card
    if has:
      player.has.append(card)

      # All other players don't have it
      for otherPlayer in self.players:
        if otherPlayer != player:

          # Sanity Check
          if card in otherPlayer.has:
            raise ConflictingDataError("{} was just found not to have {}, but it is already listed in his had.".format(otherPlayer.name, card.name))

          # Don't have it in their hands
          otherPlayer.hasnt.append(card)

          # Don't have it in their disproofs
          for disproof in otherPlayer.disproofs:
            if card in disproof:
              disproof.remove(card)

      # Remove all disproofs containing the card from the players hand.
      for disproof in player.disproofs:
        if card in disproof:
          player.disproofs.remove(disproof)

    # Player doesn't have card
    else:
      player.hasnt.append(card)

      # Remove it from his previous disproofs
      for disproof in player.disproofs:
        if card in disproof:
          disproof.remove(card)

  def set_user_hand(self, cards):
    '''
    Used to set the cards dealt to the user. Accepts a list of strings
    representing the cards. No validation happens here because it is done
    immediately in the new_info function.
    '''
    for card in cards:
      self.new_info(self.userPlayer, card, True)

    self.optimize()

  def next_player(self):
    '''
    Update self.curretnPlayer to be the next player
    '''
    numCurrentPlayer = self.players.index(self.currentPlayer)
    numNextPlayer = (numCurrentPlayer +1) % len(self.players)
    self.currentPlayer = self.players[numNextPlayer]
    
  def export(self, gamePath):
    '''
      Saves current game state to a file to be restored later.
    '''
    
    gameElement = ET.Element('game')
    
    # Export Players
    playersElement = ET.Element('players')
    for player in self.players:
      playerElement = ET.Element('player')
      playerElement.text = player.name
      if player is self.userPlayer:
        playerElement.set('user', 'True')
      playersElement.append(playerElement)
    gameElement.append(playersElement)
    
    # Export Deck
    gameElement.append(self.deck.export())
    
    # Export hand
    handElement = self.userPlayer.has.export()
    handElement.tag = 'userhand'
    gameElement.append(handElement)
    
    # Export Turns
    historyElement = ET.Element('history')
    for turn in self.history: #TODO Presumably manual calls to new_info should get some kind of entry in history
      turnElement = ET.Element('turn')  # And there is a diferent special_info wrapper method tha also adds a line to the history.
      for key, value in turn.items():
        pairElement = ET.Element(key)
        if value is not None:
          if key == 'guess':
            for card in value:
              cardElement = ET.Element('card')
              cardElement.text = card.name
              pairElement.append(cardElement)
          elif key != 'guesser': # Don't need to save guesser info.
            # same .name syntax works for disprover, and card
            pairElement.text = value.name
        turnElement.append(pairElement)
      historyElement.append(turnElement)
    gameElement.append(historyElement)
    
    # Write the file
    with open(gamePath, 'w'):
      ET.ElementTree(gameElement).write(gamePath)
    

class ConflictingDataError(Exception):
  '''
  Clue specific exception that is raised whenever conflicting data is found in
  hands or anywhere else. Ideally once the program is stable, this will only
  happen when the user inputs invalid data, or a player makes a mistake.

  In the meantime, it can also help find bugs in the program.
  '''
  pass

def import_game(gamePath):
  '''
  Returns a game which is restored from a file.
  '''
  
  tree = ET.parse(gamePath)
  gameElement = tree.getroot()
  
  # Get the player information from the file
  players = []
  for playerElement in gameElement.find('players'):
    name = playerElement.text
    players.append(cluePlayer(name))
    if 'user' in playerElement.attrib:
      userPlayer = players[-1]
      
  # Create the deck
  deck = clueDeck(gameElement.find('deck'))
            
  # Create the game
  game = clueGame(players, userPlayer, deck)
   
  # Populate the user hand
  for cardElement in gameElement.findall('./userhand/category/card'):
    game.new_info(userPlayer, deck.get_card_by_name(cardElement.text), True)
          
  # Now recalculate the game table from the history
  for turnElement in gameElement.find('history'):
    # The guess
    guess = []
    for cardElement in turnElement.find('guess'):
      guess.append(game.deck.get_card_by_name(cardElement.text))
    # The disprover
    disprover = None
    for player in players:
      if player.name == turnElement.find('disprover').text:
        disprover = player
    # The card seen
    cardName = turnElement.find('cardSeen').text
    if cardName is None:
      cardSeen = None
    else:
      cardSeen = game.deck.get_card_by_name(cardName)
    
    # Take or pass the turn
    if guess == []:
      game.pass_turn()
    else:
      game.take_turn(guess, disprover, cardSeen = None)
  
  return game
  
  
  
  
  
  
