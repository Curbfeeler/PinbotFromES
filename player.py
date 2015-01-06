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
##     ____  __    _____  ____________     ______________  ___________
##    / __ \/ /   /   \ \/ / ____/ __ \   / ___/_  __/   |/_  __/ ___/
##   / /_/ / /   / /| |\  / __/ / /_/ /   \__ \ / / / /| | / /  \__ \ 
##  / ____/ /___/ ___ |/ / /___/ _, _/   ___/ // / / ___ |/ /  ___/ / 
## /_/   /_____/_/  |_/_/_____/_/ |_|   /____//_/ /_/  |_/_/  /____/  
## 
#################################################################################

import procgame.game

class Player(procgame.game.Player):

	def __init__(self, name):
			super(Player, self).__init__(name)

			### Create Player Stats Array ############################
			self.player_stats = {}

			### General Stats ########################################
			self.player_stats['ball_in_play']=False
                        self.player_stats['extra_balls']=0
                        self.player_stats['extra_ball_lit']=False

			### Ball Saver ###########################################
			self.player_stats['ballsave_active']=False
			self.player_stats['ballsave_timer_active']=False

			### Bonus and Status #####################################
			self.player_stats['status']=''
			self.player_stats['bonus_x']=1
			self.player_stats['energy_bonus']=0

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


			### Chest Matrix Stats ####################################
			self.chestMatrix01={} #YellowRow
			self.chestMatrix01['chestMatrix11']=False
			self.chestMatrix01['chestMatrix12']=False
			self.chestMatrix01['chestMatrix13']=False
			self.chestMatrix01['chestMatrix14']=False
			self.chestMatrix01['chestMatrix15']=False
			self.chestMatrix02={} #BlueRow
			self.chestMatrix02['chestMatrix21']=False
			self.chestMatrix02['chestMatrix22']=False
			self.chestMatrix02['chestMatrix23']=False
			self.chestMatrix02['chestMatrix24']=False
			self.chestMatrix02['chestMatrix25']=False
			self.chestMatrix03={} #OrangeRow
			self.chestMatrix03['chestMatrix31']=False
			self.chestMatrix03['chestMatrix32']=False
			self.chestMatrix03['chestMatrix33']=False
			self.chestMatrix03['chestMatrix34']=False
			self.chestMatrix03['chestMatrix35']=False
			self.chestMatrix04={} #GreenRow
			self.chestMatrix04['chestMatrix41']=False
			self.chestMatrix04['chestMatrix42']=False
			self.chestMatrix04['chestMatrix43']=False
			self.chestMatrix04['chestMatrix44']=False
			self.chestMatrix04['chestMatrix45']=False
			self.chestMatrix05={} #RedRow
			self.chestMatrix05['chestMatrix51']=False
			self.chestMatrix05['chestMatrix52']=False
			self.chestMatrix05['chestMatrix53']=False
			self.chestMatrix05['chestMatrix54']=False
			self.chestMatrix05['chestMatrix55']=False

			self.chestMatrix10={} #YellowCol
			self.chestMatrix10['chestMatrix11']=False
			self.chestMatrix10['chestMatrix21']=False
			self.chestMatrix10['chestMatrix31']=False
			self.chestMatrix10['chestMatrix41']=False
			self.chestMatrix10['chestMatrix51']=False
			self.chestMatrix20={} #BlueCol  
			self.chestMatrix20['chestMatrix12']=False
			self.chestMatrix20['chestMatrix22']=False
			self.chestMatrix20['chestMatrix32']=False
			self.chestMatrix20['chestMatrix42']=False
			self.chestMatrix20['chestMatrix52']=False
			self.chestMatrix30={} #OrangeCol
			self.chestMatrix30['chestMatrix13']=False
			self.chestMatrix30['chestMatrix23']=False
			self.chestMatrix30['chestMatrix33']=False
			self.chestMatrix30['chestMatrix43']=False
			self.chestMatrix30['chestMatrix53']=False
			self.chestMatrix40={} #GreenCol 
			self.chestMatrix40['chestMatrix14']=False
			self.chestMatrix40['chestMatrix24']=False
			self.chestMatrix40['chestMatrix34']=False
			self.chestMatrix40['chestMatrix44']=False
			self.chestMatrix40['chestMatrix54']=False
			self.chestMatrix50={} #RedCol   
			self.chestMatrix50['chestMatrix15']=False
			self.chestMatrix50['chestMatrix25']=False
			self.chestMatrix50['chestMatrix35']=False
			self.chestMatrix50['chestMatrix45']=False
			self.chestMatrix50['chestMatrix55']=False
			
			self.chestRowMatrix = []
			self.chestRowMatrix.append(self.chestMatrix01)
			self.chestRowMatrix.append(self.chestMatrix02)
			self.chestRowMatrix.append(self.chestMatrix03)
			self.chestRowMatrix.append(self.chestMatrix04)
			self.chestRowMatrix.append(self.chestMatrix05)

			self.chestColMatrix = []
			self.chestColMatrix.append(self.chestMatrix10)
			self.chestColMatrix.append(self.chestMatrix20)
			self.chestColMatrix.append(self.chestMatrix30)
			self.chestColMatrix.append(self.chestMatrix40)
			self.chestColMatrix.append(self.chestMatrix50)


			### Drop Target Stats ####################################
			self.player_stats['drop_banks_completed']=0

			### Jackpot Stats ########################################
			self.player_stats['jackpot_level']=1
			self.player_stats['total_jackpots_collected']=0
			self.player_stats['last_multiball_jackpots_collected']=0
			self.player_stats['jackpot_lit']=False

			### Multiball Stats ######################################
			self.player_stats['lock1_lit']=False
			self.player_stats['lock2_lit']=False
			self.player_stats['lock3_lit']=False
			self.player_stats['multiball_running']=False
			self.player_stats['balls_locked']=0

			### Right Ramp Stats #####################################
			self.player_stats['fault_visits']=0
			self.player_stats['million_lit']=False

			### Skillshot ############################################
			self.player_stats['skillshot_active']=False
			self.player_stats['skillshot_x']=1
			self.player_stats['chestmade_x']=1
			### Zone Status Stats ####################################
			self.player_stats['active_zone_limit']=3
			self.player_stats['zones_visited']=0
			self.player_stats['zone1_status']=-1
			self.player_stats['zone2_status']=-1
			self.player_stats['zone3_status']=-1
			self.player_stats['zone4_status']=-1
			self.player_stats['zone5_status']=-1
			self.player_stats['zone6_status']=-1
			self.player_stats['zone7_status']=-1
			self.player_stats['zone8_status']=-1
			self.player_stats['zone9_status']=-1

			### Mode Status Stats ####################################
			self.player_stats['mode1_status']=-1
			self.player_stats['mode2_status']=-1
			self.player_stats['mode3_status']=-1
			self.player_stats['mode4_status']=-1
			self.player_stats['mode5_status']=-1
			self.player_stats['mode6_status']=-1
			self.player_stats['mode7_status']=-1
			self.player_stats['mode8_status']=-1
			self.player_stats['mode9_status']=-1