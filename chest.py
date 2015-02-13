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

class ChestMode(game.Mode):
	"""docstring for ChestMode"""
	def __init__(self, game, priority):
			super(ChestMode, self).__init__(game, priority)
			self.chestFilled = False
			self.chestFilledPoints = 10000
			self.chestFilledDisplayTime = 3
			for switch in self.game.switches:
				if switch.name.find('chestMatrix', 0) != -1:
					self.add_switch_handler(name=switch.name, event_type='active', \
					delay=0.01, handler=self.chestMatrixSwitches)			

	def mode_started(self):
		#### Load Mode Feature Defaults ####
		self.chestHold = self.game.user_settings['Feature']['Chest Hold']

		if (self.chestHold == False):
			self.resetChest()
		else:
			self.update_lamps()

		return super(ChestMode, self).mode_started()
				
	def mode_stopped(self):
		return super(ChestMode, self).mode_stopped()

	def update_lamps(self):
		print "update_lamps"
		objPlayer = self.game.players[self.game.current_player_index]
		for num in range(0,4):
			columndatadict = objPlayer.chestColMatrix[num]
			for key, value in sorted(columndatadict.items()):
				if value == True:
					self.game.lamps[key].enable()
		pass

	def resetChest(self):
		print "resetChest"
		objPlayer = self.game.players[self.game.current_player_index]
		for num in range(0,4):
			columndatadict = objPlayer.chestColMatrix[num]
			for colkey, colvalue in sorted(columndatadict.items()):
				colvalue = False
			rowdatadict = objPlayer.chestRowMatrix[num]
			for rowkey, rowvalue in sorted(rowdatadict.items()):
				rowvalue = False
		pass

	def chestMade(self, iPoints):
		self.chestFilled = True
		self.game.utilities.displayText(100,'CHEST', 'MADE',str(iPoints * self.game.utilities.get_player_stats('chestmade_x')), 'POINTS',seconds=self.chestFilledDisplayTime,justify='center')
		self.game.utilities.score(iPoints * self.game.utilities.get_player_stats('chestmade_x'))
		self.game.utilities.set_player_stats('chestmade_x',self.game.utilities.get_player_stats('chestmade_x') + 1)
		self.game.lampctrlflash.play_show('skillshot', repeat=False, callback=self.game.update_lamps)

		#points will be added in the base mode
		self.game.sound.play('vortexMade')
		self.game.sound.stop_music()
		self.game.sound.play_music('multiball_intro'+ str(self.game.ball),loops=1,music_volume=.5)				
		self.game.modes.remove(self)
		self.resetChest()		
		self.game.modes.add(self.game.multiball_mode)


	def chestMatrixSwitches(self,sw):
		bOneRowKnownComplete = False
		bOneColKnownComplete = False
		objPlayer = self.game.players[self.game.current_player_index]
		self.game.score(100)
		iRowHit = int(sw.name[11])
		iColHit = int(sw.name[12])
		if(iRowHit > 0): #hit a row
			myrowdatadict = objPlayer.chestRowMatrix[iRowHit-1]
			iSumDataDict = sum(myrowdatadict.values())
			if iSumDataDict==5: #Already all complete!
				self.game.utilities.displayText(100,'TRY', 'DIFF','ROW', 'PLEASE',seconds=1,justify='center')
				pass
			elif iSumDataDict==0: #No rows complete, no reason to "for loop" here 
				self.game.lamps["chestMatrix" +str(iRowHit) +str(iColHit+1)].enable()
				myrowdatadict["chestMatrix" +str(iRowHit) +str(iColHit+1)] = True
				othercoldatadict = objPlayer.chestColMatrix[iColHit]
				othercoldatadict["chestMatrix" +str(iRowHit) +str(iColHit+1)] = True
			else:
				for keyA, valueA in sorted(myrowdatadict.items()):
					if valueA == False:
						self.game.lamps[keyA].enable() #Light same-named lamp
						myrowdatadict[keyA] = True
						othercoldatadict = objPlayer.chestColMatrix[int(keyA[12])-1]
						for keyB, valueB in sorted(othercoldatadict.items()):						
							if keyB == keyA:
								othercoldatadict[keyB] = True
								if iSumDataDict == 4:
									bOneRowKnownComplete = True
									self.game.utilities.displayText(100,'ROW', str(iRowHit),'MADE','',seconds=1,justify='center')								
								break
						break
			#Now check to see if the entire matrix is made			
			if bOneRowKnownComplete and sum(objPlayer.chestRowMatrix[4].values())==5 and sum(objPlayer.chestRowMatrix[3].values())==5 and sum(objPlayer.chestRowMatrix[2].values())==5 and sum(objPlayer.chestRowMatrix[1].values())==5 and sum(objPlayer.chestRowMatrix[0].values())==5:
				self.chestMade(self.chestFilledPoints)
				pass
		else:            #hit a col
			mycoldatadict = objPlayer.chestColMatrix[iColHit-1]
			iSumDataDict = sum(mycoldatadict.values())
			if iSumDataDict==5: #Already all complete!
				self.game.utilities.displayText(100,'TRY', 'DIFF','COL', 'PLEASE',seconds=1,justify='center')
				pass
			elif iSumDataDict==0: #No Cols complete, no reason to "for loop" here 
				self.game.lamps["chestMatrix" +str(iRowHit+1) +str(iColHit)].enable()
				mycoldatadict["chestMatrix" +str(iRowHit+1) +str(iColHit)] = True
				otherrowdatadict = objPlayer.chestRowMatrix[iRowHit]
				otherrowdatadict["chestMatrix" +str(iColHit) +str(iRowHit+1)] = True
			else:
				for keyA, valueA in sorted(mycoldatadict.items()):
					if valueA == False:
						self.game.lamps[keyA].enable() #Light same-named lamp
						mycoldatadict[keyA] = True
						otherrowdatadict = objPlayer.chestRowMatrix[int(keyA[11])-1]
						for keyB, valueB in sorted(otherrowdatadict.items()):						
							if keyB == keyA:
								otherrowdatadict[keyB] = True
								if iSumDataDict == 4:
									bOneColKnownComplete = True
									self.game.utilities.displayText(100,'COL', str(iColHit),'MADE', '',seconds=1,justify='center')								
								break
							
						break
			#Now check to see if the entire matrix is made			
			if bOneColKnownComplete and sum(objPlayer.chestColMatrix[4].values())==5 and sum(objPlayer.chestColMatrix[3].values())==5 and sum(objPlayer.chestColMatrix[2].values())==5 and sum(objPlayer.chestColMatrix[1].values())==5 and sum(objPlayer.chestColMatrix[0].values())==5:
				self.chestMade(self.chestFilledPoints)
			self.update_lamps()

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
