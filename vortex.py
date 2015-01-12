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
##    _   _            _            
##   | | | |          | |           
##   | | | | ___  _ __| |_ _____  __
##   | | | |/ _ \| '__| __/ _ \ \/ /
##   \ \_/ / (_) | |  | ||  __/>  < 
##    \___/ \___/|_|   \__\___/_/\_\
##                              
#################################################################################

import procgame.game
from procgame import *
import pinproc
import locale

class VortexMode(game.Mode):

	def __init__(self, game, priority):
			super(VortexMode, self).__init__(game, priority)
			####################
			#Mode Setup
			####################
			self.vortexDisplayTime = 3

	def mode_started(self):
		self.game.utilities.set_player_stats('vortex_active',True)
		self.update_lamps()
		self.game.utilities.displayText(100,'VORTEX FOR',str(self.game.utilities.get_player_stats('bonus_x')) +'X',seconds=6,justify='center')
		return super(VortexMode, self).mode_started()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('vortex_active',False)
		self.update_lamps()
		#self.game.collect_mode.update_lamps()
		return super(VortexMode, self).mode_stopped()

	def update_lamps(self):
		print "Update Lamps: Skillshot"
		if (self.game.utilities.get_player_stats('vortex_active') == True):
			self.startVortexLamps()
		else:
			self.stopVortexLamps()
	
	def startVortexLamps(self):
		pass
	        #self.game.lamps.gameOverBackBox.schedule(schedule=0x0000000F, cycle_seconds=0, now=False)
		#self.game.lamps.matchBackBox.schedule(schedule=0x000000F0, cycle_seconds=0, now=False)
		#self.game.lamps.ballInPlayBackBox.schedule(schedule=0x00000F00, cycle_seconds=0, now=False)
		#self.game.lamps.mouth1LeftBackBox.schedule(schedule=0x0000F000, cycle_seconds=0, now=False)
		#self.game.lamps.mouth2BackBox.schedule(schedule=0x000F0000, cycle_seconds=0, now=False)
		#self.game.lamps.chestMatrix52.schedule(schedule=0xCCC00000, cycle_seconds=1, now=False)
		#self.game.coils.outholeKicker_Knocker.schedule(schedule=0x00C00000, cycle_seconds=0, now=False)

	def stopVortexLamps(self):
		pass
		#self.game.lamps.gameOverBackBox.disable()
		#self.game.lamps.matchBackBox.disable()
		#self.game.lamps.ballInPlayBackBox.disable()
		#self.game.lamps.mouth1LeftBackBox.disable()
		#self.game.lamps.mouth2BackBox.disable()
		#self.game.lamps.chestMatrix52.disable()
		#self.game.coils.outholeKicker_Knocker.disable()

	##############################
	## Vortex Handling Modes ##
	##############################



	def sw_shooter_active_for_8000ms(self, sw):
		#########################
		#Alert Snoozing Player
		#########################
		self.game.utilities.displayText(101,'HEY',self.game.players[self.game.current_player_index].name.upper(),seconds=2,justify='center')
		self.game.utilities.displayText(100,'VORTEX FOR',str(self.game.utilities.get_player_stats('bonus_x')) +'X',seconds=6,justify='center')
		self.game.sound.play('wakeUp')
		self.game.shooter_lane_status = 1
		return procgame.game.SwitchContinue

	def vortexMissed(self):
		self.game.utilities.displayText(100,'VORTEX','MISSED',seconds=self.vortexDisplayTime,justify='center')
		self.game.sound.play('skillshotMissed')
		#self.game.sound.stop_music()
		#self.game.sound.play_music('main'+ str(self.game.ball),loops=1,music_volume=.5)
		self.game.modes.remove(self)

		
	def vortexMade(self, iPoints):
		self.game.utilities.displayText(100,'VORTEX',locale.format("%d", iPoints * self.game.utilities.get_player_stats('bonus_x'), grouping=True) + ' POINTS',seconds=self.vortexDisplayTime,justify='center')
		self.game.utilities.score(iPoints * self.game.utilities.get_player_stats('bonus_x'))
		self.game.lampctrlflash.play_show('skillshot', repeat=False, callback=self.game.update_lamps)

		#points will be added in the base mode
		self.game.sound.play('vortexMade')
		#self.game.sound.stop_music()
		#self.game.sound.play_music('main'+ str(self.game.ball),loops=1,music_volume=.5)				
		self.game.modes.remove(self)
	
		

	###########################
	## Switch Handling Modes ##
	###########################

	#def sw_outhole_closed_for_1s(self, sw):
		##### Remove Skillshot Mode ####
		#self.game.modes.remove(self)
		#return procgame.game.SwitchContinue

	def sw_vortex5k_active(self, sw):
		self.vortexMade(5000)
		return procgame.game.SwitchContinue

	def sw_vortex20k_active(self, sw):
		self.vortexMade(20000)
		return procgame.game.SwitchContinue

	def sw_vortex100k_active(self, sw):
		self.vortexMade(100000)
		return procgame.game.SwitchContinue

	def sw_chestMatrix01_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	def sw_chestMatrix02_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix03_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix04_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix05_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix10_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix20_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix30_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix40_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue
	def sw_chestMatrix50_active(self, sw):
		self.vortexMissed()			
		return procgame.game.SwitchContinue


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


	def sw_slingR_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue

	def sw_slingL_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue

	def sw_outlaneLeft_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_inlaneLeft_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_inlaneRight_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_outlaneRight_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_singleEject_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_enterRamp_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_jetTop_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_jetMiddle_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_jetBottom_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_tenPointer1_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_tenPointer2_BehindDropBank_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_tenPointer3_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_upperDrop_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_midDrop_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_lowerDrop_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_scoreEnergyStandUp_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
	
	def sw_advancePlanent_active(self, sw):
		self.vortexMissed()
		return procgame.game.SwitchContinue
