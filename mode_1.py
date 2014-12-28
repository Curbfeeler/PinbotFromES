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
##    _____ __  ______  __________         ___________________
##   / ___// / / / __ \/ ____/ __ \       / / ____/_  __/ ___/
##   \__ \/ / / / /_/ / __/ / /_/ /  __  / / __/   / /  \__ \ 
##  ___/ / /_/ / ____/ /___/ _, _/  / /_/ / /___  / /  ___/ / 
## /____/\____/_/   /_____/_/ |_|   \____/_____/ /_/  /____/  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode1(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode1, self).__init__(game, priority)
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode1_status',0)
		self.update_lamps()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('mode1_status',1)

	def update_lamps(self):
		print "Update Lamps: Mode 1 Jet Bumpers"
		self.game.lamps.jetLeftLamp.schedule(schedule=0x000F000F, cycle_seconds=0, now=True)
		self.game.lamps.jetRightLamp.schedule(schedule=0xF0F0F0F0, cycle_seconds=0, now=True)	
		self.game.lamps.jetTopLamp.schedule(schedule=0x0F000F00, cycle_seconds=0, now=True)	
		self.game.lamps.jetCenter.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)	

	def sw_jetTop_active(self, sw):
		self.game.sound.play('jet_super')
		self.game.utilities.acFlashPulse(coilname='raiseRamp__LowerPFTop1Flasher',pulsetime=60)
		self.game.utilities.score(5000)
		return procgame.game.SwitchStop

	def sw_jetMiddle_active(self, sw):
		self.game.sound.play('jet_super')
		self.game.utilities.acFlashPulse(coilname='raiseRamp__LowerPFTop1Flasher',pulsetime=60)
		self.game.utilities.score(5000)
		return procgame.game.SwitchStop

	def sw_jetBottom_active(self, sw):
		self.game.sound.play('jet_super')
		self.game.utilities.acFlashPulse(coilname='raiseRamp__LowerPFTop1Flasher',pulsetime=60)
		self.game.utilities.score(5000)
		return procgame.game.SwitchStop
		
		


