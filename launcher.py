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
##    __    ___   __  ___   __________  ____________ 
##    / /   /   | / / / / | / / ____/ / / / ____/ __ \
##   / /   / /| |/ / / /  |/ / /   / /_/ / __/ / /_/ /
##  / /___/ ___ / /_/ / /|  / /___/ __  / /___/ _, _/ 
## /_____/_/  |_\____/_/ |_/\____/_/ /_/_____/_/ |_|  
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc

class Launcher_Mode(game.Mode):
	def __init__(self, game):
			super(Launcher_Mode, self).__init__(game=game, priority=3)

	def mode_started(self):
		self.game.coils.flipperEnable.enable()

	def mode_stopped(self):
		pass
			
	def sw_startButton_active_for_50ms(self, sw):
		#if self.troughIsFull()==True:
			#Game Starting
			#self.game.modes.remove(self)
			return procgame.game.SwitchContinue

	def sw_outhole_active_for_1s(self, sw):
		self.game.coils.acSelect.disable()
		self.game.coils.flipperEnable.disable()
		self.game.coils.outholeKicker_Knocker.pulse(50)
		self.game.score_display.set_text("GAME OVER",0)
		self.game.score_display.set_text("Press Start",1)
		return procgame.game.SwitchStop

	def sw_jetLeft_active(self, sw):
		return procgame.game.SwitchStop

	def sw_jetRight_active(self, sw):
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		return procgame.game.SwitchStop