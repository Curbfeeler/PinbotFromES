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
##     __  _____  ____  ______________  ___    __    __ 
##    /  |/  / / / / / /_  __/  _/ __ )/   |  / /   / / 
##   / /|_/ / / / / /   / /  / // __  / /| | / /   / /  
##  / /  / / /_/ / /___/ / _/ // /_/ / ___ |/ /___/ /___
## /_/  /_/\____/_____/_/ /___/_____/_/  |_/_____/_____/
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
from random import choice
from random import seed

class Multiball(game.Mode):
	def __init__(self, game, priority):
			super(Multiball, self).__init__(game, priority)
			self.ballsLocked = 0
			self.ballLock1Lit = False
			self.ballLock2Lit = False
			#self.ballLock3Lit = False
			self.multiballStarting = False
			#self.multiballIntroLength = 11.287

	def mode_started(self):
		self.getUserStats()
		self.update_lamps()
		return super(Multiball, self).mode_started()

	def mode_stopped(self):
		self.stopMultiball()
		pass

	def update_lamps(self):
		print "Update Lamps: Multiball"
		#self.disableLockLamps()
		#if (self.ballLock1Lit == True):
			#self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			#self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			#print "Lock 1 is Lit"
		#elif (self.ballLock2Lit == True):
			#self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			#self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			#print "Lock 2 is Lit"
		#elif (self.ballLock3Lit == True):
			#self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			#self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			#print "Lock 3 is Lit"

	def open_visor(self):
		self.game.coils.visorMotor.enable()
		self.ballLock1Lit = True
		self.game.utilities.set_player_stats('lock1_lit', self.ballLock1Lit)
		self.ballLock2Lit = True		
		self.game.utilities.set_player_stats('lock2_lit',self.ballLock2Lit)
			
	#def disableLockLamps(self):
		#self.game.lamps.rightRampLock.disable()
		#self.game.lamps.ejectLock.disable()
		#self.game.lamps.dropHoleLock.disable()

	def getUserStats(self):
		self.ballLock1Lit = self.game.utilities.get_player_stats('lock1_lit')
		self.ballLock2Lit = self.game.utilities.get_player_stats('lock2_lit')
		#self.ballLock3Lit = self.game.utilities.get_player_stats('lock3_lit')
		self.ballsLocked = self.game.utilities.get_player_stats('balls_locked')
		print "Lock 1: " + str(self.game.utilities.get_player_stats('lock1_lit'))
		print "Lock 2: " + str(self.game.utilities.get_player_stats('lock2_lit'))
		#print "Lock 3: " + str(self.game.utilities.get_player_stats('lock3_lit'))
		print "Balls Locked: " + str(self.game.utilities.get_player_stats('balls_locked'))

	#def liteLock(self,callback):
		#self.callback = callback
		#if (self.ballsLocked == 0):
			#self.game.utilities.set_player_stats('lock1_lit',True)
			#print "Setting Ball 1 Lock to Lit"
			#self.getUserStats()
		#elif (self.ballsLocked == 1):
			#self.game.utilities.set_player_stats('lock2_lit',True)
			#self.getUserStats()
		#elif (self.ballsLocked == 2):
			#self.game.utilities.set_player_stats('lock3_lit',True)
			#self.getUserStats()
		#self.update_lamps()

	def lockLeftEyeBall(self):
		self.game.sound.play('ball_lock_1')
		self.game.utilities.set_player_stats('ball1_locked',True)
		self.game.utilities.set_player_stats('balls_locked',self.game.utilities.get_player_stats('balls_locked') + 1)
		self.game.utilities.set_player_stats('lock1_lit',False)
		self.getUserStats()
		self.update_lamps()
		self.game.utilities.displayText(100,'LEFT EYE','MADE',seconds=3,justify='center')
		self.game.utilities.score(1000)
		self.game.lampctrlflash.play_show('skillshot', repeat=False, callback=self.game.update_lamps)
		self.game.trough.launch_balls(num=1)
		self.ballLock1Lit = False
		#self.callback()
		if self.game.utilities.get_player_stats('balls_locked')==2:
			self.startMultiball()		

	def lockRightEyeBall(self):
		self.game.sound.play('ball_lock_2')
		self.game.utilities.set_player_stats('ball2_locked',True)
		self.game.utilities.set_player_stats('balls_locked',self.game.utilities.get_player_stats('balls_locked') + 1)
		self.game.utilities.set_player_stats('lock2_lit',False)
		self.getUserStats()
		self.update_lamps()
		self.game.utilities.displayText(100,'RIGHT EYE','MADE',seconds=3,justify='center')
		self.game.utilities.score(1000)
		self.game.lampctrlflash.play_show('skillshot', repeat=False, callback=self.game.update_lamps)
		self.game.trough.launch_balls(num=1)
		self.ballLock2Lit = False	
		#self.callback()
		if self.game.utilities.get_player_stats('balls_locked')==2:
			self.startMultiball()

	def startMultiball(self):
		self.multiballStarting = True
		self.game.utilities.set_player_stats('multiball_running',True)
		self.resetMultiballStats()
		#self.game.collect_mode.incrementActiveZoneLimit()
		self.getUserStats()
		self.update_lamps()
		self.multiballIntro()

	def multiballIntro(self):
		self.cancel_delayed('dropReset')
		self.game.utilities.disableGI()
		self.game.sound.stop_music()
		#self.game.lampctrlflash.play_show('multiball_intro_1', repeat=False)
		#self.game.utilities.randomLampPulse(100)
		# Sound FX #
		self.game.sound.play('multiball_1')
		self.game.sound.play_music('multiball_loop'+ str(self.game.ball),loops=1,music_volume=.5)
		#Short Out Noises
		#self.delay(delay=2,handler=self.game.sound.play,param='short_out_2')
		#self.delay(delay=3,handler=self.game.sound.play,param='short_out_1')
		#self.delay(delay=4.5,handler=self.game.sound.play,param='short_out_1')
		#self.delay(delay=6,handler=self.game.sound.play,param='short_out_2')
		#self.delay(delay=8,handler=self.game.sound.play,param='short_out_1')
		#self.delay(delay=9,handler=self.game.sound.play,param='short_out_2')
		#self.delay(delay=10,handler=self.game.sound.play,param='short_out_1')
		
		#self.game.coils.quakeMotor.schedule(schedule=0x08080808,cycle_seconds=-1,now=True)
		self.resetMultiballStats()
		self.delay(delay=8,handler=self.multiballRun)

	def multiballRun(self):
		self.game.utilities.enableGI()
		#self.game.coils.quakeMotor.patter(on_time=15,off_time=100)
		#self.game.utilities.enableMultiballQuake()
		#self.game.sound.play('centerRampComplete')
		self.game.sound.play_music('multiball_loop'+ str(self.game.ball),loops=-1,music_volume=.6)
		#self.game.utilities.acCoilPulse(coilname='singleEjectHole_LeftInsertBDFlasher',pulsetime=50)
		#self.game.utilities.acFlashPulse('singleEjectHole_LeftInsertBDFlasher')
		if self.game.switches.rightEyeball.is_active()==True:
			self.game.utilities.acCoilPulse(coilname='rightEyeballEject_SunFlasher',pulsetime=50)
		if self.game.switches.leftEyeball.is_active()==True:
			self.game.utilities.acCoilPulse(coilname='leftEyeballEject_LeftPlayfieldFlasher',pulsetime=50)
		if self.game.switches.singleEject.is_active()==True:
			self.game.utilities.acCoilPulse(coilname='singleEjectHole_LeftInsertBDFlasher',pulsetime=50)
		
		
		#self.game.trough.launch_balls(num=2)
		self.multiballStarting = False
		self.game.update_lamps()

	def stopMultiball(self):
		self.game.utilities.set_player_stats('multiball_running',False)
		#self.game.utilities.set_player_stats('jackpot_lit',False)
		self.game.sound.stop_music()
		self.game.sound.play_music('main'+ str(self.game.ball),loops=-1,music_volume=.5)
		self.resetMultiballStats()
		#self.game.bonusmultiplier_mode.incrementBonusMultiplier()
		self.game.update_lamps()
		#self.game.coils.quakeMotor.disable()
		#self.callback()

	def resetMultiballStats(self):
		self.game.utilities.set_player_stats('lock1_lit',False)
		self.game.utilities.set_player_stats('lock2_lit',False)
		self.game.utilities.set_player_stats('lock3_lit',False)
		self.game.utilities.set_player_stats('balls_locked',0)
		self.getUserStats()
		
	#def sw_underPlayfieldDrop1_active(self, sw):
		#if (self.ballLock1Lit == True):
			#self.lockBall1()
		#elif (self.ballLock2Lit == True):
			#self.lockBall2()
		#elif (self.ballLock3Lit == True):
			#self.startMultiball()
		#else:
			#pass

	#def sw_ballPopperBottom_closed(self, sw):
		#if(self.multiballStarting == True):
			#return procgame.game.SwitchStop
		#else:
			#return procgame.game.SwitchContinue


	#def sw_outhole_closed_for_500ms(self, sw):
		##if (self.game.trough.num_balls_in_play == 2):
			##Last ball - Need to stop multiball
			##self.stopMultiball()
		#return procgame.game.SwitchContinue

	def sw_leftEyeball_closed_for_100ms(self, sw):
		if (self.ballLock1Lit == True):
			self.lockLeftEyeBall()
		return procgame.game.SwitchContinue

	def sw_rightEyeball_closed_for_100ms(self, sw):
		if (self.ballLock2Lit == True):
			self.lockRightEyeBall()
		return procgame.game.SwitchContinue


	#EJECTS/EYEBALLS
	    #rightEyeball:
		#number: S42
		#label: 'Right Eye Eject'
	    #leftEyeball:
		#number: S41
		#label: 'Left Eye Eject'



	def sw_visorClosed_open_for_100ms(self, sw):
		self.open_visor()
		return procgame.game.SwitchContinue

	def sw_visorOpen_closed_for_100ms(self, sw):
		self.open_visor()
		return procgame.game.SwitchContinue

	#visorOpen:
	    #number: S67
	#visorClosed:
	    #number: S66


