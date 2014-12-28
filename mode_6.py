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
##    _____ __  ______  __________     _____ ____  _____   ___   ____________ 
##   / ___// / / / __ \/ ____/ __ \   / ___// __ \/  _/ | / / | / / ____/ __ \
##   \__ \/ / / / /_/ / __/ / /_/ /   \__ \/ /_/ // //  |/ /  |/ / __/ / /_/ /
##  ___/ / /_/ / ____/ /___/ _, _/   ___/ / ____// // /|  / /|  / /___/ _, _/ 
## /____/\____/_/   /_____/_/ |_|   /____/_/   /___/_/ |_/_/ |_/_____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode6(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode6, self).__init__(game, priority)
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode6_status',0)
		self.game.update_lamps()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('mode6_status',1)

	def update_lamps(self):
		print "Update Lamps: Mode 6 mouth4BackBox"
		self.game.lamps.inlaneRightmouth4BackBox.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)
		self.game.lamps.mouth4BackBox.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)		

	#def sw_mouth4BackBox_active(self, sw):
		#self.game.utilities.score(3000)
		#self.game.utilities.acFlashPulse(coilname='dropTargetReset_RightInsertBDFlasher',pulsetime=40)
		#self.game.sound.play('super_mouth4BackBox')
		#return procgame.game.SwitchStop

	#def sw_rightOutsideReturn_active(self, sw):
		#return procgame.game.SwitchContinue


