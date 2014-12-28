#################################################################################
##____ ___ _   _ ____   ___ _____   ____    ___                      
#|  _ \_ _| \ | | __ ) / _ \_   _| |___ \  / _ \                     
#| |_) | ||  \| |  _ \| | | || |     __) || | | |                    
#|  __/| || |\  | |_) | |_| || |    / __/ | |_| |                    
#|_|__|___|_|_\_|____/_\___/_|_| __|_____(_)___/_____ ___ ___  _   _ 
#|  _ \     |  _ \ / _ \ / ___| | ____|  _ \_ _|_   _|_ _/ _ \| \ | |
#| |_) |____| |_) | | | | |     |  _| | | | | |  | |  | | | | |  \| |
#|  __/_____|  _ <| |_| | |___  | |___| |_| | |  | |  | | |_| | |\  |
#|_|        |_| \_\\___/ \____| |_____|____/___| |_| |___\___/|_| \_|
##                                                                   
## A P-ROC Project by Dan Myers, Copyright 2013-2014
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
## Thanks to Scott Danesi for his Earthshaker Project, which is my starting point
#################################################################################

#################################################################################
##     ____  ____  ____  ____     _________    ____  _______________________
##    / __ \/ __ \/ __ \/ __ \   /_  __/   |  / __ \/ ____/ ____/_  __/ ___/
##   / / / / /_/ / / / / /_/ /    / / / /| | / /_/ / / __/ __/   / /  \__ \ 
##  / /_/ / _, _/ /_/ / ____/    / / / ___ |/ _, _/ /_/ / /___  / /  ___/ / 
## /_____/_/ |_|\____/_/        /_/ /_/  |_/_/ |_|\____/_____/ /_/  /____/  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class DropTargets(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(DropTargets, self).__init__(game, priority)
			self.dropTargetHurryUpEnabled = False

			#### Load Mode Feature Defaults ####
			#self.dropTargetHurryUpTime = self.game.user_settings['Feature']['Drop Target Time']

	def mode_started(self):
		self.resetDrops()

	def resetDrops(self):
		self.dropTargetHurryUpEnabled = False
		if (self.game.switches.upperDrop.is_active() == True or self.game.switches.midDrop.is_active() == True or self.game.switches.lowerDrop.is_active() == True):
			self.game.utilities.acCoilPulse('dropTargetReset_RightInsertBDFlasher')

	def checkForCompletion(self):
		if (self.game.switches.upperDrop.is_active() == True and self.game.switches.midDrop.is_active() == True and self.game.switches.lowerDrop.is_active() == True):
			self.dropsCompleted()

	def dropsCompleted(self):
		#self.game.jackpot_mode.incrementJackpot()
		#self.game.jackpot_mode.update_lamps()
		#if (self.game.jackpot_mode.jackpotMaxed == False):
			#self.resetDrops()
		self.resetDrops()

	def dropsSwitchHandler(self):
		self.game.sound.play('drop')
		self.checkForCompletion()

	def sw_upperDrop_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop

	def sw_midDrop_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop

	def sw_lowerDrop_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop
