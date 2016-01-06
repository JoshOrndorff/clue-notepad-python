#! /usr/bin/env python

import wx
from deck import clueDeck

class DeckMakerFrame(wx.Frame):

  def __init__(self):
    wx.Frame.__init__(self, None, wx.ID_ANY, "Deck Maker")

    self.deck = clueDeck()
    # TODO: Allow loading a previously saved deck.

    # Setup the sizers
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    panelsSizer = wx.BoxSizer(wx.HORIZONTAL)

    # Create the two panels and add them to the sizer.
    self.categoryPanel = SemiPanel(self, "Category")
    self.cardPanel     = SemiPanel(self, "Card")

    self.categoryPanel.btnAdd.Bind(wx.EVT_BUTTON, self.on_add_category)
    self.cardPanel    .btnAdd.Bind(wx.EVT_BUTTON, self.on_add_card)
    self.categoryPanel.txtNew.Bind(wx.EVT_TEXT_ENTER, self.on_add_category)
    self.cardPanel.txtNew.Bind(wx.EVT_TEXT_ENTER, self.on_add_card)
    self.categoryPanel.list  .Bind(wx.EVT_LISTBOX, self.on_category_changed)

    panelsSizer.Add(self.categoryPanel, 1, wx.ALL, border = 3)
    panelsSizer.Add(self.cardPanel, 1, wx.ALL, border = 3)

    mainSizer.Add(panelsSizer, flag = wx.ALL | wx.EXPAND, border = 3)

    # Create the standard widgets
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

    self.btnWeapon = wx.Button(self, wx.ID_ANY, "Standard Weapons")
    self.btnWeapon.Bind(wx.EVT_BUTTON, self.on_standard)
    buttonSizer.Add(self.btnWeapon, 1, wx.ALL | wx.EXPAND, border = 3)

    self.btnSuspect = wx.Button(self, wx.ID_ANY, "Standard Suspects")
    self.btnSuspect.Bind(wx.EVT_BUTTON, self.on_standard)
    buttonSizer.Add(self.btnSuspect, 1, wx.ALL | wx.EXPAND, border = 3)

    self.btnRoom = wx.Button(self, wx.ID_ANY, "Standard Rooms")
    self.btnRoom.Bind(wx.EVT_BUTTON, self.on_standard)
    buttonSizer.Add(self.btnRoom, 1, wx.ALL | wx.EXPAND, border = 3)

    mainSizer.Add(buttonSizer, flag = wx.ALL | wx.EXPAND, border = 3)

    # Create the saving bit
    saveSizer = wx.BoxSizer(wx.HORIZONTAL)

    self.txtPath = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
    self.txtPath.SetValue("myDeck.deck")
    self.txtPath.Bind(wx.EVT_TEXT_ENTER, self.on_done)
    saveSizer.Add(self.txtPath, 3, flag = wx.ALL | wx.EXPAND, border = 3)

    btnDone = wx.Button(self, wx.ID_ANY, "Save Deck")
    btnDone.Bind(wx.EVT_BUTTON, self.on_done)
    saveSizer.Add(btnDone, 1, wx.ALL | wx.EXPAND, border = 3)

    mainSizer.Add(saveSizer, flag = wx.ALL | wx.EXPAND, border = 3)

    # Activate the sizer.
    self.SetSizerAndFit(mainSizer)

    # When the selected category changes, update the card side.

  def on_category_changed(self, e):
    # First remove all old entries from the card listbox
    self.cardPanel.list.Clear()
    
    # Get the new cards
    newCategory = self.categoryPanel.list.GetString(self.categoryPanel.list.GetSelection())
    cards = self.deck.get_cards_by_category(newCategory)

    # Put the new cards in the box
    for card in cards:
      self.cardPanel.list.InsertItems([card.name], 0)

  def on_standard(self, e):
    clickedButton = e.GetEventObject()

    if   clickedButton == self.btnWeapon:
      self.deck.add_category("Weapon")
      self.deck.add_card("Weapon", "Knife")
      self.deck.add_card("Weapon", "Lead Pipe")
      self.deck.add_card("Weapon", "Wrench")
      self.deck.add_card("Weapon", "Revolver")
      self.deck.add_card("Weapon", "Rope")
      self.deck.add_card("Weapon", "Candlestick")
      self.categoryPanel.list.InsertItems(["Weapon"], 0)
      
    elif clickedButton == self.btnSuspect:
      self.deck.add_category("Suspect")
      self.deck.add_card("Suspect", "Mr. Green")
      self.deck.add_card("Suspect", "Col. Mustard")
      self.deck.add_card("Suspect", "Prof. Plum")
      self.deck.add_card("Suspect", "Miss Scarlet")
      self.deck.add_card("Suspect", "Ms. White")
      self.deck.add_card("Suspect", "Mrs. Peacock")
      self.categoryPanel.list.InsertItems(["Suspect"], 0)
      
    elif clickedButton == self.btnRoom:
      self.deck.add_category("Room")
      self.deck.add_card("Room", "Hall")
      self.deck.add_card("Room", "Ball Room")
      self.deck.add_card("Room", "Billiard Room")
      self.deck.add_card("Room", "Lounge")
      self.deck.add_card("Room", "Library")
      self.deck.add_card("Room", "Conservatory")
      self.deck.add_card("Room", "Kitchen")
      self.deck.add_card("Room", "Dining Room")
      self.deck.add_card("Room", "Study")
      self.categoryPanel.list.InsertItems(["Room"], 0)

    self.categoryPanel.list.SetSelection(0)
    self.on_category_changed(None)

  def on_add_category(self, e):
    self.deck.add_category(str(self.categoryPanel.txtNew.GetValue()).capitalize())
    self.cardPanel.list.Clear()
    e.Skip() # To allow event handling to continue in the SemiPanel.

  def on_add_card(self, e):
    category = self.categoryPanel.list.GetString(self.categoryPanel.list.GetSelection())
    category = str(category)
    self.deck.add_card(category, str(self.cardPanel.txtNew.GetValue()).capitalize())
    e.Skip() # To allow event handling to continue in the SemiPanel.

  def on_done(self, e):
    # Make sure no categories are empty
    for category in self.deck.categories:
      if len(self.deck.get_cards_by_category(category)) == 0:
        wx.MessageBox("Category {} cannot be empty.".format(category))
        return

    path = self.txtPath.GetValue()
    self.deck.save(path)

class SemiPanel(wx.Panel):

  def __init__(self, parent, title):
    wx.Panel.__init__(self, parent)

    # Setup the Static Box Sizer
    box = wx.StaticBox(self, wx.ID_ANY, title)
    panelSizer = wx.StaticBoxSizer(box, wx.VERTICAL)

    # Create the list of categories
    self.list = wx.ListBox(self)
    panelSizer.Add(self.list, flag = wx.ALL | wx.EXPAND, border = 3)

    # Create the new widgets
    newSizer = wx.BoxSizer(wx.HORIZONTAL)

    lblNew = wx.StaticText(self, wx.ID_ANY, "New " + title + ":")
    newSizer.Add(lblNew, 1)

    self.txtNew = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
    self.txtNew.Bind(wx.EVT_TEXT_ENTER, self.on_add)
    newSizer.Add(self.txtNew, 2, flag = wx.EXPAND)

    self.btnAdd = wx.Button(self, wx.ID_ANY, "Add")
    self.btnAdd.Bind(wx.EVT_BUTTON, self.on_add)
    newSizer.Add(self.btnAdd, 1)

    panelSizer.Add(newSizer, flag = wx.ALL | wx.EXPAND, border = 3)

    # Activate the sizer
    self.SetSizer(panelSizer)

  def on_add(self, e):
    # Read and clear the text box.
    value = [] # InsertItems takes a list, so we will make one.
    value.append(self.txtNew.GetValue().capitalize())
    self.txtNew.SetValue("")

    # Add value to list
    self.list.InsertItems(value, 0)

    self.list.SetSelection(0)

if __name__ == "__main__":
  app = wx.App()
  frame = DeckMakerFrame()
  frame.Show()
  app.MainLoop()
