import wingdbstub
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
##     __  ______    _____   __   _________    __  _________
##    /  |/  /   |  /  _/ | / /  / ____/   |  /  |/  / ____/
##   / /|_/ / /| |  / //  |/ /  / / __/ /| | / /|_/ / __/   
##  / /  / / ___ |_/ // /|  /  / /_/ / ___ |/ /  / / /___   
## /_/  /_/_/  |_/___/_/ |_/   \____/_/  |_/_/  /_/_____/   
##
#################################################################################

###################################
# SYSTEM IMPORTS
###################################
import procgame.game
import pinproc
import locale
import yaml
import sys
import os
import logging
from OSC import *
#from SwitchGUI_Mode import *
from time import strftime

###################################
# MODE IMPORTS
###################################
from base import *
from attract import *
import scoredisplay
from scoredisplay import AlphaScoreDisplay #test and see about converting this to *
from chest import *
from skillshot import *
from utilities import *
from tilt import *
from player import *
from ballsaver import *
from bonus import *
from droptargets import *
from multiball import *
from trough import *
from jackpot import *
from shelter import *
from highscore import *
from bonusmultiplier import *
from vortex import *

#### Mini Modes ####
from mode_1 import *
from mode_2 import *
from mode_3 import *
from mode_4 import *
from mode_5 import *
from mode_6 import *
from mode_7 import *
from mode_8 import *
from mode_9 import *

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")

################################################
# GLOBAL PATH VARIABLES
################################################
game_machine_type = 'wpcAlphanumeric'
curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
settings_path = curr_file_path + "/config/settings.yaml"
game_data_path = curr_file_path + "/config/game_data.yaml"
game_data_template_path = curr_file_path + "/config/game_data_template.yaml"
settings_template_path = curr_file_path + "/config/settings_template.yaml"
game_machine_yaml = curr_file_path + "/config/pinbot.yaml"
game_music_path = curr_file_path + "/assets/music/"
game_sound_path = curr_file_path + "/assets/sounds/"
game_lampshows = curr_file_path + "/lamps/"

ballsPerGame = 3 # this will eventually be called from the config file

################################################
# GAME CLASS
################################################
class PinbotFromES(game.BasicGame):
	def __init__(self):
		super(PinbotFromES, self).__init__(pinproc.MachineTypeWPCAlphanumeric)
		self.load_config(game_machine_yaml)
		self.logging_enabled = True
		self.balls_per_game = ballsPerGame
		OSC_closed_switches = ['trough1','trough2','trough3','trough4','visorOpen']
		
		self.osc = modes.OSC_Mode(game=self, priority=1, closed_switches=OSC_closed_switches)
		self.modes.add(self.osc)
		#self.switchGui = SwitchInputGUI_Mode(self)
		
		### Set Logging Info ###
		# MJO: I find this log format annoying...
		# logging.basicConfig(filename='gamelog.txt',level=logging.INFO)
		logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

		#### Settings and Game Data ####
		self.load_settings(settings_template_path, settings_path)
		self.load_game_data(game_data_template_path, game_data_path)

		#### Setup Sound Controller ####
		self.sound = procgame.sound.SoundController(self)
		self.RegisterSound()

		#update audit data on boot up time
		self.game_data['Time Stamps']['Last Boot-Up'] =str(strftime("%d %b %Y %H:%M"))
		if self.game_data['Time Stamps']['First Boot-Up']=='Not Set':
			self.game_data['Time Stamps']['First Boot-Up'] = self.game_data['Time Stamps']['Last Boot-Up']
		self.save_game_data()

		#I added this line on 8/13/14
		self.reset()

	def reset(self):
		#super(PinbotFromES, self).reset()

		self.ball = 0
		self.old_players = []
		self.old_players = self.players[:]
		self.players = []
		self.current_player_index = 0
		self.modes.modes = []
		self.shooter_lane_status = 0
		self.tiltStatus = 0

		#setup high scores
		self.highscore_categories = []

		#### Classic High Score Data ####
		cat = highscore.HighScoreCategory()
		cat.game_data_key = 'ClassicHighScoreData'
		self.highscore_categories.append(cat)

		for category in self.highscore_categories:
			category.load_from_game(self)

		# MJO - CHANGE TO USE ALPHA
		#### Setup Alphanumeric Display Controller ####
		self.draw_desktop = True # config.value_for_key_path(keypath='virt_alpha_desktop', default=False)
		if self.draw_desktop:
			from desktop import Desktop
			self.desktop = Desktop()
			self.desktop.draw_window()

			self.desktop.load_images(curr_file_path+"/alpha_display/")

		#setup score display
		self.score_display = AlphaScoreDisplay(self, 0)

		self.alpha_score_display = AlphaScoreDisplay(self,0)
		self.modes.add(self.alpha_score_display)
		
		#### Setup Sound Controller ####
		#self.sound = procgame.sound.SoundController(self)
		#self.RegisterSound()

		#### Setup Lamp Controller ####
		self.lampctrl = procgame.lamps.LampController(self)
		self.lampctrlflash = procgame.lamps.LampController(self)
		self.RegisterLampshows()

		#### software version number ####
		self.revision = "1.0.0"

		#### Mode Definitions ####
		self.utilities = UtilitiesMode(self,0)
		
		self.base_mode = BaseGameMode(self,2)
		self.attract_mode = AttractMode(self,5)
		self.drops_mode = DropTargets(self,9)
		self.jackpot_mode = Jackpot(self,12)
		self.vortex_mode = VortexMode(self,97)
		self.bonusmultiplier_mode = BonusMultiplier(self,98)
		self.chest_mode = ChestMode(self,99)
		self.skillshot_mode = SkillshotMode(self,100)
		self.multiball_mode = Multiball(self,101)
		self.ballsaver_mode = BallSaver(self,199)
		self.tilt = Tilt(self,200)
		self.bonus_mode = Bonus(self,1000)
		self.highscore_mode = HighScore(self,1001)
		self.trough = Trough(self,2000)

		#### Mini Mode Definitions ####
		self.mode_1 = Mode1(self,30)
		self.mode_2 = Mode2(self,31)
		self.mode_3 = Mode3(self,32)
		self.mode_4 = Mode4(self,33)
		self.mode_5 = Mode5(self,34)
		self.mode_6 = Mode6(self,35)
		self.mode_7 = Mode7(self,36)
		self.mode_8 = Mode8(self,37)
		self.mode_9 = Mode9(self,38)
		
		
		#### Initial Mode Queue ####
		self.modes.add(self.utilities)
		self.modes.add(self.trough)
		self.modes.add(self.base_mode)

		#self.switchGui = SwitchInputGUI_Mode(self)

	def save_settings(self):
			super(PinbotFromES, self).save_settings(settings_path)

	def save_game_data(self):
			super(PinbotFromES, self).save_game_data(game_data_path)

	def RegisterSound(self):
		# Sound Settings:
		#self.sound.music_volume_offset = 10 #This will be hardcoded at 10 since I have external volume controls I will be using
		# Music Registration
		self.sound.register_music('main1', game_music_path + 'Transvolta_DiscoComputer.mp3')
		self.sound.register_music('shooter1', game_music_path + 'DigitalEmotion_GoGoYellowScreen_90secondShooterLoop.wav')
		self.sound.register_music('multiball_intro1', game_music_path + 'Automat_Droid_SansIntro.ogg')
		self.sound.register_music('multiball_loop1', game_music_path + 'Lifelike - So Electric.mp3')
		self.sound.register_music('game_over1', game_music_path + 'TheDroids_TheForcePartsIandII.mp3')

		self.sound.register_music('main2', game_music_path + 'Kraftwerk - Computer Love.mp3')
		self.sound.register_music('shooter2', game_music_path + 'SPACE - Magic Fly (1977 Music Video).mp3')
		self.sound.register_music('multiball_intro2', game_music_path + 'Ozric Tentacles - Eternal Wheel.mp3')
		self.sound.register_music('multiball_loop2', game_music_path + 'ELO_HereIsTheNews.mp3')
		self.sound.register_music('game_over2', game_music_path + 'Didier Marouani - Temps X (1979 Music Video).mp3')

		self.sound.register_music('main3', game_music_path + 'Transvolta_DiscoComputer.mp3')
		self.sound.register_music('shooter3', game_music_path + 'DigitalEmotion_GoGoYellowScreen_90secondShooterLoop.wav')
		self.sound.register_music('multiball_intro3', game_music_path + 'Automat_Droid.mp3')
		self.sound.register_music('multiball_loop3', game_music_path + 'ELO_HereIsTheNews.mp3')
		self.sound.register_music('game_over3', game_music_path + 'TheDroids_TheForcePartsIandII.mp3')

		# Sound FX Registration
		self.sound.register_sound('wakeUp', game_sound_path + 'Rooster.wav')
		self.sound.register_sound('sling', game_sound_path + 'slings.wav')
		self.sound.register_sound('jet', game_sound_path + 'pops.wav')
		self.sound.register_sound('skillshotAwarded', game_sound_path + 'News_Intro.wav')
		self.sound.register_sound('skillshotMissed', game_sound_path + 'Crickets.wav') #Crowd_Boo.wav
		self.sound.register_sound('vortexMade', game_sound_path + 'Ahhh_Pleasantly_Surprised.wav')
		#self.sound.register_sound('rightRampComplete', game_sound_path + 'sweep1.wav',new_sound_volume=.1) #Very loud sample
		# BallSaver Sounds #
		self.sound.register_sound('ball_saved', game_sound_path + 'ballsave.wav')
		# Drop Sounds #
		self.sound.register_sound('drop', game_sound_path + 'dropsdown.wav')
		# Eject Sounds #
		self.sound.register_sound('eject', game_sound_path + '1.wav')
		self.sound.register_sound('ejectsaucer', game_sound_path + '1.wav')
		# Outlane Sounds #
		self.sound.register_sound('outlane', game_sound_path + 'outlane_bad.wav')
		self.sound.register_sound('inlane', game_sound_path + '1.wav')
		# Game Start Voice #
		self.sound.register_sound('game_start', game_sound_path + '1.wav')
		# Ten Point Switch #
		self.sound.register_sound('game_start_rev', game_sound_path + '1.wav')
		self.sound.register_sound('game_start_takeoff', game_sound_path + 'Bottle_Rocket.wav')
		# Player Voice #
		self.sound.register_sound('player_1_vox', game_sound_path + 'welcomeplayer1vox.wav')
		self.sound.register_sound('player_2_vox', game_sound_path + 'welcomeplayer2vox.wav')
		self.sound.register_sound('player_3_vox', game_sound_path + 'welcomeplayer3vox.wav')
		self.sound.register_sound('player_4_vox', game_sound_path + 'welcomeplayer4vox.wav')
		self.sound.register_sound('player_1_up_vox', game_sound_path + 'player1vox.wav')
		self.sound.register_sound('player_2_up_vox', game_sound_path + 'player2vox.wav')
		self.sound.register_sound('player_3_up_vox', game_sound_path + 'player3vox.wav')
		self.sound.register_sound('player_4_up_vox', game_sound_path + 'player4vox.wav')
		# Multiball Sounds #
		self.sound.register_sound('multiball_1', game_sound_path + 'Spaceship_Alarm.mp3')
		self.sound.register_sound('main_loop_tape_stop', game_sound_path + 'music_001_main_loop_stop.wav',new_sound_volume=.5)
		self.sound.register_sound('short_out_1', game_sound_path + '1.wav')
		self.sound.register_sound('short_out_2', game_sound_path + '1.wav')
		# Ball Lock Vocals #
		self.sound.register_sound('ball_lock_1', game_sound_path + '1.wav')
		self.sound.register_sound('ball_lock_2', game_sound_path + '1.wav')
		# Jackpot Vocals #
		self.sound.register_sound('jackpot', game_sound_path + '1.wav')
		self.sound.register_sound('jackpot_increase', game_sound_path + '1.wav')
		self.sound.register_sound('jackpot_lit', game_sound_path + '1.wav')
		# Complete Shot Vocals #
		self.sound.register_sound('complete_shot', game_sound_path + '1.wav')


		self.sound.set_volume(10)

	def RegisterLampshows(self):
		self.lampctrl.register_show('attract1', game_lampshows + 'attract_grow.lampshow')

		self.lampctrl.register_show('center_ramp_1', game_lampshows + 'centerramp_complete_a.lampshow')
		self.lampctrlflash.register_show('bonus_feat_left', game_lampshows + 'bonus_feature_left.lampshow')
		self.lampctrlflash.register_show('bonus_feat_right', game_lampshows + 'bonus_feature_right.lampshow')
		self.lampctrlflash.register_show('bonus_total', game_lampshows + 'bonus_total_a.lampshow')
		self.lampctrlflash.register_show('multiball_intro_1', game_lampshows + 'multiball_intro.lampshow')

		self.lampctrl.register_show('jackpot', game_lampshows + 'jackpot_awarded_a.lampshow')
		self.lampctrl.register_show('skillshot', game_lampshows + 'skillshot_standard_awarded.lampshow')
		self.lampctrl.register_show('super_skillshot', game_lampshows + 'skillshot_super_awarded.lampshow')
		self.lampctrl.register_show('zone_collected', game_lampshows + 'zones_zonecollected_a.lampshow')

	def create_player(self, name):
		return Player(name)
		
################################################
# GAME DEFINITION
################################################
def main():
	game = PinbotFromES()
	game.reset()
	game.run_loop()

if __name__ == '__main__':
	main()