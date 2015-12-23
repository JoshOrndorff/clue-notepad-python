from cPickle import dump

class clueDeck(list):
	'''
	Represents a deck of cards in the clue game.
	'''
	def __init__(self):
		self.categories = []

	def add_category(self, category, names):
		'''
		For custom decks, adds a category of cards (eg. weapon, room. etc) and
		the cards that go in that category.
		'''

		if category in self.categories:
			raise ValueError, "Category already exists in deck."
		elif type(category) != str:
			raise TypeError, "Category must be a string."

		self.categories.append(category)

		for name in names:
			self.add_card(category, name)

	def add_card(self, category, name):
		if category not in self.categories:
			raise ValueError, "Not a valid category. Add category first."

		if type(name) != str:
			raise TypeError, "Each card name must be a string"

		self.append(clueCard(category, name))


	def get_cards_by_category(self, category):
		'''
		Returns a list of all cards of a certain category
		'''
		if category not in self.categories:
			raise ValueError, "Not a valid category."

		cards = []

		for card in self:
			if card.category == category:
				cards.append(card)
		return cards

	def save(self, path):
		with open(path, 'wb') as output:
			dump(self, output, -1)

class clueCard(object):

	def __init__(self, category, name):
		self.category = str(category)
		self.name = str(name)

