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
##   _____ _    _ ______  _____ _______ 
##  / ____| |  | |  ____|/ ____|__   __|
## | |    | |__| | |__  | (___    | |   
## | |    |  __  |  __|  \___ \   | |   
## | |____| |  | | |____ ____) |  | |   
##  \_____|_|  |_|______|_____/   |_|   
##                                     
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Chest(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Chest, self).__init__(game, priority)
			self.chestFilled = False

	def mode_started(self):
		#### Load Mode Feature Defaults ####
		self.chestHold = self.game.user_settings['Feature']['Chest Hold']

		if (self.chestHold == False):
			self.resetChest()

		for switch in self.game.switches:
					if switch.name.find('chestMatrix', 0) != -1:
						self.add_switch_handler(name=switch.name, event_type='active', \
					                                delay=0.01, handler=self.chestMatrixSwitches)			
	def mode_stopped(self):
		#self.cancel_delayed('dropReset')
		#self.game.utilities.set_player_stats('jackpot_level',1)
		pass

	def update_lamps(self):
		print "update_lamps"
		pass

	def resetChest(self):
		print "resetChest"
		pass

	def sw_chestMatrix50_active(self, sw):
			print "hit 50 in Chest Mode"	
			return procgame.game.SwitchContinue

	def chestMatrixSwitches(self,sw):
		self.game.score(100)
		#self.game.bonus(1)
		#self.game.lamps[sw.name].enable()
		#self.game.effects.flickerOn(sw.name)   # switch on the lamp at the target
		self.game.lamps.chestMatrix11.enable()
		#self.game.current_player().chestRowMatrix[sw.name]=True
		if sum([i for i in self.game.current_player().chestRowMatrix.values()])==5:
			pass
		#self.game.lamps.notUsed11.enable()


#Switch Denotation
#chestMatrix01 #Row 0, Col 1, Yellow Switch - Hori
#chestMatrix02 #Row 0, Col 2, Blue Switch - Hori
#chestMatrix03 #Row 0, Col 3, Orange Switch - Hori
#chestMatrix04 #Row 0, Col 4, Green Switch - Hori
#chestMatrix05 #Row 0, Col 5, Red Switch - Hori
#chestMatrix10 #Row 1, Col 0, Yellow Switch - Vert
#chestMatrix20 #Row 2, Col 0, Yellow Switch - Vert
#chestMatrix30 #Row 3, Col 0, Yellow Switch - Vert
#chestMatrix40 #Row 4, Col 0, Yellow Switch - Vert
#chestMatrix50 #Row 5, Col 0, Yellow Switch - Vert
#	Name	        row	col	in code
#	chestMatrix	1	1	chestMatrix11
#	chestMatrix	1	2	chestMatrix12
#	chestMatrix	1	3	chestMatrix13
#	chestMatrix	1	4	chestMatrix14
#	chestMatrix	1	5	chestMatrix15
#	chestMatrix	2	1	chestMatrix21
#	chestMatrix	2	2	chestMatrix22
#	chestMatrix	2	3	chestMatrix23
#	chestMatrix	2	4	chestMatrix24
#	chestMatrix	2	5	chestMatrix25
#	chestMatrix	3	1	chestMatrix31
#	chestMatrix	3	2	chestMatrix32
#	chestMatrix	3	3	chestMatrix33
#	chestMatrix	3	4	chestMatrix34
#	chestMatrix	3	5	chestMatrix35
#	chestMatrix	4	1	chestMatrix41
#	chestMatrix	4	2	chestMatrix42
#	chestMatrix	4	3	chestMatrix43
#	chestMatrix	4	4	chestMatrix44
#	chestMatrix	4	5	chestMatrix45
#	chestMatrix	5	1	chestMatrix51
#	chestMatrix	5	2	chestMatrix52
#	chestMatrix	5	3	chestMatrix53
#	chestMatrix	5	4	chestMatrix54
#	chestMatrix	5	5	chestMatrix55
