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
		bOneRowKnownComplete = False
		bOneColKnownComplete = False
		objPlayer = self.game.players[self.game.current_player_index]
		self.game.score(100)
		iRowHit = int(sw.name[11])
		iColHit = int(sw.name[12])
		if(iRowHit > 0): #hit a row
			datadict = objPlayer.chestRowMatrix[iRowHit-1]
			iSumDataDict = sum(datadict.values())
			if iSumDataDict==5: #Already all complete!
				self.game.utilities.displayText(100,'TRY DIFF','ROW PLEASE',seconds=1,justify='center')
				pass
			elif iSumDataDict==0: #No rows complete, no reason to "for loop" here 
				self.game.lamps["chestMatrix" +str(iRowHit) +str(iColHit+1)].enable()
				datadict["chestMatrix" +str(iRowHit) +str(iColHit+1)] = True
				otherdatadict = objPlayer.chestColMatrix[iColHit]
				otherdatadict["chestMatrix" +str(iRowHit) +str(iColHit+1)] = True
			else:
				for keyA, valueA in sorted(datadict.items()):
					if valueA == False:
						self.game.lamps[keyA].enable() #Light same-named lamp
						datadict[keyA] = True
						otherdatadict = objPlayer.chestColMatrix[int(keyA[12])-1]
						for keyB, valueB in sorted(otherdatadict.items()):						
							if keyB == keyA:
								otherdatadict[keyB] = True
								break
						if iSumDataDict == 4:
							bOneRowKnownComplete = True
							self.game.utilities.displayText(100,'ROW ' +str(iRowHit),'MADE',seconds=1,justify='center')
						break
			#Now check to see if the entire matrix is made			
			if bOneRowKnownComplete and sum(objPlayer.chestRowMatrix[4].values())==5 and sum(objPlayer.chestRowMatrix[3].values())==5 and sum(objPlayer.chestRowMatrix[2].values())==5 and sum(objPlayer.chestRowMatrix[1].values())==5 and sum(objPlayer.chestRowMatrix[0].values())==5:
				self.game.utilities.displayText(100,'GOOD JOB','ALL DONE',seconds=1,justify='center')
				pass
		else:            #hit a col
			datadict = objPlayer.chestColMatrix[iColHit-1]
			iSumDataDict = sum(datadict.values())
			if iSumDataDict==5: #Already all complete!
				self.game.utilities.displayText(100,'TRY DIFF','COL PLEASE',seconds=1,justify='center')
				pass
			elif iSumDataDict==0: #No Cols complete, no reason to "for loop" here 
				self.game.lamps["chestMatrix" +str(iRowHit+1) +str(iColHit)].enable()
				datadict["chestMatrix" +str(iRowHit+1) +str(iColHit)] = True
				otherdatadict = objPlayer.chestRowMatrix[iRowHit]
				otherdatadict["chestMatrix" +str(iColHit) +str(iRowHit+1)] = True
			else:
				for keyA, valueA in sorted(datadict.items()):
					if valueA == False:
						self.game.lamps[keyA].enable() #Light same-named lamp
						datadict[keyA] = True
						otherdatadict = objPlayer.chestRowMatrix[int(keyA[12])-1]
						for keyB, valueB in sorted(otherdatadict.items()):						
							if keyB == keyA:
								otherdatadict[keyB] = True
								break
							if iSumDataDict == 4:
								bOneColKnownComplete = True
								self.game.utilities.displayText(100,'COL ' +str(iColHit),'MADE',seconds=1,justify='center')
						break
			#Now check to see if the entire matrix is made			
			if bOneColKnownComplete and sum(objPlayer.chestColMatrix[4].values())==5 and sum(objPlayer.chestColMatrix[3].values())==5 and sum(objPlayer.chestColMatrix[2].values())==5 and sum(objPlayer.chestColMatrix[1].values())==5 and sum(objPlayer.chestColMatrix[0].values())==5:
				self.game.utilities.displayText(100,'GOOD JOB','ALL DONE',seconds=1,justify='center')
				pass


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
