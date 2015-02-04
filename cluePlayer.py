from clueDeck import clueDeck

class cluePlayer(object):
	'''Represents a player in the clue game.'''

	def __init__(self, name, numCards):

		self.name = str(name)
		self.numCards = numCards
		self.disproofs = []
		self.has = clueDeck() # Cards the player has
		self.hasnt = clueDeck() # Cards the player doesn't have

