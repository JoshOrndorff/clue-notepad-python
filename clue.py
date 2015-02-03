#TODO split this into seperate files and figure out how python namespaces work

class clueGame(object):

	def __init__(self, playerNames, userPlayer, nonStandardDeck = False):

		numPlayers = len(playerNames)
		self.deck = nonStandardDeck if nonStandardDeck else clueDeck()
		
		if userPlayer >= 0 and userPlayer < numPlayers:
			self.userPlayer = userPlayer
		else:
			raise ValueError, "userPlayer must be between 0 and number of players (currently {}.".format(numPlayers)

		minCardsPerHand = (self.deck.get_num_cards() - self.deck.get_num_categories()) // numPlayers
		playersWithExtraCard = (self.deck.get_num_cards() - self.deck.get_num_categories()) % numPlayers

		self.players = []
		
		for i in range(len(playerNames)):
			numCards = minCardsPerHand + 1 if i < playersWithExtraCard else minCardsPerHand
			self.players.append(cluePlayer(self.deck, numCards, playerNames[i])) #TODO Maybe a new player doesn't need the whole deck, but just the categories

		
		self.currentPlayer = 0
		self.history = []
		#TODO member attribute for correct answer?

	def pass_turn(self):
		'''
		This is a turn when the player does not make it to a room.
		'''
		self.history.append({"guesser": self.currentPlayer, "guess": None, "disprover": None})
		
		# Increment (modularly) the player for next time (and as a shortcut for the next line).
		self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
		
	def take_turn(self, guess = None, disprover = None, cardSeen = None):

		'''
			This is a normal turn where player makes a guess and disprover shows
			a card. NOTE: If no cards are shown but the game is not won because
			the guesser himself holds one of the cards guessed, disprover should
			equal the player guessing. If the game is in fact won, disprover should
			be None.

			This function or pass_turn must be called for each and every turn.
		'''

		# Ensure arguments are compatible
		if self.currentPlayer != self.userPlayer and cardSeen != None:
			raise ValueError, "Cannot specify cardSeen unless it is users turn to guess."
		if self.currentPlayer == self.userPlayer and disprover != self.currentPlayer and cardSeen == None:
			raise ValueError, "Must specify a card seen, when another player shows you a card."

		self.history.append({"guesser": self.currentPlayer, "guess": guess, "disprover": disprover})
		
		# When user sees a card note it.
		if cardSeen != None:
			self.new_info(disprover, cardSeen, True)

		# Increment (modularly) the player for next time (and as a shortcut for the next line).
		self.currentPlayer = (self.currentPlayer + 1) % len(self.players)

		# Players who didn't show, do not have any of the cards
		for player in range(self.currentPlayer, disprover): # Players who didn't show
			for card in guess: # Cards in guess
				self.new_info(player, card, False)

		# Add to disprover's disproof list unless he's known to have a card in the guess.
		if card not in self.players[disprover].hand:
			#TODO Also check to see if any cards in the disproof have known locations, and remove them from the disproof before adding it.
			self.players[disprover].disproofs.append(guess)		

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
		
		# First some validation
		category = self.deck.get_category(card)

		if type(has) != bool:
			raise TypeError, "Argument, has, must be Boolean (True or False)."
		
		# Now add the info
		if has: # Player has the card
			for currentPlayer in self.players: # All players don't have it
					currentPlayer.hand[category][card] = False
			self.players[player].hand[category][card] = True    # Change player to having it
			
		else: # Player doesn't have card
			self.players[player].hand[category][card] = False
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

#Pretty sure I don't need this, but keeping it for now just in case.	
'''
	def get_player_card_totals(self):
		totals = []
		for player in self.players:
			totals.append(player.numCards)
		return totals
'''

class cluePlayer(object):

	def __init__(self, deck, numCards, name = ""):

		self.name = str(name)
		self.numCards = numCards
		self.disproofs = []
		self.hand = {}

		# Initialize hand with categories
		for category in deck:
			self.hand[category] = {}

class clueDeck(dict):

	def __init__(self, nonStandard = False):
		if not nonStandard:
			self.make_standard_deck()

	def make_standard_deck(self):
		self["suspect"] = ["Mr. Green   ", "Col. Mustard", "Ms. Scarlet ", "Mrs. White  ", "Mrs. Peacock", "Prof. Plum  "]
		self["weapon"]  = ["Lead Pipe   ", "Wrench      ", "Revolver    ", "Knife       ", "Candlestick ", "Rope        "]
		self["room"]    = ["Kitchen     ", "Hall        ", "Dining Room ", "Ball Room   ", "Billiard Rm ", "Library     ", "Study       ", "Conservatory", "Lounge      "]
		
	def __contains__(self, card): # special method for "in" keyword
		for category in self.values():
			if card in category:
				return True
		return False
		
	def get_num_cards(self):
		size = 0
		for category in self.values():
			size += len(category)
		return size
		
	def get_num_categories(self):
		return len(self)
		
	def get_category(self, card):
		'''
		Returns the category of a given card, or raises a ValueError if the card is
		not in the deck. This way it can also be used for validation.
		'''
		
		for category in self:
			if card in self[category]:
				return category
		raise ValueError, "Card, {}, is not is the deck".format(card)
		
	def add_category(self, category, cards):
		'''
		For custom decks, adds a category of cards (eg. weapon, room. etc) and
		the cards that go in that category.
		'''
		
		if type(category) != str:
			raise TypeError, "Category must be a string"
		for card in cards:
			if type(card) != str:
				raise TypeError, "Each card must be a string"
				
		self[category] = cards
		
	#TODO def load(path):
		'''Saves current deck to specified path'''
	
	#TODO def save(path):
		'''Load a deck from the specified path'''
		# The standard deck could actually be a separate file to get loaded instead
		# of being hard coded.
