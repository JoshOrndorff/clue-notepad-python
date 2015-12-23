import wx
from cluePackage import *

class NewGameDialog(wx.Frame):
	# TODO: This should probably be a dialog, but I was getting corrupted double
	# linked list error, so as a workaround it is a frame.
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "Setup A New Game")
		
		self.parent = parent

		# Setup the two panels
		self.playersPanel = PlayersPanel(self)
		self.userHandPanel = UserHandPanel(self)
		self.userHandPanel.Hide() # Initially only show the players panel
		
		# Setup a sizer so the panels fill the dialog
		bigSizer = wx.BoxSizer(wx.HORIZONTAL)
		bigSizer.Add(self.playersPanel , 1, flag = wx.ALL | wx.EXPAND, border = 3)
		bigSizer.Add(self.userHandPanel, 1, flag = wx.ALL | wx.EXPAND, border = 3)
		self.SetSizer(bigSizer)
		
		# Bind events for switching from intro stuff to main panels.
		self.playersPanel .btnDone.Bind(wx.EVT_BUTTON, self.on_players_done)
		self.userHandPanel.btnDone.Bind(wx.EVT_BUTTON, self.on_user_hand_done)	
		
		self.Centre()	
		
		
	def on_players_done(self, e):
		# Gather values from panel
		names = []
		for i in range(6):
			name = self.playersPanel.nameBoxes[i].GetValue().strip()
			if name != "":
				names.append(name)
			if self.playersPanel.meButtons[i].GetValue():
				numUserPlayer = len(names) - 1
				
		# Ensure two players have been entered.
		if len(names) < 2:
			wx.MessageBox("You must enter at least two players.")
			return
		
		# Make the game
		self.parent.game = clueGame(names, numUserPlayer, "standard.deck") # TODO: allow non-standard deck
		
		# Fill and activate the next panel
		self.playersPanel.Hide()
		self.userHandPanel.fill(self.parent.game.deck)
		self.userHandPanel.Show()
		
		self.Layout()

	def on_user_hand_done(self, e):
		hand = []
		numCards = self.parent.game.userPlayer.numCards
		
		for box in self.userHandPanel.boxes:
			if box.GetValue():
				hand.append(box.card)
		
		# Validate number of cards
		if len(hand) != numCards:
			wx.MessageBox("You must select exactly {} cards.".format(numCards))
			return
			
		# Set the hand
		for category in self.parent.game.deck.categories:
			allFoundSoFar = True
			for card in self.parent.game.deck.get_cards_by_category(category):
				if card in hand:
					continue
				else:
					allFoundSoFar = False
			if allFoundSoFar:
				wx.MessageBox("You may not select every card from any category")
				return
				
		# That's all; fill and return to the main Frame
		self.parent.controlPanel.fill(self.parent.game)
		self.parent.notebook    .fill(self.parent.game)
		self.MakeModal(False)
		self.Destroy()


class PlayersPanel(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY)

		self.nameBoxes = []
		self.meButtons = []
		
		sizer = wx.GridSizer(8, 3, 3, 3)
		
		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Enter each player's name and select yourself."))
		sizer.AddMany([(0,0), (0,0)]) # Blank spaces
		
		# Make six rows for names
		for i in range(6):
			# Label
			lblName = wx.StaticText(self, wx.ID_ANY,"Player {}'s name:".format(i))
			sizer.Add(lblName, flag = wx.ALIGN_RIGHT)
			
			# Textbox
			nameBox = wx.TextCtrl(self)
			nameBox.Bind(wx.EVT_TEXT, self.on_text_changed)
			self.nameBoxes.append(nameBox)
			sizer.Add(nameBox, flag = wx.EXPAND)
			
			# Radio Button
			meButton = wx.RadioButton(self, wx.ID_ANY, "This is me.",\
				style = wx.RB_GROUP if i == 0 else 0)
			meButton.Disable()
			self.meButtons.append(meButton)
			sizer.Add(meButton)
			
		sizer.AddMany([(0,0), (0,0)]) # Blank spaces

		self.btnDone = wx.Button(self, wx.ID_ANY, "Done")
		sizer.Add(self.btnDone)
		
		self.SetSizer(sizer)
		
	def on_text_changed(self, e):
		# Figure out which one changed
		changedBox = e.GetEventObject()
		value = changedBox.GetValue()
		i = self.nameBoxes.index(changedBox)
		
		if value == "":
			self.meButtons[i].Disable()
			if self.meButtons[i].GetValue():
				# Check a different one
				for meButton in self.meButtons:
					if meButton.IsEnabled():
						meButton.SetValue(True)
						break
		else:
			self.meButtons[i].Enable()
		
class UserHandPanel(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		
		# Make simple widgets and placehold for options that will be filled later.
		directions = wx.StaticText(self, wx.ID_ANY, "Which cards are in your hand?")
		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btnDone = wx.Button(self, wx.ID_ANY, "Done")
		
		# Make super sizer and add items to it
		superSizer = wx.BoxSizer(wx.VERTICAL)
		superSizer.Add(directions    , 0, flag = wx.ALL | wx.EXPAND, border = 3)
		superSizer.Add(self.mainSizer, 1, flag = wx.ALL | wx.EXPAND, border = 3)
		superSizer.Add(self.btnDone  , 0, flag = wx.ALL | wx.EXPAND, border = 3)
		self.SetSizer(superSizer)
		
	def fill(self, deck):
		self.boxes = []
		for category in deck.categories:
			catSizer = wx.BoxSizer(wx.VERTICAL)
			catSizer.Add(wx.StaticText(self, wx.ID_ANY, category), flag = wx.ALL, border = 3)
			for card in deck.get_cards_by_category(category):
				box = wx.CheckBox(self, wx.ID_ANY, card.name)
				box.card = card # Give each box a card attribute for the card it represents.
				self.boxes.append(box)
				catSizer.Add(box, flag = wx.ALL, border = 3)
			self.mainSizer.Add(catSizer, 1, flag = wx.ALL | wx.EXPAND, border = 3)

