import xml.etree.ElementTree as ET

class clueDeck(list):
  '''
  Represents a deck of cards in the clue game.
  '''
  def __init__(self, deckPath = None):
    
    self.categories = []
    
    if deckPath is not None:      
      # Try to read a deck XML file
      with open(deckPath, 'r') as deckFile:
        deckTree = ET.parse(deckFile)
        
        for categoryElement in deckTree.findall('category'):
          self.categories.append(categoryElement.get('name'))
          for cardElement in categoryElement.findall('card'):
            newCard = clueCard(categoryElement.get('name'), cardElement.text)
            self.append(newCard)


  def append(self, card):
    '''Adds a specific card (eg. knife, rope, etc) to the deck'''
    
    if type(card) != clueCard:
      raise TypeError("Only clue cards may be added to clue decks.")
    
    if card.category not in self.categories:
      self.categories.append(card.category)  
    list.append(self, card) #TODO Should I be using super?


  def get_cards_by_category(self, category):
    '''
    Returns a list of all cards of a certain category.
    '''
    
    if category not in self.categories:
      raise ValueError("{} is not a valid category.".format(category))
    
    cards = []

    for card in self:
      if card.category == category:
        cards.append(card)

    return cards

  def export(self, path = None):
  
    '''
      Creates an element tree representation of the deck and returns it.
      
      Also saves the file to the specified path if it is specified.
    '''
  
    deckElement = ET.Element('deck')
    
    for category in self.categories:
      categoryElement = ET.Element('category')
      categoryElement.set('name', category)
      deckElement.append(categoryElement)
      
      for card in self.get_cards_by_category(category):
        categoryElement.append(card.export())        
    
    # Write the file if path is specified
    if path is not None:
      with open(path, 'wb'):
        ET.ElementTree(deckElement).write(path)
      
    return deckElement

class clueCard(object):

  def __init__(self, category, name):
    self.category = str(category)
    self.name = str(name)
  
  def export(self):  
    '''
      Creates an element tree representation of the card and returns it.
    '''
    
    element = ET.Element('card')
    element.text = self.name
    
    return element
    
    
def get_standard_deck():
  sd = clueDeck()
  
  sd.append(clueCard("Room", "Kitchen"))
  sd.append(clueCard("Room", "Ballroom"))
  sd.append(clueCard("Room", "Conservatory"))
  sd.append(clueCard("Room", "Billiard Rood"))
  sd.append(clueCard("Room", "Library"))
  sd.append(clueCard("Room", "Study"))
  sd.append(clueCard("Room", "Hall"))
  sd.append(clueCard("Room", "Lounge"))
  sd.append(clueCard("Room", "Dining Room"))
  
  sd.append(clueCard("Weapon", "Candlestick"))
  sd.append(clueCard("Weapon", "Knife"))
  sd.append(clueCard("Weapon", "Lead Pipe"))
  sd.append(clueCard("Weapon", "Revolver"))
  sd.append(clueCard("Weapon", "Rope"))
  sd.append(clueCard("Weapon", "Wrench"))
  
  sd.append(clueCard("Suspect", "Miss Scarlet"))
  sd.append(clueCard("Suspect", "Prof. Plum"))
  sd.append(clueCard("Suspect", "Mrs. Peacock"))
  sd.append(clueCard("Suspect", "Mr. Green"))
  sd.append(clueCard("Suspect", "Col. Mustard"))
  sd.append(clueCard("Suspect", "Mrs. White"))

  return sd

