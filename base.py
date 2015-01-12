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
##     ____  ___   _____ ______   __  _______  ____  ______
##    / __ )/   | / ___// ____/  /  |/  / __ \/ __ \/ ____/
##   / __  / /| | \__ \/ __/    / /|_/ / / / / / / / __/   
##  / /_/ / ___ |___/ / /___   / /  / / /_/ / /_/ / /___   
## /_____/_/  |_/____/_____/  /_/  /_/\____/_____/_____/    
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc 
import random
import time
import sys
import locale

#from bonus import *

class BaseGameMode(game.Mode):
	def __init__(self, game, priority):
			#locale.setlocale(locale.LC_ALL, '') #Might not be needed
			super(BaseGameMode, self).__init__(game, priority)
			
			
	def mode_started(self):
			#Start Attract Mode
			self.game.modes.add(self.game.attract_mode)
			self.game.utilities.releaseStuckBalls()

	def update_lamps(self):
		self.game.lamps.ballInPlayBackBox.enable()
		#self.game.lamps.jetRightLamp.enable()
		#self.game.lamps.jetTopLamp.enable()
			
	###############################################################
	# MAIN GAME HANDLING FUNCTIONS
	###############################################################
	def start_game(self):
		self.game.utilities.log('Start Game','info')

		self.game.sound.stop_music()

		#Reset Prior Game Scores
		self.game.game_data['LastGameScores']['LastPlayer1Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer2Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer3Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer4Score'] = ' '

		#This function is to be used when starting a NEW game, player 1 and ball 1
		#Clean Up
		self.game.modes.remove(self.game.attract_mode)
		#self.game.modes.add(self.game.tilt)
		
		self.game.add_player() #will be first player at this point
		self.game.ball = 1

		self.start_ball()
		self.game.utilities.updateBaseDisplay()

		#self.game.sound.play('game_start')


		print "Game Started"
		
	def start_ball(self):
		self.game.utilities.log('Start Ball','info')

		#### Update Audits ####
		self.game.game_data['Audits']['Balls Played'] += 1
		self.game.save_game_data()
		
		#### Set Diagnostic LED ####
		#self.game.utilities.setDiagLED(self.game.current_player_index + 1)

		#### Queue Ball Modes ####
		self.loadBallModes()

		#### Enable Flippers ####
		self.game.coils.flipperEnable.enable()

		self.game.enable_bumpers(enable=True)

		#### Ensure GI is on ####
		self.game.utilities.enableGI()

		#### Kick Out Ball ####
		# This is from the original code.  Replacing with the trough mode functions
		#self.game.utilities.acCoilPulse(coilname='feedShooter_UpperPFFLash',pulsetime=50)
		#self.game.trough.num_balls_in_play = 1
		#self.game.trough.num_balls_to_launch = 1
		self.game.trough.launch_balls(num=1)


		#### Update Player Display ####
		self.game.utilities.updateBaseDisplay()

		#### Enable GI in case it is disabled from TILT ####
		self.game.utilities.enableGI()

		#### Start Shooter Lane Music ####
		self.game.sound.play_music('shooter'+ str(self.game.ball),loops=10,music_volume=.5)
		self.game.shooter_lane_status = 1
		self.game.sound.play('player_'+str(self.game.current_player_index+1) +'_up_vox')
		self.delay(delay=1.2,handler=self.game.sound.play,param='game_start')
		#### Debug Info ####
		#print "Ball Started"

	def finish_ball(self):
		# Remove Drops mode because of delay issue #
		self.game.modes.remove(self.game.drops_mode)

		self.game.modes.add(self.game.bonus_mode)
		
		if self.game.tiltStatus == 0:
			self.game.bonus_mode.calculate(self.game.base_mode.finish_ball)
			#### Script List Variable Initialization ####
			script=[]
			
			myBonus = self.game.utilities.get_player_stats('bonus')
			if myBonus > 0:
				myMultiplier = self.game.utilities.get_player_stats('bonus_x')
				if myMultiplier == 1:
					self.game.utilities.displayText(102,'END BALL BONUS',locale.format("%d", myBonus, grouping=True),seconds=5,justify='center')
				else:
					self.game.utilities.displayText(102,'END BALL BONUS',locale.format("%d", myBonus, grouping=True) +' X' +str(myMultiplier),seconds=5,justify='center')
					for x in range(1, myMultiplier):
						myNewBonus = myBonus + myBonus
						self.game.utilities.displayText(102,'END BALL BONUS',locale.format("%d", myNewBonus, grouping=True) +' X' +str(myMultiplier-x),seconds=5,justify='center')						
				self.game.utilities.score(myBonus*myMultiplier)
			else:
				self.game.utilities.displayText(102,'END OF BALL','NO BONUS',seconds=5,justify='center')
			#if self.game.switches.leftEyeBall.is_closed() == True:
					#self.game.Coils.('Dummy')
			#if self.game.switches.rightEyeBall.is_closed() == True:
					#self.game.Coils.('Dummy')
			self.game.utilities.releaseStuckBalls()


			self.delay(delay=6,handler=self.end_ball)

		
	def end_ball(self):
		#Remove Bonus
		self.game.modes.remove(self.game.bonus_mode)
		

		#update games played stats
		self.game.game_data['Audits']['Balls Played'] += 1

		#Update Last Game Scores in game data file
		if self.game.ball == self.game.balls_per_game:
			self.playerAuditKey = 'LastPlayer' + str(self.game.current_player_index + 1) + 'Score'
			self.game.game_data['LastGameScores'][self.playerAuditKey] = self.game.utilities.currentPlayerScore()

		#save game audit data
		self.game.save_game_data()

		self.game.utilities.log("End of Ball " + str(self.game.ball) + " Called",'info')
		self.game.utilities.log("Total Players: " + str(len(self.game.players)),'info')
		self.game.utilities.log("Current Player: " + str(self.game.current_player_index),'info')
		self.game.utilities.log("Balls Per Game: " + str(self.game.balls_per_game),'info')
		self.game.utilities.log("Current Ball: " + str(self.game.ball),'info')

		#### Remove Ball Modes ####
		self.unloadBallModes()

		#self.game.sound.fadeout_music(time_ms=1000) #This is causing delay issues with the AC Relay
		self.game.sound.stop_music()

                if self.game.utilities.get_player_stats('extra_balls') > 0:
                        self.game.lamps.shootAgain.schedule(schedule=0xFF00FF00)
                        self.start_ball()
                elif self.game.current_player_index == len(self.game.players) - 1:
			#Last Player or Single Player Drained
			#print "Last player or single player drained"
			if self.game.ball == self.game.balls_per_game:
				#Last Ball Drained
				print "Last ball drained, ending game"
				#self.end_game()
				self.finish_game()
			else:
				#Increment Current Ball
				#print "Increment current ball and set player back to 1"
				self.game.current_player_index = 0
				self.game.ball += 1
				self.start_ball()
		else:
			#Not Last Player Drained
			print "Not last player drained"
			self.game.current_player_index += 1
			self.start_ball()

	def finish_game(self):
		#self.game.modes.add(self.game.highscore_mode)
		#self.game.highscore_mode.checkScores(self.game.base_mode.end_game)
		self.end_game()

	def end_game(self):
		self.game.utilities.log('Game Ended','info')

		self.game.modes.remove(self.game.highscore_mode)

		#### Disable Flippers ####
		self.game.coils.flipperEnable.disable()

		#### Disable Bumpers ####
		self.game.enable_bumpers(enable=False)

		#### Disable AC Relay ####
		self.cancel_delayed(name='acEnableDelay')
		#self.game.coils.acSelect.disable()

		#### Update Gmaes Played Stats ####
		self.game.game_data['Audits']['Games Played'] += 1

		#### Save Game Audit Data ####
		self.game.save_game_data()

		#self.game.modes.add(self.game.attract_mode)
		self.game.sound.play_music('game_over'+ str(self.game.ball),loops=1,music_volume=1)

		self.game.reset()

	def loadBallModes(self):
		self.game.modes.add(self.game.skillshot_mode)
		#self.game.modes.add(self.game.bonus_mode)
		#self.game.modes.add(self.game.chest_mode) #not starting it on ball load for now.
		#self.game.modes.add(self.game.centerramp_mode)
		#self.game.modes.add(self.game.rightramp_mode)
		self.game.modes.add(self.game.tilt)
		self.game.modes.add(self.game.ballsaver_mode)
		self.game.modes.add(self.game.drops_mode)
		#self.game.modes.add(self.game.jackpot_mode)
		#self.game.modes.add(self.game.spinner_mode)
		#self.game.modes.add(self.game.multiball_mode)
		#self.game.modes.add(self.game.collect_mode)
		#self.game.modes.add(self.game.shelter_mode)
		
	def unloadBallModes(self):
		self.game.modes.remove(self.game.bonus_mode)
		self.game.modes.remove(self.game.skillshot_mode)
		self.game.modes.remove(self.game.chest_mode)
		self.game.modes.remove(self.game.vortex_mode)
		#self.game.modes.remove(self.game.centerramp_mode)
		#self.game.modes.remove(self.game.rightramp_mode)
		self.game.modes.remove(self.game.tilt)
		self.game.modes.remove(self.game.ballsaver_mode)
		self.game.modes.remove(self.game.drops_mode)
		#self.game.modes.remove(self.game.jackpot_mode)
		#self.game.modes.remove(self.game.spinner_mode)
		self.game.modes.remove(self.game.multiball_mode)
		#self.game.modes.remove(self.game.collect_mode)
		#self.game.modes.remove(self.game.shelter_mode)
		self.game.modes.remove(self.game.bonusmultiplier_mode)

		### Clear Mini Modes ###
		self.game.modes.remove(self.game.mode_1)
		self.game.modes.remove(self.game.mode_2)
		self.game.modes.remove(self.game.mode_3)
		self.game.modes.remove(self.game.mode_4)
		self.game.modes.remove(self.game.mode_5)
		self.game.modes.remove(self.game.mode_6)
		self.game.modes.remove(self.game.mode_7)
		self.game.modes.remove(self.game.mode_8)
		self.game.modes.remove(self.game.mode_9)

	def ejectSingle1(self):
		self.game.utilities.acFlashPulse('singleEjectHole_LeftInsertBDFlasher')
		self.delay(delay=.2,handler=self.game.utilities.acFlashPulse,param='singleEjectHole_LeftInsertBDFlasher')
		self.delay(delay=.4,handler=self.game.utilities.acCoilPulse,param='singleEjectHole_LeftInsertBDFlasher')
		self.delay(delay=.6,handler=self.game.sound.play,param='ejectsaucer')

	# extra method for adding bonus to make it shorter when used
	def add_bonus(self,bonusname,points):
		mybonus = self.game.utilities.get_player_stats(bonusname)
		self.game.utilities.set_player_stats(bonusname,mybonus + points)
		self.game.utilities.displayText(100,'ENERGY',str(mybonus + points),seconds=.5,justify='center')
		#print "player_stats('bonus',points)" +str(points)

	###############################################################
	# BASE SWITCH HANDLING FUNCTIONS
	###############################################################		
	#def sw_instituteDown_closed(self, sw):
		#self.game.coils.quakeInstitute.disable()
		#return procgame.game.SwitchStop

	def sw_startButton_active_for_1000ms(self, sw):
		#########################
		#Force Stop Game
		#########################
		self.game.utilities.log('Force Stop Game','warning')

		#### Remove Ball Modes ####
		self.unloadBallModes()

		#self.game.sound.fadeout_music(time_ms=1000) #This is causing delay issues with the AC Relay
		self.game.sound.stop_music()

		self.end_game()
		
	def sw_startButton_active_for_20ms(self, sw):
		print 'Player: ' + str(self.game.players.index)
		print 'Ball' + str(self.game.ball)
		#Flash GI - Not using schedule
		self.flashDelay = .1 #used for the delay between GI flashes
		self.flashDelayGap = .1
		self.game.utilities.disableGI()
		self.delay(name='reenableGI',delay=self.flashDelay,handler=self.game.utilities.enableGI)
		self.delay(name='disableGI',delay=(self.flashDelay*2)+self.flashDelayGap,handler=self.game.utilities.disableGI)
		self.delay(name='reenableGI',delay=(self.flashDelay*3)+self.flashDelayGap,handler=self.game.utilities.enableGI)
		self.flashDelay = .1 #used for the delay between GI flashes
		self.flashDelayGap = .1

		#Trough is full!
		if self.game.ball == 0:
			if self.game.utilities.troughIsFull()==True:
				#########################
				#Start New Game
				#########################
				self.start_game()
			else:
				#missing balls
				self.game.utilities.releaseStuckBalls()
				#self.game.alpha_score_display.set_text("MISSING PINBALLS",0)
				#self.game.alpha_score_display.set_text("PLEASE WAIT",1)
		elif self.game.ball == 1 and len(self.game.players) < 4:
			self.game.add_player()
			print 'Player Added - Total Players = ' + str(len(self.game.players))
			if (len(self.game.players) == 2):
				self.game.sound.play_voice('player_2_vox')
				self.game.utilities.displayText(200,topText='PLAYER 2',bottomText='ADDED',seconds=1,justify='center')
			elif (len(self.game.players) == 3):
				self.game.sound.play_voice('player_3_vox')
				self.game.utilities.displayText(200,topText='PLAYER 3',bottomText='ADDED',seconds=1,justify='center')
			elif (len(self.game.players) == 4):
				self.game.sound.play_voice('player_4_vox')
				self.game.utilities.displayText(200,topText='PLAYER 4',bottomText='ADDED',seconds=1,justify='center')
		else:
			pass		
		return procgame.game.SwitchStop

	def sw_startButton_active_for_1s(self, sw):
		#will put launcher in here eventually
		pass
		
	def sw_outhole_closed_for_1s(self, sw):
		### Ball handling ###
		if self.game.trough.num_balls_in_play == 1: #Last ball in play
			self.game.utilities.setBallInPlay(False) # Will need to use the trough mode for this
			#self.game.utilities.acCoilPulse('outholeKicker_Knocker')
			self.delay('finishBall',delay=1,handler=self.finish_ball)
		return procgame.game.SwitchStop

	def sw_singleEject_closed_for_200ms(self, sw):
		self.ejectSingle1()
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_jetMiddle_active(self, sw):
		self.game.sound.play('jet')
		self.game.utilities.score(200)
		self.add_bonus("energy_bonus",1000)
		self.add_bonus("bonus",100)

		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_jetBottom_active(self, sw):
		self.game.sound.play('jet')
		self.game.utilities.score(200)
		self.add_bonus("energy_bonus",1000)
		self.add_bonus("bonus",100)
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		self.game.sound.play('jet')
		self.game.utilities.score(200)
		self.add_bonus("energy_bonus",1000)
		self.add_bonus("bonus",100)		
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		self.game.sound.play('sling')
		self.game.utilities.score(100)
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		self.game.sound.play('sling')
		self.game.utilities.score(100)
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop


	##################################################
	## Skillshot Switches
	## These will set the ball in play when tripped
	##################################################
	#def sw_onRamp25k_active(self, sw):
		#self.game.utilities.setBallInPlay(True)
		#return procgame.game.SwitchStop

	#def sw_onRamp50k_active(self, sw):
		#self.game.utilities.setBallInPlay(True)
		#return procgame.game.SwitchStop

	#def sw_onRamp100k_active(self, sw):
		#self.game.utilities.setBallInPlay(True)
		#return procgame.game.SwitchStop

	#def sw_onRampBypass_active(self, sw):
		#self.game.utilities.setBallInPlay(True)
		#return procgame.game.SwitchStop

	#def sw_centerRampMiddle_active(self, sw):
		#self.game.utilities.setBallInPlay(True)
		#return procgame.game.SwitchStop

	#def sw_centerRampEnd_active(self, sw):
		#self.game.utilities.setBallInPlay(True)
		#return procgame.game.SwitchStop

	def sw_shooter_open(self, sw):
		# This will play the car take off noise when the ball leaves the shooter lane
		if (self.game.utilities.get_player_stats('ball_in_play') == False):
			self.game.sound.play('game_start_takeoff')
		
			

	#############################
	## Zone Switches
	#############################
	#def sw_leftStandup1_closed(self, sw):
		#return procgame.game.SwitchStop

	#def sw_rightStandupHigh2_closed(self, sw):
		#return procgame.game.SwitchStop

	#def sw_rightStandupLow3_closed(self, sw):
		#return procgame.game.SwitchStop
		
	#def sw_centerStandup4_closed(self, sw):
		#return procgame.game.SwitchStop
		
	#def sw_ejectHole5_closed(self, sw):
		#return procgame.game.SwitchStop
		
	#def sw_rightLoop6_closed(self, sw):
		#return procgame.game.SwitchStop
		
	#def sw_rightInsideReturn7_closed(self, sw):
		#return procgame.game.SwitchStop
		
	#def sw_leftReturnLane8_closed(self, sw):
		#return procgame.game.SwitchStop
		
	#def sw_captiveBall9_closed(self, sw):
		#return procgame.game.SwitchStop

	def sw_shooter_closed_for_1s(self, sw):
		if (self.game.utilities.get_player_stats('ball_in_play') == True):
			#Kick the ball into play
			#self.game.trough.launch_ball()
			pass
		return procgame.game.SwitchStop

	#############################
	## Outlane Switches
	#############################
	def sw_outlaneRight_closed(self, sw):
		self.game.utilities.setBallInPlay(True)
		self.game.utilities.score(100)
		self.game.sound.play('outlane')

	def sw_outlaneLeft_closed(self, sw):
		self.game.utilities.setBallInPlay(True)
		self.game.utilities.score(100)
		self.game.sound.play('outlane')

	#############################
	## Inlane Switches
	#############################
	def sw_inlaneRight_closed(self, sw):
		self.game.utilities.setBallInPlay(True)
		self.game.utilities.score(100)
		self.game.sound.play('inlane')

	def sw_inlaneLeft_closed(self, sw):
		self.game.utilities.setBallInPlay(True)
		self.game.utilities.score(100)
		self.game.sound.play('inlane')

	def sw_unused62_closed(self, sw):
		self.game.utilities.acCoilPulse(coilname='feedShooter_UpperPFFLash',pulsetime=100)