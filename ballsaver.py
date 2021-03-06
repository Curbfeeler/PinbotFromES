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
##     ____  ___    __    __       _____ ___ _    ____________ 
##    / __ )/   |  / /   / /      / ___//   | |  / / ____/ __ \
##   / __  / /| | / /   / /       \__ \/ /| | | / / __/ / /_/ /
##  / /_/ / ___ |/ /___/ /___    ___/ / ___ | |/ / /___/ _, _/ 
## /_____/_/  |_/_____/_____/   /____/_/  |_|___/_____/_/ |_|  
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc

class BallSaver(game.Mode):
	def __init__(self, game, priority):
			super(BallSaver, self).__init__(game, priority)

			self.ballSaverTime = 15 #This needs to be moved to pull from the configuration file
			self.ballSaverGracePeriodThreshold = 3 #This needs to be moved to pull from the configuration file
			self.ballSaveLampsActive = True #Probably should move to mode started instead of init...
			self.ballSavedEarly = False 

	############################
	#### Standard Functions ####
	############################
	def mode_started(self):
		self.cancel_delayed('stopballsavelamps')
		self.game.utilities.set_player_stats('ballsave_active',True)
		self.ballSaveLampsActive = True
		self.game.trough.ball_save_active = True
		self.update_lamps()

	def mode_stopped(self):
		self.game.trough.ball_save_active = False
		return super(BallSaver, self).mode_stopped()

	def update_lamps(self):
		print "Update Lamps: Ball Saver"
		if (self.game.utilities.get_player_stats('ballsave_active') == True and self.ballSaveLampsActive == True):
			self.startBallSaverLamps()
		else:
			self.stopBallSaverLamps()
		
	def startBallSaverLamps(self):
		self.game.lamps.shootAgain.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=False)

	def startBallSaverLampsWarning(self):
		self.game.lamps.shootAgain.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)

	def stopBallSaverLamps(self):
		self.ballSaveLampsActive = False
		self.game.lamps.shootAgain.disable()

	def stopBallSaverMode(self):
		self.game.utilities.set_player_stats('ballsave_active',False)
		self.stopBallSaverTimers()
		self.update_lamps()
		self.game.modes.remove(self)

	def startBallSaverTimers(self):
		self.game.utilities.set_player_stats('ballsave_timer_active',True)
		self.delay(name='ballsaver',delay=self.ballSaverTime,handler=self.stopBallSaverMode)
		self.delay(name='stopballsavelamps',delay=self.ballSaverTime - self.ballSaverGracePeriodThreshold,handler=self.stopBallSaverLamps)

	def stopBallSaverTimers(self):
		self.game.utilities.set_player_stats('ballsave_timer_active',False)
		self.cancel_delayed('stopballsavelamps')
		self.cancel_delayed('ballsaver')

	def kickBallToTrough(self):
		self.game.utilities.acCoilPulse(coilname='outholeKicker_Knocker',pulsetime=50)

	def kickBallToShooterLane(self):
		self.game.utilities.acCoilPulse(coilname='feedShooter_UpperPFFLash',pulsetime=100)

	def saveBall(self):
		
                                                   #topLeft7='XXXXXXX', topRight7='XXXXXXX',bottomLeft7='8888888',bottomRight7='8888888'
		self.game.utilities.displayText(199,topLeft7='BALL', topRight7='SAVED',bottomLeft7='8888888',bottomRight7='8888888',seconds=3,justify='center')

		#Stop Skillshot
		self.game.modes.remove(self.game.skillshot_mode)
		#Start Chest Mode
		#self.game.modes.remove(self.game.chest_mode)
		#self.game.modes.add(self.game.chest_mode)

		self.game.sound.play('ball_saved')

		#These are from the original code
		#self.kickBallToTrough()
		#self.kickBallToShooterLane()
		self.game.trough.launch_balls(num=1)
		self.stopBallSaverMode()

	def saveBallEarly(self): #Need to work on this...
                                                   #topLeft7='XXXXXXX', topRight7='XXXXXXX',bottomLeft7='8888888',bottomRight7='8888888'
		self.game.utilities.displayText(199,topLeft7='BALL', topRight7='SAVED',bottomLeft7='8888888',bottomRight7='8888888',seconds=3,justify='center')

		#Stop Skillshot
		self.game.modes.remove(self.game.skillshot_mode)
		#Start Chest Mode
		#self.game.modes.remove(self.game.chest_mode)
		#self.game.modes.add(self.game.chest_mode)

		self.game.sound.play('ball_saved')

		#These are from the original code
		#self.kickBallToTrough()
		#self.kickBallToShooterLane()
		self.game.trough.launch_balls(num=1)
		self.stopBallSaverMode()

	#def sw_outhole_closed_for_1s(self, sw):
		#if (self.game.utilities.get_player_stats('ballsave_active') == True):
			#self.game.utilities.log('BALLSAVE - Outhole closed for 1s - SwitchStop','info')
			#self.saveBall()
			#return procgame.game.SwitchStop
		#else:
			#self.game.utilities.log('BALLSAVE NOT ACTIVE - Outhole closed for 1s - SwitchContinue','info')
			#return procgame.game.SwitchContinue

	#def sw_outhole_closed(self, sw):
		#if (self.game.utilities.get_player_stats('ballsave_active') == True):
			#self.game.utilities.log('BALLSAVE - Ouhole closed - SwitchStop - Disabling timers','info')
			#self.cancel_delayed('ballsaver')
			#return procgame.game.SwitchStop
		#else:
			#self.game.utilities.log('BALLSAVE - Ouhole closed - SwitchContinue','info')
			#return procgame.game.SwitchContinue

	##################################################
	## Skillshot Switches
	## These will set the ball in play when tripped
	##################################################
	def sw_vortex5k_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_vortex20k_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_vortex100k_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_tenPointer1_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_jetTop_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_jetMiddle_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_jetBottom_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_slingL_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_slingR_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix01_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_chestMatrix02_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix03_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix04_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix05_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix10_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix20_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix30_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix40_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	def sw_chestMatrix50_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue
	
	##################################################
	## Early Ballsave Switches
	## These will save the ball early if the trough has enough balls to support
	## WORK IN PROGRESS
	##################################################

	#def sw_rightOutlane_active(self, sw):
		#if (self.game.utilities.get_player_stats('ballsave_active') == True):
