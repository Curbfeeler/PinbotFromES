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
##    _____________   __________________     ____  ___    __  _______     __________  __ __
##   / ____/ ____/ | / /_  __/ ____/ __ \   / __ \/   |  /  |/  / __ \   / ____/ __ \/ //_/
##  / /   / __/ /  |/ / / / / __/ / /_/ /  / /_/ / /| | / /|_/ / /_/ /  /___ \/ / / / ,<   
## / /___/ /___/ /|  / / / / /___/ _, _/  / _, _/ ___ |/ /  / / ____/  ____/ / /_/ / /| |  
## \____/_____/_/ |_/ /_/ /_____/_/ |_|  /_/ |_/_/  |_/_/  /_/_/      /_____/\____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode4(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode4, self).__init__(game, priority)
			self.TotalAwarded = 0
			self.MaxAwarded = 3
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode4_status',0)
		self.game.update_lamps()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('mode4_status',1)
		self.game.lamps.centerRamp50k.disable()
		self.game.shelter_mode.refreshPlayerInfo()
		self.game.update_lamps()

	def update_lamps(self):
		print "Update Lamps: Mode 4 Center 50k"
		self.game.lamps.centerRamp50k.schedule(schedule=0xF0F0F0F0, cycle_seconds=0, now=True)

	#def sw_centerRampMiddle_active(self, sw):
		#if (self.game.utilities.get_player_stats('ball_in_play') == True):
				#self.game.utilities.score(50000)
				#self.TotalAwarded += 1
		#if (self.TotalAwarded <= self.MaxAwarded):
			#pass				
		#else:
			#self.game.modes.remove(self)
		#return procgame.game.SwitchContinue


