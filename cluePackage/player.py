from deck import clueDeck

class cluePlayer(object):
	'''Represents a player in the clue game.'''

	def __init__(self, name):

		self.name = str(name)
		self.numCards = None
		self.disproofs = []
		self.has   = [] # Cards the player has
		self.hasnt = [] # Cards the player doesn't have

