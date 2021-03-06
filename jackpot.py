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
##        _____   ________ __ ____  ____  ______
##       / /   | / ____/ //_// __ \/ __ \/_  __/
##  __  / / /| |/ /   / ,<  / /_/ / / / / / /   
## / /_/ / ___ / /___/ /| |/ ____/ /_/ / / /    
## \____/_/  |_\____/_/ |_/_/    \____/ /_/     
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Jackpot(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Jackpot, self).__init__(game, priority)
			self.jackpotMaxed = False

			#### Load Mode Feature Defaults ####
			# Is this needed here since it is int he mode_started??? #
			self.jackpotHold = self.game.user_settings['Feature']['Jackpot Hold']
			self.jackpotLevel = self.game.utilities.get_player_stats('jackpot_level')

	def mode_started(self):
		#### Load Mode Feature Defaults ####
		self.jackpotHold = self.game.user_settings['Feature']['Jackpot Hold']

		if (self.jackpotHold == False):
			self.resetJackpotLevel()

	def mode_stopped(self):
		#self.cancel_delayed('dropReset')
		#self.game.utilities.set_player_stats('jackpot_level',1)
		pass

	def update_lamps(self):
		print "Update Lamps: Jackpot"
		self.jackpotLevel = self.game.utilities.get_player_stats('jackpot_level')
		print 'Jackpot Update Lamps Called'

		# Update Jackpot Value #
		for i in range(1,8):
			if (self.jackpotLevel == i):
				self.jackpotLamp = 'jackpot' + str(i)
				self.game.lamps[self.jackpotLamp].schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			else:
				self.jackpotLamp = 'jackpot' + str(i)
				self.game.lamps[self.jackpotLamp].disable()

		# Update Jackpot Flasher #
		if (self.game.utilities.get_player_stats('jackpot_lit') == True):
			self.game.coils.top3Flashers.schedule(schedule=0x000C000C, cycle_seconds=0, now=True)
			self.game.lamps.rightRampJackpot.enable()
		else:
			self.game.coils.top3Flashers.disable()
			self.game.lamps.rightRampJackpot.disable()

	def incrementJackpot(self):
		if (self.game.utilities.get_player_stats('jackpot_level') < 7):
			self.game.utilities.set_player_stats('jackpot_level',self.game.utilities.get_player_stats('jackpot_level') + 1)
			self.game.utilities.displayText(self.priority,topText='JACKPOT',bottomText='INCREASED',justify='center',seconds=2)
			self.game.sound.play('jackpot_increase')
		if (self.game.utilities.get_player_stats('jackpot_level') == 7):
			self.jackpotMaxed = True

	def resetJackpotLevel(self):
		self.game.utilities.set_player_stats('jackpot_level',1)
		self.jackpotMaxed = False
		self.update_lamps()

	def lightJackpot(self):
		if (self.game.utilities.get_player_stats('jackpot_lit') == False):
			self.game.utilities.set_player_stats('jackpot_lit',True)
			self.game.sound.play('jackpot_lit')
			self.update_lamps()
		else:
			#will put vocals here for shoot right ramp for jackpot
			pass

	def unlightJackpot(self):
		if (self.game.utilities.get_player_stats('jackpot_lit') == True):
			self.game.utilities.set_player_stats('jackpot_lit',False)
			self.update_lamps()

	def awardJackpot(self):
		self.game.sound.play('jackpot')
		self.game.utilities.shakerPulseHigh()
		self.game.lampctrlflash.play_show('jackpot', repeat=False, callback=self.game.update_lamps)
		if (self.jackpotLevel == 1):
			self.game.utilities.score(500000)
		elif (self.jackpotLevel == 2):
			self.game.utilities.score(1000000)
		elif (self.jackpotLevel == 3):
			self.game.utilities.score(1250000)
		elif (self.jackpotLevel == 4):
			self.game.utilities.score(1500000)
		elif (self.jackpotLevel == 5):
			self.game.utilities.score(1500000)
		elif (self.jackpotLevel == 6):
			self.game.utilities.score(2000000)
		elif (self.jackpotLevel == 7):
			self.game.utilities.score(2500000)
		self.unlightJackpot()
		self.resetJackpotLevel()

		