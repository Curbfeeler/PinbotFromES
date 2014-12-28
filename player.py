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