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
		
		if type(category) != str:
			raise TypeError, "Category must be a string"

		for name in names:
			if type(name) != str:
				raise TypeError, "Each card must be a string"
			self.append(clueCard(category, name))

		self.categories.append(category)

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

# Temporary code to make standard deck
if __name__ == "__main__":
	deck = clueDeck()

	deck.add_category("Weapon", ["Knife", "Lead Pipe", "Wrench", "Revolver",\
	                             "Rope", "Candlestick"])
	deck.add_category("Room", ["Hall", "Ball Room", "Billiard Room", "Lounge",\
	                           "Library", "Conservatory", "Kitchen",\
	                           "Dining Room", "Study"])
	deck.add_category("Suspect", ["Mr. Green", "Col. Mustard", "Prof. Plum",\
	                              "Miss Scarlet", "Ms. White", "Mrs. Peacock"])
	deck.save("standard.deck")



