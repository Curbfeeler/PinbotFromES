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
##     ____  ____  _   ____  _______
##    / __ )/ __ \/ | / / / / / ___/
##   / __  / / / /  |/ / / / /\__ \ 
##  / /_/ / /_/ / /|  / /_/ /___/ / 
## /_____/\____/_/ |_/\____//____/  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Bonus(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Bonus, self).__init__(game, priority)
			# Settings Variables #
			self.delay_time = 1.5

			# System Variables #
			self.total_value = 0
			

	def mode_started(self):

		# Disable the flippers
		self.game.coils.flipperEnable.disable()
		self.game.sound.stop_music()
		self.game.utilities.disableGI()

		#### Disable All Lamps ####
		for lamp in self.game.lamps:
			lamp.disable()

	def mode_stopped(self):
		# Enable the flippers
		self.game.coils.flipperEnable.enable() # Can possibly remove this and let the "Ball Start" function handle it.
		#self.game.sound.stop_music() # Only needed if using background Bonus music
		self.game.utilities.enableGI()

	def calculate(self,callback):
		#self.game.sound.play_music('bonus'+ str(self.game.ball), loops=1)
		self.callback = callback
		self.total_value = self.game.utilities.get_player_stats('bonus') * self.game.utilities.get_player_stats('bonus_x')

	def setMyDisplayContent(self):
		#### Script List Variable Initialization ####
		script=[]

		script.append({'top':'TRANSITION 0','bottom':'TRANSITION 0','timer':2,'transition':0})
		script.append({'top':'TRANSITION 1','bottom':'TRANSITION 1','timer':8,'transition':1})
		script.append({'top':'TRANSITION 2','bottom':'TRANSITION 2','timer':2,'transition':2})
		script.append({'top':'TRANSITION 3','bottom':'TRANSITION 3','timer':2,'transition':3})
		script.append({'top':'TRANSITION 4','bottom':'TRANSITION 4','timer':2,'transition':4})
		#Cancel any score display scripts that may be running
		self.game.alpha_score_display.cancel_script()
		self.game.alpha_score_display.set_script(script)

	def dummy_handler(self):
		print 'sat here two seconds...'
		pass

	def multiplier(self):
		self.game.utilities.displayText(priority=self.priority,topText='X'+str(self.game.utilities.get_player_stats('bonus_x')).upper(),bottomText=locale.format("%d", self.total_value, True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_features')
		self.game.lampctrlflash.play_show('bonus_feat_right', repeat=False)
		self.game.utilities.setBackboxLED(255,0,0,pulsetime=100)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.total)

	def total(self):
		self.game.utilities.score(self.total_value) # this should upadte the player score in question
		self.game.utilities.displayText(priority=self.priority,topText=locale.format("%d", self.game.utilities.currentPlayerScore(), True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_total')
		#self.game.utilities.acFlashSchedule(coilname='lowerRamp_EnergyFlashers',schedule=0x00CCCCCC, cycle_seconds=1, now=True)
		#self.game.utilities.acFlashSchedule(coilname='outholeKicker_Knocker',schedule=0x00CCCCCC, cycle_seconds=1, now=True)
		#self.game.coils.backboxLightingB.schedule(schedule=0x00CCCCCC, cycle_seconds=1, now=True)
		self.game.lampctrlflash.play_show('bonus_total', repeat=False)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.finish)		

	def finish(self):
		self.game.sound.stop_music()
		self.callback()
		#self.game.base_mode.end_ball()