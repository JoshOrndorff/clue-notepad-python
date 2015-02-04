from cPickle import dump

class clueDeck(list):
	'''
	Represents a deck of cards in the clue game.
	'''
		
	def get_categories(self):
		categories = []
		for card in self:
			if card.category not in categories:
				categories.append(card.category)
		return categories

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
			self.append(clueCard(category, card))

	def save(self, path):
		with open(path, 'wb') as output:
			dump(self, output, -1)

class clueCard(object):

	def __init__(self, category, name):
		self.category = str(category)
		self.name = str(name)
	
