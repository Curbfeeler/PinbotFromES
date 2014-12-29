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
##    _____ __ __ ______    __   _____ __  ______  ______
##   / ___// //_//  _/ /   / /  / ___// / / / __ \/_  __/
##   \__ \/ ,<   / // /   / /   \__ \/ /_/ / / / / / /   
##  ___/ / /| |_/ // /___/ /______/ / __  / /_/ / / /    
## /____/_/ |_/___/_____/_____/____/_/ /_/\____/ /_/     
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
#import scoredisplay
#from scoredisplay import AlphaScoreDisplay
import locale

class SkillshotMode(game.Mode):
	def __init__(self, game, priority):
			super(SkillshotMode, self).__init__(game, priority)
			####################
			#Mode Setup
			####################
			self.superSkillshotValue = 250000
			self.skillshotDisplayTime = 2
			self.superSkillshotSeconds = 3

	def mode_started(self):
		self.game.utilities.set_player_stats('skillshot_active',True)
		self.update_lamps()
		self.game.utilities.displayText(100,'SKILLSHOT READY','MULTIPLIER X' + str(self.game.utilities.get_player_stats('skillshot_x')),seconds=4,justify='center')
		return super(SkillshotMode, self).mode_started()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('skillshot_active',False)
		self.update_lamps()
		#self.game.collect_mode.update_lamps()
		return super(SkillshotMode, self).mode_stopped()

	def update_lamps(self):
		print "Update Lamps: Skillshot"
		if (self.game.utilities.get_player_stats('skillshot_active') == True):
			self.startSkillshotLamps()
		else:
			self.stopSkillshotLamps()
		
	def startSkillshotLamps(self):
		#self.game.lamps.gameOverBackBox.schedule(schedule=0x0000000F, cycle_seconds=0, now=False)
		#self.game.lamps.matchBackBox.schedule(schedule=0x000000F0, cycle_seconds=0, now=False)
		#self.game.lamps.ballInPlayBackBox.schedule(schedule=0x00000F00, cycle_seconds=0, now=False)
		#self.game.lamps.mouth1LeftBackBox.schedule(schedule=0x0000F000, cycle_seconds=0, now=False)
		#self.game.lamps.mouth2BackBox.schedule(schedule=0x000F0000, cycle_seconds=0, now=False)
		self.game.lamps.blue4.schedule(schedule=0xCCC00000, cycle_seconds=0, now=False)
		#self.game.coils.outholeKicker_Knocker.schedule(schedule=0x00C00000, cycle_seconds=0, now=False)

	def stopSkillshotLamps(self):
		#self.game.lamps.gameOverBackBox.disable()
		#self.game.lamps.matchBackBox.disable()
		#self.game.lamps.ballInPlayBackBox.disable()
		#self.game.lamps.mouth1LeftBackBox.disable()
		#self.game.lamps.mouth2BackBox.disable()
		self.game.lamps.blue3.disable()
		#self.game.coils.outholeKicker_Knocker.disable()

	##############################
	## Skillshot Handling Modes ##
	##############################
	def superSkillshotMissed(self):
		self.game.utilities.displayText(100,'SUPER SKILLSHOT','MISSED',seconds=self.skillshotDisplayTime,justify='center')
		self.game.modes.remove(self)

	def superSkillshotAwarded(self):
		self.game.sound.play('skillshotAwarded')
		self.game.sound.play_voice('complete_shot')
		self.game.lampctrlflash.play_show('super_skillshot', repeat=False, callback=self.game.update_lamps)
		self.game.utilities.displayText(100,'SUPER SKILLSHOT',locale.format("%d", self.superSkillshotValue * self.game.utilities.get_player_stats('skillshot_x'), grouping=True) + ' POINTS',seconds=self.skillshotDisplayTime,justify='center')
		self.game.utilities.score(self.superSkillshotValue * self.game.utilities.get_player_stats('skillshot_x'))
		self.game.utilities.set_player_stats('skillshot_x',self.game.utilities.get_player_stats('skillshot_x') + 1)
		self.game.modes.remove(self)

	def skillshotMissed(self):
		self.game.utilities.displayText(100,'SKILLSHOT','MISSED',seconds=self.skillshotDisplayTime,justify='center')
		self.game.modes.remove(self)

	def skillshotAwarded(self):
		#points will be added in the base mode
		self.game.modes.remove(self)

	###########################
	## Switch Handling Modes ##
	###########################

	def sw_outhole_closed_for_1s(self, sw):
		#### Remove Skillshot Mode ####
		self.game.modes.remove(self.game.skillshot_mode)
		return procgame.game.SwitchContinue

	def sw_vortex5k_active(self, sw):
		self.game.utilities.displayText(100,'SKILLSHOT',locale.format("%d", 5000 * self.game.utilities.get_player_stats('skillshot_x'), grouping=True) + ' POINTS',seconds=self.skillshotDisplayTime,justify='center')
		self.game.utilities.score(50000 * self.game.utilities.get_player_stats('skillshot_x'))
		self.game.lampctrlflash.play_show('skillshot', repeat=False, callback=self.game.update_lamps)
		# Spot a Random Zone
		#self.game.collect_mode.spotZone()
		self.skillshotAwarded()
		return procgame.game.SwitchContinue

	def sw_vortex20k_active(self, sw):
		self.game.utilities.displayText(100,'SKILLSHOT',locale.format("%d", 20000 * self.game.utilities.get_player_stats('skillshot_x'), grouping=True) + ' POINTS',seconds=self.skillshotDisplayTime,justify='center')
		self.game.utilities.score(25000 * self.game.utilities.get_player_stats('skillshot_x'))
		self.game.lampctrlflash.play_show('skillshot', repeat=False, callback=self.game.update_lamps)
		# Spot a Random Zone
		#self.game.collect_mode.spotZone()
		self.skillshotAwarded()
		return procgame.game.SwitchContinue

	def sw_vortex100k_active(self, sw):
		self.game.utilities.displayText(100,'SKILLSHOT',locale.format("%d", 100000 * self.game.utilities.get_player_stats('skillshot_x'), grouping=True) + ' POINTS',seconds=self.skillshotDisplayTime,justify='center')
		self.game.utilities.score(100000 * self.game.utilities.get_player_stats('skillshot_x'))
		self.game.lampctrlflash.play_show('skillshot', repeat=False, callback=self.game.update_lamps)
		# Spot a Random Zone
		#self.game.collect_mode.spotZone()
		self.skillshotAwarded()
		return procgame.game.SwitchContinue

	def sw_slingL_active(self, sw):
		self.skillshotMissed()
		return procgame.game.SwitchContinue

	#def sw_rightStandup50k_active(self, sw):
		#self.superSkillshotMissed()
		#return procgame.game.SwitchContinue

	#def sw_rightStandupHigh2_active(self, sw):
		#self.superSkillshotMissed()
		#return procgame.game.SwitchContinue

	#def sw_rightStandupLow3_active(self, sw):
		#self.superSkillshotMissed()
		#return procgame.game.SwitchContinue

	#def sw_captiveBall9_closed(self, sw):
		#self.superSkillshotAwarded()
		#return procgame.game.SwitchContinue

	#def sw_centerRampEnd_active(self, sw):
		#self.game.sound.play_voice('shoot_captive_ball')
		#self.delay(name='endSuperSkillshot',delay=self.superSkillshotSeconds,handler=self.superSkillshotMissed)
		#return procgame.game.SwitchContinue