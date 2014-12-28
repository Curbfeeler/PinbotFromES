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
##    _________    ____  ___________    ________   _________    ____  _   _______    _____    __ 
##   / ____/   |  / __ \/_  __/  _/ |  / / ____/  / ____/   |  / __ \/ | / /  _/ |  / /   |  / / 
##  / /   / /| | / /_/ / / /  / / | | / / __/    / /   / /| | / /_/ /  |/ // / | | / / /| | / /  
## / /___/ ___ |/ ____/ / / _/ /  | |/ / /___   / /___/ ___ |/ _, _/ /|  // /  | |/ / ___ |/ /___
## \____/_/  |_/_/     /_/ /___/  |___/_____/   \____/_/  |_/_/ |_/_/ |_/___/  |___/_/  |_/_____/
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode9(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode9, self).__init__(game, priority)
			self.captiveLevel = 0
			
	def mode_started(self):
		self.game.modes.remove(self.game.skillshot_mode)
		self.game.utilities.set_player_stats('mode9_status',0)
		self.game.shelter_mode.refreshPlayerInfo()
		self.game.update_lamps()
		self.incrementCaptiveLevel()
		self.delay(delay=20,handler=self.game.modes.remove,param=self)
		

	def mode_stopped(self):
		self.captiveLevel = 0
		self.game.lamps.gameOverBackBox.disable()
		self.game.lamps.matchBackBox.disable()
		self.game.lamps.ballInPlayBackBox.disable()
		self.game.lamps.mouth1LeftBackBox.disable()
		self.game.lamps.mouth2BackBox.disable()
		self.game.utilities.set_player_stats('mode9_status',1)
		self.cancel_delayed('increment')


	def update_lamps(self):
		self.game.lamps.gameOverBackBox.disable()
		self.game.lamps.matchBackBox.disable()
		self.game.lamps.ballInPlayBackBox.disable()
		self.game.lamps.mouth1LeftBackBox.disable()
		self.game.lamps.mouth2BackBox.disable()

		if self.captiveLevel >= 1:
			self.game.lamps.gameOverBackBox.enable()
		if self.captiveLevel >= 2:
			self.game.lamps.matchBackBox.enable()
		if self.captiveLevel >= 3:
			self.game.lamps.ballInPlayBackBox.enable()
		if self.captiveLevel >= 4:
			self.game.lamps.mouth1LeftBackBox.enable()
		if self.captiveLevel == 5:
			self.game.lamps.mouth2BackBox.enable()

	def incrementCaptiveLevel(self):
		if (self.captiveLevel < 5):
			self.captiveLevel += 1
		else:
			self.captiveLevel = 1
		self.update_lamps()
		self.delay(name='increment',delay=.2,handler=self.incrementCaptiveLevel)

	def awardCaptiveValue(self):
		self.cancel_delayed('increment')
		if self.captiveLevel == 1:
			self.game.utilities.score(25000)
			self.game.lamps.gameOverBackBox.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 2:
			self.game.utilities.score(50000)
			self.game.lamps.matchBackBox.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 3:
			self.game.utilities.score(100000)
			self.game.lamps.ballInPlayBackBox.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 4:
			self.game.utilities.score(150000)
			self.game.lamps.mouth1LeftBackBox.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 5:
			self.game.utilities.score(200000)
			self.game.lamps.mouth2BackBox.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)

		self.game.sound.play('captive_carnival')
		self.delay(delay=.1,handler=self.game.sound.play,param='captive_carnival')
		self.delay(delay=.2,handler=self.game.sound.play,param='captive_carnival')
		self.delay(delay=.4,handler=self.game.sound.play_voice,param='complete_shot')
		self.delay(name='increment',delay=.6,handler=self.incrementCaptiveLevel)
		

	#def sw_captiveBall9_closed(self, sw):
		#self.awardCaptiveValue()
		#return procgame.game.SwitchStop