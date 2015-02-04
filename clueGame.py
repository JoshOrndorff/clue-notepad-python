from cPickle import load
from cluePlayer import cluePlayer

class clueGame(object):

	def __init__(self, playerNames, numUserPlayer, deckPath = "standard.deck"):

		#Calculate the number of players
		numPlayers = len(playerNames)

		# Load the deck
		with open(deckPath, 'rb') as input:
			self.deck = load(input)

		# Determine how many cards each player gets
		minCardsPerHand = (len(self.deck) - len(self.deck.get_categories())) // numPlayers
		playersWithExtraCard = (len(self.deck) - len(self.deck.get_categories())) % numPlayers

		#Create the players list
		self.players = []
		
		for i in range(len(playerNames)):
			numCards = minCardsPerHand + 1 if i < playersWithExtraCard else minCardsPerHand
			self.players.append(cluePlayer(playerNames[i], numCards))
		
		# Validate the user player
		if numUserPlayer >= 0 and numUserPlayer < numPlayers:
			self.userPlayer = self.players[numUserPlayer]
		else:
			raise ValueError, "userPlayer must be between 0 and number of players (currently {}.".format(numPlayers)

		# Final initializing
		self.currentPlayer = self.players[0]
		self.history = []

		#TODO member attribute for correct answer??

	def pass_turn(self):
		'''
		This is a turn when the player does not make it to a room.
		'''
		self.history.append({"guesser": self.currentPlayer.name,\
                             "guess": None,\
                         "disprover": None})

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
			raise ValueError, "Cannot specify cardSeen unless it is users turn to guess."
		if self.currentPlayer == self.userPlayer and disprover != self.currentPlayer and cardSeen == None:
			raise ValueError, "Must specify cardSeen, when another player shows you a card."
			# Should the cardSeen business be a separate call to new_info?

		self.history.append({"guesser": currentPlayer.name,\
                             "guess": guess,\
                         "disprover": disprover.name})
		
		# When user sees a card note it.
		if cardSeen != None:
			self.new_info(disprover, cardSeen, True)

		self.next_player()

		# Add to disprover's disproof list unless he's known to have a card.
		
		if card not in disprover.has:
			# Remove any cards with known locations from the guess first.
			for player in self.players:
				for card in player.has:
					if card in guess:
						guess.remove(card)
			self.players[disprover].disproofs.append(guess)

		# Players who didn't show, do not have any of the cards
		for player in self.players:
			if player == disprover:
				break
			for card in guess:
				self.new_info(player, card, False)		

		self.optimize() # Perhaps this should be moved to the new_info function

	def optimize(self):
		'''Checks for completed process of elimination results
		And also does other general maintenance'''

		#TODO: Make this work
		
		changes = False
		
		# If a player is known to have the correct number of cards, all other cards can be False.
		
		# If a player is known to not have the maximum number of cards, all other cards can be True.
		
		# Do some sanity checks. eg. at least one card in each category is not in the hands.
		
		# Finally, the recursive call
		if changes:
			self.optimize()

	def new_info(self, player, card, has):
		'''
		Updates all players' hands when new information is discovered. Generally
		this method is only used internally.
		
		Also for specifying additional information manually that does not come up
		during regular game play. For example if a card is turned up by accident,
		or there is table talk during the game.
		'''

		if type(has) != bool:
			raise TypeError, "Argument, has, must be Boolean (True or False)."
		
		# Now add the info
		if has: # Player has the card
			for currentPlayer in self.players: # All other players don't have it
				if currentPlayer != self.userPlayer:
					currentPlayer.hasnt.append(card)
			player.has.append(card)
			
		else: # Player doesn't have card
			player.hasnt.append(card)
			for disproof in self.players[player].disproofs: # Remove it from his previous disproofs
				if card in disproof:
					disproof.remove(card)
					if len(disproof) == 1: # If any disproofs contain only one card
						self.new_info(player, card, True)


	def set_user_hand(self, cards):
		'''
		Used to set the cards dealt to the user. Accepts a list of strings
		representing the cards. No validation happens here because it is done
		immediately in the new_info function.
		'''
		for card in cards:
			self.new_info(self.userPlayer, card, True)

	def next_player(self):
		'''
		Update self.curretnPlayer to be the next player
		'''
		numCurrentPlayer = self.players.index(self.currentPlayer)
		numNextPlayer = (numCurrentPlayer +1) % len(self.players)
		self.currentPlayer = self.players[numNextPlayer]

