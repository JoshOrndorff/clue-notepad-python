import xml.etree.ElementTree as ET

class clueDeck(list):
  '''
  Represents a deck of cards in the clue game.
  '''
  def __init__(self, deckPath = None):
    self.categories = []
    
    if deckPath == None: # Creating a new blank deck
      return
      
    # Try to read a deck XML file
    with open(deckPath, 'r') as deckFile:
      deckTree = ET.parse(deckFile)
      
      for categoryElement in deckTree.findall('category'):
        self.add_category(categoryElement.get('name'))
        for cardElement in categoryElement.findall('card'):
          self.add_card(categoryElement.get('name'), cardElement.text)
    

  def add_category(self, category):
    '''Adds a category of cards (eg. weapon, room, etc) to a new deck.'''

    if category in self.categories:
      raise ValueError("Category, {}, already exists in deck.".format(category))
    elif type(category) != str:
      raise TypeError("Category must be a string.")

    self.categories.append(category)

  def add_card(self, category, name):
    '''Adds a specific card (eg. knife, rope, etc) to a category'''
    
    if category not in self.categories:
      raise ValueError("Not a valid category. Add category first.")

    if type(name) != str:
      raise TypeError("Each card name must be a string")

    self.append(clueCard(category, name))


  def get_cards_by_category(self, category):
    '''
    Returns a list of all cards of a certain category
    '''
    if category not in self.categories:
      raise ValueError("{} is not a valid category.".format(category))

    cards = []

    for card in self:
      if card.category == category:
        cards.append(card)
    return cards

  def save(self, path):
  
    '''Saves a deck to an XML file for later use'''
  
    deckElement = ET.Element('deck')
    
    for category in self.categories:
      categoryElement = ET.Element('category')
      categoryElement.set('name', category)
      deckElement.append(categoryElement)
      
      for card in self.get_cards_by_category(category):
        cardElement = ET.Element('card')
        cardElement.text = card.name
        categoryElement.append(cardElement)        
    
    # Write the file
    with open(path, 'wb') as output:
      ET.ElementTree(deckElement).write(path)

class clueCard(object):

  def __init__(self, category, name):
    self.category = str(category)
    self.name = str(name)

def get_standard_deck():
  sd = clueDeck()
  
  sd.add_category("Room")
  sd.add_card("Room", "Kitchen")
  sd.add_card("Room", "Ballroom")
  sd.add_card("Room", "Conservatory")
  sd.add_card("Room", "Billiard Rood")
  sd.add_card("Room", "Library")
  sd.add_card("Room", "Study")
  sd.add_card("Room", "Hall")
  sd.add_card("Room", "Lounge")
  sd.add_card("Room", "Dining Room")
  
  sd.add_category("Weapon")
  sd.add_card("Weapon", "Candlestick")
  sd.add_card("Weapon", "Knife")
  sd.add_card("Weapon", "Lead Pipe")
  sd.add_card("Weapon", "Revolver")
  sd.add_card("Weapon", "Rope")
  sd.add_card("Weapon", "Wrench")
  
  sd.add_category("Suspect")
  sd.add_card("Suspect", "Miss Scarlet")
  sd.add_card("Suspect", "Prof. Plum")
  sd.add_card("Suspect", "Mrs. Peacock")
  sd.add_card("Suspect", "Mr. Green")
  sd.add_card("Suspect", "Col. Mustard")
  sd.add_card("Suspect", "Mrs. White")

  return sd

