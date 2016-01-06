#! /usr/bin/env python

# TODO: merge control panel in to ClueFrame class.

import wx
import wx.grid
from cluePackage import *
from os.path import isfile
from NewGameDialog import NewGameDialog

class ClueFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Clue Score Pad", size = wx.Size(900, 600))

		# Setup all the panels
		self.controlPanel = ControlPanel(self)
		self.notebook = ClueNotebook(self)

		# Bind actions
		#self.controlPanel.btnPass  .Bind(wx.EVT_BUTTON, on_turn)
		#self.controlPanel.btnSubmit.Bind(wx.EVT_BUTTON, on_turn)

		# Setup the overall Sizer (for the two big panels)
		bigSizer = wx.BoxSizer(wx.HORIZONTAL)
		bigSizer.Add(self.controlPanel , 1, flag = wx.ALL | wx.EXPAND, border = 3)
		bigSizer.Add(self.notebook     , 1, flag = wx.ALL | wx.EXPAND, border = 3)
		self.SetSizer(bigSizer)

		# Get the game from the New Game Dialog
		dlg = NewGameDialog(self)
		dlg.MakeModal()
		dlg.SetFocus()
		dlg.Show()

		self.Centre()

'''
	def on_turn(self, e):
		if e.GetEventObject == self.controlPanel.btnPass:
			self.game.pass_turn()
		else:
			# TODO Code for take turn might be gnarly
			pass

		self.controlPanel.fill(game) # TODO: Does this recreate all the buttons? is that necessary?
'''
class ClueNotebook(wx.Notebook):

	def __init__(self, parent):
		wx.Notebook.__init__(self, parent, wx.ID_ANY)

		# First panel is the hands data
		self.handsGrid = wx.grid.Grid(self, wx.ID_ANY)
		# TODO: Consider a different grid for each category		
		self.AddPage(self.handsGrid, "Hands")

		# Second panel is the disproofs list
		disproofsPanel = wx.Panel(self)
		# TODO: Add something fancier so show the disproofs
		self.AddPage(disproofsPanel, "Disproofs")

		# Third panel is the game history
		historyPanel = wx.Panel(self)
		# TODO: Add a wx.ListBox
		self.AddPage(historyPanel, "Game History")

	def fill(self, game):
		# First the hands grid
		self.handsGrid.SetDefaultRowSize(20)
		self.handsGrid.SetDefaultColSize(80)
		self.handsGrid.CreateGrid(len(game.deck), len(game.players))

		# Set column headers
		i = 0
		for player in game.players:
			self.handsGrid.SetColLabelValue(i, player.name)
			i += 1

		# Set row headers
		i = 0
		for card in game.deck:
			self.handsGrid.SetRowLabelValue(i, card.name)
			i += 1
		
		self.handsGrid.SetCellValue(0, 0, 'wxGrid is good')

		# Next the disproofs TODO
		
		

class ControlPanel(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(200,200))

	def fill(self, game):
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# First section is for what was guessed
		self.lblTurn = wx.StaticText(self, wx.ID_ANY, "It's {}'s turn".format(game.players[0].name))
		sizer.Add(self.lblTurn, flag = wx.ALL | wx.EXPAND, border = 3)

		self.boxes = []
		guessSizer = wx.BoxSizer(wx.HORIZONTAL)
		for category in game.deck.categories:
			catSizer = wx.BoxSizer(wx.VERTICAL)
			catSizer.Add(wx.StaticText(self, wx.ID_ANY, category), flag = wx.ALL, border = 3)
			newCategory = True
			for card in game.deck.get_cards_by_category(category):
				box = wx.RadioButton(self, wx.ID_ANY, card.name, style = wx.RB_GROUP if newCategory else 0)
				newCategory = False
				box.card = card # Give each box a card attribute for the card it represents.
				self.boxes.append(box)
				catSizer.Add(box, flag = wx.ALL, border = 3)
			guessSizer.Add(catSizer, 1, flag = wx.ALL | wx.EXPAND, border = 3)

		sizer.Add(guessSizer, flag = wx.ALL | wx.EXPAND, border = 3)

		# Second section is for who showed a card
		lblShowed = wx.StaticText(self, wx.ID_ANY, "Who showed a card?")
		sizer.Add(lblShowed, flag = wx.ALL | wx.EXPAND, border = 3)

		showedSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.playerButtons = []
		for player in game.players:
			button = wx.RadioButton(self, wx.ID_ANY, player.name, style = wx.RB_GROUP if game.players.index(player) == 0 else 0)
			button.player = player
			self.playerButtons.append(button)
			showedSizer.Add(button, flag = wx.ALL | wx.EXPAND, border = 3)

		sizer.Add(showedSizer, flag = wx.ALL | wx.EXPAND, border = 3)

		# Third section is for which card was seen
		lblSeen = wx.StaticText(self, wx.ID_ANY, "Which card was seen?")
		sizer.Add(lblSeen, flag = wx.ALL | wx.EXPAND, border = 3)

		seenSizer = wx.BoxSizer(wx.HORIZONTAL)
		for i in range(len(game.deck.categories)):
			button = wx.RadioButton(self, wx.ID_ANY, "Finish this later") # TODO
			seenSizer.Add(button, flag = wx.ALL | wx.EXPAND, border = 3)

		sizer.Add(seenSizer, flag = wx.ALL | wx.EXPAND, border = 3)

		# Fourth section is for finished buttons
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.btnPass = wx.Button(self, wx.ID_ANY, "Pass Turn")
		buttonSizer.Add(btnPass, flag = wx.ALL | wx.EXPAND, border = 3)

		btnSubmit = wx.Button(self, wx.ID_ANY, "Submit Turn")
		buttonSizer.Add(btnSubmit, flag = wx.ALL | wx.EXPAND, border = 3)
		
		sizer.Add(buttonSizer, flag = wx.ALL | wx.EXPAND, border = 3)
			
		self.SetSizer(sizer)
		self.Layout()

	def on_guess_changed(self):
		#TODO Update the which card radio buttons
		pass


if __name__ == "__main__":
	app = wx.App()
	frame = ClueFrame()
	frame.Show()
	app.MainLoop()
