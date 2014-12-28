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
##     _______  ____________  ___       ____  ___    __    __ 
##    / ____/ |/ /_  __/ __ \/   |     / __ )/   |  / /   / / 
##   / __/  |   / / / / /_/ / /| |    / __  / /| | / /   / /  
##  / /___ /   | / / / _, _/ ___ |   / /_/ / ___ |/ /___/ /___
## /_____//_/|_|/_/ /_/ |_/_/  |_|  /_____/_/  |_/_____/_____/
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
import scoredisplay
from scoredisplay import AlphaScoreDisplay
#from base import AlphaScoreDisplay

class ExtraBall(game.Mode):
	def __init__(self, game):
			super(SkillshotMode, self).__init__(game=game, priority=7)
			####################
			#Mode Setup
			####################
			
			#self.score_display = AlphaScoreDisplay(self.game,0)
			#gameover_mode = GameOver(game)
			
			#self.checkForStuckBalls()

	def mode_started(self):
		self.lightExtraBallLamps()

	def enableACSelect(self):
		self.game.coils.acSelect.enable() #for Flashers

	def mode_stopped(self):
		self.stopExtraBallLamps()
		return super(SkillshotMode, self).mode_stopped()

	def update_display(self):
		self.p = self.game.current_player()
		self.score_display.set_text(str(self.p.score),0)
		self.score_display.set_text("Ball "+str(self.game.ball),1)
		
	def startExtraBallLamps(self):
		self.game.lamps.shootAgain.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)

	def stopExtraBallLamps(self):
		self.game.lamps.shootAgain.disable()

	#def score(self, points):
		#p = self.game.current_player()
		#p.score += points
		#self.cancel_delayed('updatescore')
		#self.delay(name='updatescore',delay=0.5,handler=self.update_display)

	#def sw_onRamp50k_active(self, sw):
		##need to score
		#self.game.modes.remove(self)
		#return procgame.game.SwitchContinue