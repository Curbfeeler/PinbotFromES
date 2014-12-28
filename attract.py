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
##     ___  ________________  ___   ____________   __  _______  ____  ______
##    /   |/_  __/_  __/ __ \/   | / ____/_  __/  /  |/  / __ \/ __ \/ ____/
##   / /| | / /   / / / /_/ / /| |/ /     / /    / /|_/ / / / / / / / __/   
##  / ___ |/ /   / / / _, _/ ___ / /___  / /    / /  / / /_/ / /_/ / /___   
## /_/  |_/_/   /_/ /_/ |_/_/  |_\____/ /_/    /_/  /_/\____/_____/_____/   
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
import locale
import math
import random

#### Set Locale ####
locale.setlocale(locale.LC_ALL, "")

class AttractMode(game.Mode):
	def __init__(self, game, priority):
			super(AttractMode, self).__init__(game, priority)
			self.modeTickCounter = 0
			self.attractTest = False
			self.attractLampshowKey = 0
			self.attractLampshows = 1

	def mode_started(self):
		#### Reset Quake Instituet ####
		#### Be sure it is in the upright position ####
		#self.resetQuakeInstitute()
		
		#### Set Diagnostic LED ####
		#self.game.utilities.setDiagLED(0)

		self.game.coils.acSelect.enable()

		#### Start Attract Mode Lamps ####
		#self.startAttractLamps3()
		#self.game.lampctrl.play_show('attract1', repeat=True)
		self.changeAttractLampshow()

		#### Create and Set Display Content ####
		self.setDisplayContent()

		#### Ensure GI is on ####
		self.game.utilities.enableGI()

		#### Enable Backbox Lighting ####
		#self.game.utilities.setBackboxLED(100,100,255)

	#def mode_tick(self):
		#This will cycle random colors through the backbox during Attract Mode
		#if(self.modeTickCounter == 1000):
			#self.game.utilities.setBackboxLED(random.randint(0,255),random.randint(0,255),random.randint(0,255))
			#self.modeTickCounter = 0
		#else:
			#self.modeTickCounter += 1

	def mode_stopped(self):
		#### Disable All Lamps ####
		for lamp in self.game.lamps:
			lamp.disable()

		self.cancel_delayed('lampshows')
		self.game.lampctrl.stop_show()
		self.game.lampctrlflash.stop_show()

		#### Cancel Display Script ####
		self.game.alpha_score_display.cancel_script()

		#### Enable AC Relay for Flashers ####
		#### This is only needed for using lampshows that contain flashers on the AC Relay ####
		self.game.coils.acSelect.enable()

		#### Disable Backbox Lighting ####
		#self.game.utilities.setBackboxLED()

	def changeAttractLampshow(self):
		if (self.attractLampshowKey < self.attractLampshows):
			self.attractLampshowKey += 1
		else:
			self.attractLampshowKey = 1
		self.game.lampctrlflash.stop_show()
		self.game.lampctrlflash.play_show('attract' + str(self.attractLampshowKey), repeat=True)
		self.delay(name='lampshows',delay=2,handler=self.changeAttractLampshow)

			
	def setDisplayContent(self):
		#### Script List Variable Initialization ####
		script=[]

		if(self.attractTest == True):
			script.append({'top':'TRANSITION 0','bottom':'TRANSITION 0','timer':2,'transition':0})
			script.append({'top':'TRANSITION 1','bottom':'TRANSITION 1','timer':8,'transition':1})
			script.append({'top':'TRANSITION 2','bottom':'TRANSITION 2','timer':2,'transition':2})
			script.append({'top':'TRANSITION 3','bottom':'TRANSITION 3','timer':2,'transition':3})
			script.append({'top':'TRANSITION 4','bottom':'TRANSITION 4','timer':2,'transition':4})
			#Cancel any score display scripts that may be running
			self.game.alpha_score_display.cancel_script()
			self.game.alpha_score_display.set_script(script)
			return




		################################################
		#### Pinbot Title Animation Definition ####
		################################################
		animPinbot=[] # This is a temporary placeholder until we define new transitions
		animPinbot.append({'top':'                ','bottom':'                ','timer':.1,'transition':0})
		animPinbot.append({'top':'               P','bottom':'                ','timer':.1,'transition':0})
		animPinbot.append({'top':'              PI','bottom':'T               ','timer':.1,'transition':0})
		animPinbot.append({'top':'             PIN','bottom':'OT              ','timer':.1,'transition':0})
		animPinbot.append({'top':'            PINB','bottom':'BOT             ','timer':.1,'transition':0})
		animPinbot.append({'top':'           PINBO','bottom':'NBOT            ','timer':.1,'transition':0})
		animPinbot.append({'top':'          PINBOT','bottom':'INBOT           ','timer':.1,'transition':0})
		animPinbot.append({'top':'         PINBOT ','bottom':'PINBOT          ','timer':.1,'transition':0})
		animPinbot.append({'top':'        PINBOT  ','bottom':' PINBOT         ','timer':.1,'transition':0})
		animPinbot.append({'top':'       PINBOT   ','bottom':'  PINBOT        ','timer':.1,'transition':0})
		animPinbot.append({'top':'      PINBOT    ','bottom':'   PINBOT       ','timer':.1,'transition':0})
		animPinbot.append({'top':'     PINBOT     ','bottom':'    PINBOT      ','timer':.1,'transition':0})
		animPinbot.append({'top':'    PINBOT      ','bottom':'     PINBOT     ','timer':.1,'transition':0})
		animPinbot.append({'top':'   PINBOT       ','bottom':'      PINBOT    ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT        ','bottom':'       PINBOT   ','timer':.1,'transition':0})
		animPinbot.append({'top':' PINBOT         ','bottom':'        PINBOT  ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  S     ','bottom':'       PINBOX   ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  X     ','bottom':'       PINBX    ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2     ','bottom':'       PINX     ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  S     ','bottom':'       PIX      ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  X     ','bottom':'       PX       ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2     ','bottom':'       P-       ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  X     ','bottom':'       P-R      ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  S     ','bottom':'       P-RO     ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  X     ','bottom':'       P-ROC    ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2     ','bottom':'      P-ROC     ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2    0','bottom':'     P-ROC      ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2   0 ','bottom':'    P-ROC       ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2  0  ','bottom':'   P-ROC        ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'  P-ROC         ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':' P-ROC          ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'P-ROC       E   ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'P-ROC      EN   ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'P-ROC     EDN   ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'P-ROC    EDIN   ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'P-ROC   EDITN   ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'P-ROC  EDITIN   ','timer':.1,'transition':0})
		animPinbot.append({'top':'  PINBOT  2.0   ','bottom':'P-ROC EDITION   ','timer':5,'transition':0})

		##############
		#### Game Over
		##############
		script.append({'top':'GAME OVER','bottom':'PRESS START','timer':5,'transition':0})

		#########################
		#### Previous Game Scores
		#########################
		self.player1Score = self.game.game_data['LastGameScores']['LastPlayer1Score']
		self.player2Score = self.game.game_data['LastGameScores']['LastPlayer2Score']
		self.player3Score = self.game.game_data['LastGameScores']['LastPlayer3Score']
		self.player4Score = self.game.game_data['LastGameScores']['LastPlayer4Score']

		try:
			self.player1Score = locale.format("%d", int(float(self.player1Score)), True)
		except ValueError:
			pass

		try:
			self.player2Score = locale.format("%d", int(float(self.player2Score)), True)
		except ValueError:
			pass

		try:
			self.player3Score = locale.format("%d", int(float(self.player3Score)), True)
		except ValueError:
			pass

		try:
			self.player4Score = locale.format("%d", int(float(self.player4Score)), True)
		except ValueError:
			pass

		#######################################################################
		#### Set Top and Bottom Text for Previous Game Scores #################
		#### This section will create a string of 16 characters for the top 
		#### and bottom score displays that contains 2 scores for for each row.  
		#### It also contains error checking for when both scores on 1 line are 
		#### larger than 16 characters.
		#######################################################################
		self.scoreSpaceCount = 16 - (len(str(self.player1Score)) + len(str(self.player2Score)))
		if self.scoreSpaceCount < 0: # Just in case scores get very large (over 8 characters each)
			self.scoreSpaceCount = 0
		self.topScoresText = str(self.player1Score)
		for i in range (0,self.scoreSpaceCount): # Puts a space between the scores for i places
			self.topScoresText += ' ' 
		self.topScoresText += str(self.player2Score) # Add the score to the end
		# Set Bottom Text
		self.scoreSpaceCount = 16 - (len(str(self.player3Score)) + len(str(self.player4Score)))
		if self.scoreSpaceCount < 0: # Just in case scores get very large (over 8 characters each)
			self.scoreSpaceCount = 0
		self.bottomScoresText = str(self.player3Score)
		for i in range (0,self.scoreSpaceCount):
			self.bottomScoresText += ' '
		self.bottomScoresText += str(self.player4Score)

		# Append Prev Game Scores to Script
		script.append({'top':self.topScoresText,'bottom':self.bottomScoresText,'timer':7,'transition':0})
		
		########################################################
		#### Title Screen Animation ############################
		#### Adds the animation defined above to the script list
		########################################################
		script=script + animPinbot

		########################
		#### About Game Software
		########################
		script.append({'top':'SOFTWARE BY','bottom':'DAN MYERS','timer':5,'transition':3})

		################
		#### High Scores
		################
		#for category in self.game.highscore_categories:
			#for index, score in enumerate(category.scores):
				#score_str = locale.format("%d", score.score, True)
				#ranking = str(index)
				#name = str(score.inits)
				#data={'score':score_str, 'ranking':ranking}

				#### Classic High Score Data ####
				#if category.game_data_key == 'ClassicHighScoreData':
					#if index == 0:
						#text1 = 'GRAND CHAMPION'
						#text2 = name + ' ' + score_str
					#else:
						#text1 = 'HIGH SCORE ' + ranking
						#text2 = name + ' ' + score_str
				#### Mileage Champion ####
				#elif category.game_data_key == 'MilesChampion':
					#if index == 0:
						#text1 = 'MILEAGE CHAMP'
						#text2 = name + ' ' + score_str + ' MILES'

				#script.append({'top':text1,'bottom':text2,'timer':5,'transition':1})

		self.grandChampScore = locale.format("%d", self.game.game_data['GrandChamp']['GrandChampScore'], True)
		self.grandChampInits = self.game.game_data['GrandChamp']['GrandChampInits']

		self.highScore1Score = locale.format("%d", self.game.game_data['HighScore1']['HighScore1Score'], True)
		self.highScore1Inits = self.game.game_data['HighScore1']['HighScore1Inits']

		self.highScore2Score = locale.format("%d", self.game.game_data['HighScore2']['HighScore2Score'], True)
		self.highScore2Inits = self.game.game_data['HighScore2']['HighScore2Inits']

		self.highScore3Score = locale.format("%d", self.game.game_data['HighScore3']['HighScore3Score'], True)
		self.highScore3Inits = self.game.game_data['HighScore3']['HighScore3Inits']

		self.highScore4Score = locale.format("%d", self.game.game_data['HighScore4']['HighScore4Score'], True)
		self.highScore4Inits = self.game.game_data['HighScore4']['HighScore4Inits']

		script.append({'top':'GRAND CHAMPION','bottom':self.grandChampInits + ' ' + self.grandChampScore,'timer':.75,'transition':1})
		script.append({'top':'HIGH SCORE 1','bottom':self.highScore1Inits + ' ' + self.highScore1Score,'timer':.75,'transition':1})
		script.append({'top':'HIGH SCORE 2','bottom':self.highScore2Inits + ' ' + self.highScore2Score,'timer':.75,'transition':1})
		script.append({'top':'HIGH SCORE 3','bottom':self.highScore3Inits + ' ' + self.highScore3Score,'timer':.75,'transition':1})
		script.append({'top':'HIGH SCORE 4','bottom':self.highScore4Inits + ' ' + self.highScore4Score,'timer':.75,'transition':1})

		#####################################################
		#### Previous Game Scores #2 ########################
		#### This is used to append the previous game scores 
		#### defined above to the script again after the high 
		#### scores have been displayed.
		##################################################### 
		script.append({'top':self.topScoresText,'bottom':self.bottomScoresText,'timer':2,'transition':0})

		###################
		#### Special Thanks
		###################
		script.append({'top':'SPECIAL THANKS','bottom':'MULTIMORPHIC','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'MARK SUNNUCKS','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'MICHAEL OCEAN','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'SCOTT DANESI','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'MYPINBALLS JIM','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'BRIAN MADDEN','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'EP THE GEEK','timer':3,'transition':2})

		#####################
		#### Powered By P-ROC
		#####################
		script.append({'top':'PROUDLY POWERED','bottom':'BY              ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY             P','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY            P ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY           P  ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY          P   ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY         P    ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY        P     ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY       P      ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY      P       ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY     P        ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY    P         ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY   P          ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY  P           ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P           -','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P          - ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P         -  ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P        -   ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P       -    ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P      -     ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P     -      ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P    -       ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P   -        ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P  -         ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P -          ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-           ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P+           ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-          R','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P+         RO','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-        ROC','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P+       ROC ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-      ROC  ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P+     ROC   ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-    ROC    ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P+   ROC     ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-  ROC      ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P+ ROC       ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-ROC        ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P+ROC        ','timer':.1,'transition':0})
		script.append({'top':'PROUDLY POWERED','bottom':'BY P-ROC        ','timer':5,'transition':0})

		
		
		#############################
		#### Start New Display Script
		#############################
		#Cancel any score display scripts that may be running
		self.game.alpha_score_display.cancel_script()
		self.game.alpha_score_display.set_script(script)
		
	def startAttractLamps(self):
		##############################################################
		#### Start Attract Lamps Version 1 ###########################
		#### This basic attract lamp show uses a schedule to cycle 
		#### through the lamps in the game.  This surprisingly creates 
		#### a nice attract mode for those looking to get something 
		#### basic up and running.  It uses a mod function to cycle 
		#### through every 4 lamps.
		##############################################################
		i = 0
		for lamp in self.game.lamps:
			if i % 4 == 3:
				lamp.schedule(schedule=0xf000f000, cycle_seconds=0, now=False)
			elif i % 4 == 2:
				lamp.schedule(schedule=0x0f000f00, cycle_seconds=0, now=False)
			elif i % 4 == 1:
				lamp.schedule(schedule=0x00f000f0, cycle_seconds=0, now=False)
			elif i % 4 == 0:
				lamp.schedule(schedule=0x000f000f, cycle_seconds=0, now=False)
			i = i + 1

	def startAttractLamps2(self):
		##############################################################
		#### Start Attract Lamps Version 2 ###########################
		#### This basic attract lamp show uses a schedule to cycle 
		#### through the lamps in the game.  This surprisingly creates 
		#### a nice attract mode for those looking to get something 
		#### basic up and running.  It uses a mod function to cycle 
		#### through every 8 lamps.
		##############################################################
		i = 0
		for lamp in self.game.lamps:
			if i % 8 == 7:
				lamp.schedule(schedule=0xf0000000, cycle_seconds=0, now=False)
			elif i % 8 == 6:
				lamp.schedule(schedule=0x0f000000, cycle_seconds=0, now=False)
			elif i % 8 == 5:
				lamp.schedule(schedule=0x00f00000, cycle_seconds=0, now=False)
			elif i % 8 == 4:
				lamp.schedule(schedule=0x000f0000, cycle_seconds=0, now=False)
			elif i % 8 == 3:
				lamp.schedule(schedule=0x0000f000, cycle_seconds=0, now=False)
			elif i % 8 == 2:
				lamp.schedule(schedule=0x00000f00, cycle_seconds=0, now=False)
			elif i % 8 == 1:
				lamp.schedule(schedule=0x000000f0, cycle_seconds=0, now=False)
			elif i % 8 == 0:
				lamp.schedule(schedule=0x0000000f, cycle_seconds=0, now=False)
			i = i + 1

	def startAttractLamps3(self):
		##############################################################
		#### Start Attract Lamps Version 2 ###########################
		#### This basic attract lamp show uses a schedule to cycle 
		#### through the lamps in the game.  This surprisingly creates 
		#### a nice attract mode for those looking to get something 
		#### basic up and running.  It uses a mod function to cycle 
		#### through every 8 lamps.
		##############################################################
		i = 0
		for lamp in self.game.lamps:
			if i % 8 == 7:
				lamp.schedule(schedule=0xf00000ff, cycle_seconds=0, now=False)
			elif i % 8 == 6:
				lamp.schedule(schedule=0xff00000f, cycle_seconds=0, now=False)
			elif i % 8 == 5:
				lamp.schedule(schedule=0xfff00000, cycle_seconds=0, now=False)
			elif i % 8 == 4:
				lamp.schedule(schedule=0x0fff0000, cycle_seconds=0, now=False)
			elif i % 8 == 3:
				lamp.schedule(schedule=0x00fff000, cycle_seconds=0, now=False)
			elif i % 8 == 2:
				lamp.schedule(schedule=0x000fff00, cycle_seconds=0, now=False)
			elif i % 8 == 1:
				lamp.schedule(schedule=0x0000fff0, cycle_seconds=0, now=False)
			elif i % 8 == 0:
				lamp.schedule(schedule=0x00000fff, cycle_seconds=0, now=False)
			i = i + 1
		
	#def resetQuakeInstitute(self):
		#### Quake Institute Reset ###############################
		#### In case the Quake Institute is down, this will start 
		#### the motor and the Institute Up switch will activate 
		#### and stop in the switch handler below
		##########################################################
		#if self.game.switches.instituteUp.is_active()==False:
			#self.game.coils.quakeInstitute.enable()

	################################
	#### Switch Handler Section ####
	################################
	#def sw_instituteUp_open(self, sw):
		#self.game.coils.quakeInstitute.disable()
		#return procgame.game.SwitchStop

	def sw_outhole_closed(self, sw):
		#This will eventually be moved to the Trough mode
		return procgame.game.SwitchStop

	def sw_outhole_active_for_1s(self, sw):
		#This will eventually be moved to the Trough mode
		#self.game.coils.flipperEnable.disable()
		#self.game.utilities.acCoilPulse('outholeKicker_Knocker')
		#self.game.alpha_score_display.set_text("GAME OVER",0)
		#self.game.alpha_score_display.set_text("PRESS START",1)
		return procgame.game.SwitchStop
	
	#######################################################################
	#### Jet, Sling and Skillshot Switch Handling #########################
	#### Stop the switches from registering during Attract Mode ###########
	#######################################################################
	def sw_jetTop_active(self, sw):
		return procgame.game.SwitchStop

	def sw_jetMiddle_active(self, sw):
		return procgame.game.SwitchStop

	def sw_jetBottom_active(self, sw):
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		return procgame.game.SwitchStop

	#def sw_onRamp25k_active(self, sw):
		#return procgame.game.SwitchStop

	#def sw_onRamp50k_active(self, sw):
		#return procgame.game.SwitchStop

	#def sw_onRamp100k_active(self, sw):
		#return procgame.game.SwitchStop

	#def sw_onRampBypass_active(self, sw):
		#return procgame.game.SwitchStop