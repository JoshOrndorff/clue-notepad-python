from cPickle import load
from cluePlayer import cluePlayer

class clueGame(object):

	def __init__(self, playerNames, numUserPlayer, deckPath = "standard.deck"):

		#Calculate the number of players
		numPlayers = len(playerNames)

		# Load the deck
		with open(deckPath, 'rb') as deckFile:
			self.deck = load(deckFile)

		# Determine how many cards each player gets
		minCardsPerHand = (len(self.deck) - len(self.deck.categories)) // numPlayers
		playersWithExtraCard = (len(self.deck) - len(self.deck.categories)) % numPlayers

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
		self.history.append({"guesser": self.currentPlayer,\
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

		self.history.append({"guesser": self.currentPlayer,\
                             "guess": guess[:],\
                         "disprover": disprover}) # Slicing guess to copy it.

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

		
		# When user sees a card note it.
		if cardSeen != None:
			self.new_info(disprover, cardSeen, True)

		# User didn't see a specific card, so add to disprover's disproof list.
		else:
			# Remove any cards with known locations from the guess first.
			import ipdb; ipdb.set_trace()
			for player in self.players:
				for card in player.has:
					if card in guess:
						guess.remove(card)
			# And if any cards remain in the guess, add it to the disproofs list
			if len(guess) > 0:
				disprover.disproofs.append(guess)	

		self.optimize()
		self.next_player()

	def optimize(self):
		'''Checks for completed process of elimination results
		And also does other general maintenance'''
		
		changes = False

		for player in self.players:		
			# If a player is known to have the correct number of cards, 
			# he does not have any other cards.
			if len(player.has) == player.numCards:
				for card in self.deck:
					if card not in player.has and card not in player.hasnt:
						self.new_info(player, card, False)
		
			# If a player is known to be without the maximum number of cards,
			# he has all remaining unknown cards.
			elif len(self.deck) - len(player.hasnt) -len(self.deck.categories) == player.numCards:
				for card in self.sdeck:
					if card not in player.has and card not in player.hasnt:
						self.new_info(player, card, True)

			# Any disproofs of length 1 are now known information.
			for disproof in player.disproofs:
				if len(disproof) == 1: # If any disproofs contain only one card
					self.new_info(player, disproof[0], True)
					player.disproofs.remove(disproof)

		# Do I need to loop through all cards with known locations and remove them from
		# disproofs? Or is it impossible for them to have gotten there in the first place.
		# No, I don't. Whenever a card location is learned it is removed from all existing disproofs.
		
		# Sanity Check: At least one card in each category is not in the hands.
		# TODO: After the program is known to work, move this to the else clause
		# of the recursive call so it is only run once per turn (to help performance).
		for category in self.deck.categories:
			for card in self.deck.get_cards_by_category(category):
				allFoundSoFar = True
				for player in self.players:
					if card in player.has:
						break
					else:
						allFoundSoFar = False
			if allFoundSoFar:
				raise ValueError, "All cards in {} category are known to be in players' hands."
		
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

		if has: # Player has the card
			for currentPlayer in self.players: # All other players don't have it
				if currentPlayer != self.userPlayer:
					currentPlayer.hasnt.append(card)
			player.has.append(card)
		#TODO When we find out where a card is, we remove it from all other players' disproofs.
		#TODO Also remove all disproofs containing the card from the players hand.
			
		else: # Player doesn't have card
			player.hasnt.append(card)
			for disproof in player.disproofs: # Remove it from his previous disproofs
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

