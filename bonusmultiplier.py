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
##     ____  ____  _   ____  _______    __  _____  ____  ______________  __    ______________ 
##    / __ )/ __ \/ | / / / / / ___/   /  |/  / / / / / /_  __/  _/ __ \/ /   /  _/ ____/ __ \
##   / __  / / / /  |/ / / / /\__ \   / /|_/ / / / / /   / /  / // /_/ / /    / // __/ / /_/ /
##  / /_/ / /_/ / /|  / /_/ /___/ /  / /  / / /_/ / /___/ / _/ // ____/ /____/ // /___/ _, _/ 
## /_____/\____/_/ |_/\____//____/  /_/  /_/\____/_____/_/ /___/_/   /_____/___/_____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class BonusMultiplier(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(BonusMultiplier, self).__init__(game, priority)
			
	def mode_started(self):
		self.update_lamps()

	def mode_stopped(self):
		pass

	def update_lamps(self):
		#### Get Multiplier ####
		self.multiplier = self.game.utilities.get_player_stats('bonus_x')

		#### Clear Lamps ####
		self.game.lamps.bonus2x.disable()
		self.game.lamps.bonus3x.disable()
		self.game.lamps.bonus4x.disable()
		self.game.lamps.bonus5x.disable()


		if (self.multiplier > 1):
			self.game.lamps.bonus2x.enable()
		if (self.multiplier > 2):
			self.game.lamps.bonus3x.enable()
		if (self.multiplier > 3):
			self.game.lamps.bonus4x.enable()
		if (self.multiplier > 4):
			self.game.lamps.bonus5x.enable()
			
	def incrementBonusMultiplier(self):
		self.multiplier = self.game.utilities.get_player_stats('bonus_x')
		if (self.multiplier <> 5):
			self.game.utilities.set_player_stats('bonus_x',self.multiplier + 1)
			self.update_lamps()
		else:
			#### Bonus Maxed ####
			pass

		
		


