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
##     __  _______  ____  ______   ____     ____  ____  _   ____  _______
##    /  |/  / __ \/ __ \/ ____/  ( __ )   / __ )/ __ \/ | / / / / / ___/
##   / /|_/ / / / / / / / __/    / __  |  / __  / / / /  |/ / / / /\__ \ 
##  / /  / / /_/ / /_/ / /___   / /_/ /  / /_/ / /_/ / /|  / /_/ /___/ / 
## /_/  /_/\____/_____/_____/   \____/  /_____/\____/_/ |_/\____//____/  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode8(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode8, self).__init__(game, priority)
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode8_status',1)
		self.game.bonusmultiplier_mode.incrementBonusMultiplier()
		self.game.shelter_mode.refreshPlayerInfo()
		self.game.update_lamps()
		self.game.modes.remove(self)

	def mode_stopped(self):
		pass