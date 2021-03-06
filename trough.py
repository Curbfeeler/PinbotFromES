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
##   __________  ____  __  __________  __
##  /_  __/ __ \/ __ \/ / / / ____/ / / /
##   / / / /_/ / / / / / / / / __/ /_/ / 
##  / / / _, _/ /_/ / /_/ / /_/ / __  /  
## /_/ /_/ |_|\____/\____/\____/_/ /_/   
## 
#################################################################################

import procgame.game
import procgame.dmd
import logging


class Trough(procgame.game.Mode):
	"""Manages trough by providing the following functionality:

		- Keeps track of the number of balls in play
		- Keeps track of the number of balls in the trough
		- Launches one or more balls on request and calls a launch_callback when complete, if one exists.
		- Auto-launches balls while ball save is active (if linked to a ball save object
		- Identifies when balls drain and calls a registered drain_callback, if one exists.
		- Maintains a count of balls locked in playfield lock features (if externally incremented) and adjusts the count of number of balls in play appropriately.  This will help the drain_callback distinguish between a ball ending or simply a multiball ball draining.

	Parameters:

		'game': Parent game object.
		'position_switchnames': List of switchnames for each ball position in the trough.
		'eject_switchname': Name of switch in the ball position the feeds the shooter lane.
		'eject_coilname': Name of coil used to put a ball into the shooter lane.
		'early_save_switchnames': List of switches that will initiate a ball save before the draining ball reaches the trough (ie. Outlanes).
		'shooter_lane_switchname': Name of the switch in the shooter lane.  This is checked before a new ball is ejected.
		'drain_callback': Optional - Name of method to be called when a ball drains (and isn't saved).	
	"""
	def __init__(self, game, priority, position_switchnames=None, eject_switchname=None, eject_coilname=None, early_save_switchnames=None, shooter_lane_switchname=None, drain_callback=None):
		super(Trough, self).__init__(game, priority)

		#setup logging
		self.log = logging.getLogger('pinbot.trough')

		#setup vars
		self.position_switchnames = []			#position_switchnames
		self.early_save_switchnames = []
		self.eject_switchname = None			#eject_switchname
		self.eject_coilname = None				#eject_coilname
		self.shooter_lane_switchname = None		#shooter_lane_switchname
		self.drain_callback = drain_callback

                self.extra_ball = False     # Is the ball sitting in the lane an extra ball awarded
		#populate vars from yaml*
		for switch in self.game.switches.items_tagged('trough'):
			self.position_switchnames.append(switch.name)
			self.log.info("Trough Switch is:"+switch.name)

		for switch in self.game.switches.items_tagged('early_save'):
			self.early_save_switchnames.append(switch.name)
			self.log.info("Early Save Switch is:"+switch.name)

		for switch in self.game.switches.items_tagged('outhole'):
			self.outhole_switchname = switch.name
			self.log.info("Outhole Switch is:"+self.outhole_switchname)

		for switch in self.game.switches.items_tagged('trough_eject'):
			self.eject_switchname = switch.name
			self.log.info("Trough Eject Switch is:"+self.eject_switchname)

		for switch in self.game.switches.items_tagged('shooter_lane'):
			self.shooter_lane_switchname = switch.name
			self.log.info("Shooter Lane Switch is:"+self.shooter_lane_switchname)

		for coil in self.game.coils.items_tagged('outhole'):
			self.outhole_coilname = coil.name
			self.log.info("Outhole Coil is:"+self.outhole_coilname)

		for coil in self.game.coils.items_tagged('trough_eject'):
			self.eject_coilname = coil.name
			self.log.info("Trough Eject Coil is:"+self.eject_coilname)



		# Install switch handlers.
		# Use a delay of 750ms which should ensure balls are settled.
		for switch in self.position_switchnames:
			self.add_switch_handler(name=switch, event_type='active', delay=1.0, handler=self.position_switch_handler)

		for switch in self.position_switchnames:
			self.add_switch_handler(name=switch, event_type='inactive', delay=1.0, handler=self.position_switch_handler)

		# Install early ball_save switch handlers.
		#for switch in self.early_save_switchnames:
			#self.add_switch_handler(name=switch, event_type='active', delay=None, handler=self.early_save_switch_handler)

		# Install outhole switch handler.
		#self.add_switch_handler(name=self.outhole_switchname, event_type='active', delay=.20, handler=self.outhole_switch_handler)

                # Install shooter lane handler
                self.add_switch_handler(name=self.shooter_lane_switchname, event_type='active', delay=1.0, handler=self.shooter_lane_switch_handler)
		# Reset variables

                # This is the number of balls not in the trough or locks, so physically in play
		self.num_balls_in_play = 0

                # This is the number of balls physically sitting in locks, so not in play and not in the trough
		self.num_balls_locked = 0

		self.num_balls_to_launch = 0
		self.num_balls_to_stealth_launch = 0
		self.launch_in_progress = False

		self.ball_save_active = False

		""" Callback called when a ball is saved.  Used optionally only when ball save is enabled (by a call to :meth:`Trough.enable_ball_save`).  Set externally if a callback should be used. """
		self.ball_save_callback = None

		""" Method to get the number of balls to save.  Set externally when using ball save logic."""
		self.num_balls_to_save = None

		self.launch_callback = None

		self.debug()

	#def mode_tick(self):
		#self.debug()

	def debug(self):
		self.log.info("BALL" +str(self.game.ball) +"/" +str(self.game.balls_per_game) +",B-IN-PLY"+str(self.num_balls_in_play) + ", B-LCKD" + str(self.num_balls_locked)+ ", TRO" + str(self.num_balls())+", player locks "+str(self.game.utilities.get_player_stats('balls_locked')))
		#self.game.utilities.arduino_write_number(number=self.num_balls())		
		self.delay(name='launch', event_type=None, delay=1.0, handler=self.debug)
		

	def state_str(self):
		return '%d/%d balls' % (self.num_balls(), self.game.num_balls_total)


	def enable_ball_save(self, enable=True):
		"""Used to enable/disable ball save logic."""
		self.ball_save_active = enable

	#def early_save_switch_handler(self, sw):
		#if self.ball_save_active:
			# Only do an early ball save if a ball is ready to be launched.
			# Otherwise, let the trough switches take care of it.
			#if self.game.switches[self.eject_switchname].is_active():
				#self.launch_balls(1, self.ball_save_callback, stealth=True)

		#add handler for outhole
	#def sw_outhole_active_for_500ms(self, sw):
	def sw_outhole_closed_for_1s(self, sw):
	#def outhole_switch_handler(self,sw):
		self.log.info('Outhole switch handler')

		self.log.info("Balls in play before pulse = "+str(self.num_balls_in_play))
		self.log.info("Balls in trough before pulse = "+str(self.num_balls()))			

		#self.delay(name='dummy', event_type=None, delay=1.0, handler=self.dummy)
                # Kick the ball into the trough
		self.game.utilities.acCoilPulse('outholeKicker_Knocker')
		if self.num_balls_in_play > 0:
			self.num_balls_in_play -= 1
			
		self.delay(name='dummy', event_type=None, delay=1.0, handler=self.dummy)			

		self.log.info("Balls in play after pulse = "+str(self.num_balls_in_play))
		self.log.info("Balls in trough after pulse = "+str(self.num_balls()))			


                # Schedule a call for one second from now to let things settle
                self.delay('outhole_recheck',delay=1.0,handler=self.outhole_recheck)

        # Called one second after the outhole is handled.  Will call the handler again if there is still
        # a ball in the outhole, otherwise will continue with rest of outhole processing
        def outhole_recheck(self):
		#self.delay(name='dummy', event_type=None, delay=1.0, handler=self.dummy)
		if self.game.switches.outhole.is_closed() == True:
			self.log.info('Calling outhole_recheck, is_closed is true')
			self.sw_outhole_closed_for_1s('Dummy')
		else:
			self.log.info('Calling outhole_recheck, is_closed is false')
			# If ball save is active, save it but wait first for one second for the trough to settle
			if (self.game.utilities.get_player_stats('ballsave_active') == True):
				self.game.ballsaver_mode.saveBall()
			# If ball save isn't active, check for end of multiball
			elif(self.game.utilities.get_player_stats('multiball_running') != 'None'):
				self.checkForEndOfMultiball()
			if self.num_balls_in_play == 0: #Last ball in play
				self.game.utilities.setBallInPlay(False) # Will need to use the trough mode for this
				self.game.base_mode.finish_ball()

	def checkForEndOfMultiball(self):
		if (self.num_balls() >= 3 and self.game.utilities.get_player_stats('multiball_running') == 'Standard' ):
			self.game.multiball_mode.stopMultiball()
                elif self.game.utilities.get_player_stats('multiball_running') == 'Quick':
                        self.game.quick_multiball_mode.stopMultiball()

	# Switches will change states a lot as balls roll down the trough.
	# So don't go through all of the logic every time.  Keep resetting a
	# delay function when switches change state.  When they're all settled,
	# the delay will call the real handler (check_switches).
	def position_switch_handler(self, sw):
		self.cancel_delayed('check_switches')
		self.delay(name='check_switches', event_type=None, delay=0.50, handler=self.check_switches)

	def check_switches(self):
                self.log.info('Trough settled')
		if self.num_balls_in_play > 0:
			# Base future calculations on how many balls the machine 
			# thinks are currently installed.
			num_current_machine_balls = self.game.num_balls_total
			temp_num_balls = self.num_balls()
			if self.ball_save_active:

				if self.num_balls_to_save:
					num_balls_to_save = self.num_balls_to_save()
				else:
					num_balls_to_save = 0

				# Calculate how many balls shouldn't be in the 
				# trough assuming one just drained
				num_balls_out = self.num_balls_locked + \
					(num_balls_to_save - 1)
				# Translate that to how many balls should be in 
				# the trough if one is being saved.
				balls_in_trough = num_current_machine_balls - \
						  num_balls_out

				if (temp_num_balls - \
				    self.num_balls_to_launch) >= balls_in_trough:
                                        self.log.info("Trough thinks it needs another ball to launch")
					self.launch_balls(1, self.ball_save_callback, \
							  stealth=True)
				else:
					# If there are too few balls in the trough.  
					# Ignore this one in an attempt to correct 
					# the tracking.
					return 'ignore'
			else:
				# Calculate how many balls should be in the trough 
				# for various conditions.
				num_trough_balls_if_ball_ending = \
					num_current_machine_balls - self.num_balls_locked
				num_trough_balls_if_multiball_ending = \
					num_trough_balls_if_ball_ending - 1
				num_trough_balls_if_multiball_drain = \
					num_trough_balls_if_ball_ending - \
					(self.num_balls_in_play - 1)
                                self.log.info("Ball ending = "+str(num_trough_balls_if_ball_ending)+ \
                                    ", Multiball ending = "+str(num_trough_balls_if_multiball_ending) + \
                                    ", Multiball drain = "+str(num_trough_balls_if_multiball_drain))


				# The ball should end if all of the balls 
				# are in the trough.

				if temp_num_balls == num_current_machine_balls or \
				   temp_num_balls == num_trough_balls_if_ball_ending:
					self.num_balls_in_play = 0
					if self.drain_callback:
						self.drain_callback()
				# Multiball is ending if all but 1 ball are in the trough.
				# Shouldn't need this, but it fixes situations where 
				# num_balls_in_play tracking
				# fails, and those situations are still occuring.
				elif temp_num_balls == \
				     num_trough_balls_if_multiball_ending:
					self.num_balls_in_play = 1
					if self.drain_callback:
						self.drain_callback()
				# Otherwise, another ball from multiball is draining 
				# if the trough gets one more than it would have if 
				# all num_balls_in_play are not in the trough.
				elif temp_num_balls ==  \
				     num_trough_balls_if_multiball_drain:
					# Fix num_balls_in_play if too low.
					if self.num_balls_in_play < 3:
						self.num_balls_in_play = 2
					# otherwise subtract 1
					else:
                                #else:
                                            self.num_balls_in_play -= 1
				#	if self.drain_callback:
				#		self.drain_callback()
                                self.num_balls_in_play = 4 - self.num_balls() - self.num_balls_locked

	# Count the number of balls in the trough by counting active trough switches.
	def num_balls(self):
		"""Returns the number of balls in the trough."""
		ball_count = 0
		for switch in self.position_switchnames:
			if self.game.switches[switch].is_active():
				ball_count += 1
		return ball_count

        # Perform physical lock count.  Tracking this in software can be error prone if one scenario is missed
        # and there is always the possibility that a ball might bounce somewhere unexpected.  If we actually
        # count the locks with a ball in by checking the switches then we should be good.
        def lock_count(self):
            lock_count = 0
            for switch in ['singleEject','rightEyeball','leftEyeball']:
                if self.game.switches[switch].is_active():
                    lock_count += 1
            self.num_balls_locked = lock_count

	def is_full(self):
		return self.num_balls() == self.game.num_balls_total

	# Either initiate a new launch or add another ball to the count of balls
	# being launched.  Make sure to keep a separate count for stealth launches
	# that should not increase num_balls_in_play.
	def launch_balls(self, num, callback=None, stealth=False):

		self.log.info('Calling: launch_balls,' +str(num))
		"""Launches balls into play.

			'num': Number of balls to be launched.  
			If ball launches are still pending from a previous request, 
			this number will be added to the previously requested number.

			'callback': If specified, the callback will be called once
			all of the requested balls have been launched.

			'stealth': Set to true if the balls being launched should NOT
			be added to the number of balls in play.  For instance, if
			a ball is being locked on the playfield, and a new ball is 
			being launched to keep only 1 active ball in play,
			stealth should be used.
		"""

		self.num_balls_to_launch += num
		self.log.info('in launch_balls now self.num_balls_to_launch = ' +str(self.num_balls_to_launch))		
                #self.autolaunch = autolaunch
		#if stealth:
			#self.num_balls_to_stealth_launch += num
		if not self.launch_in_progress:
			self.launch_in_progress = True
			if callback:
				self.launch_callback = callback
			self.common_launch_code()

	# This is the part of the ball launch code that repeats for multiple launches.
	def common_launch_code(self):
		# Only kick out another ball if the last ball is gone from the 
		# shooter lane.
		
		if self.game.switches[self.shooter_lane_switchname].is_inactive():
			self.log.info('common_launch_code says... shooter is clear')
			self.num_balls_to_launch -= 1
			#self.log.info("Balls in play before pulse = "+str(self.num_balls_in_play))
			#self.log.info("Balls in trough before pulse = "+str(self.num_balls()))			
			self.delay(name='dummy', event_type=None, delay=1.0, handler=self.dummy)
			#pulse coil
			self.game.utilities.acCoilPulse(coilname='feedShooter_UpperPFFLash',pulsetime=100)
			self.delay(name='dummy', event_type=None, delay=1.0, handler=self.dummy)

			#if self.game.switches[self.shooter_lane_switchname].is_active():
			#self.num_balls_to_launch -= 1
			#self.num_balls_in_play += 1
				
			#self.log.info("Balls in play after pulse = "+str(self.num_balls_in_play))
			#self.log.info("Balls in trough after pulse = "+str(self.num_balls()))			
			

                        #If the ball in the shooter lane is an extra ball which a player has been awarded
                        #then decrement the number of extra balls available and flag the situation so the lamp
                        #handler can flash the lamp
			if self.game.utilities.get_player_stats('extra_balls') > 0:
                            self.game.utilities.set_player_stats('extra_balls',-1,mode='add')
                            self.extra_ball = True
                        else:
                            self.extra_ball = False
                            
                        self.update_lamps()

			# Only increment num_balls_in_play if there are no more 
			# stealth launches to complete.
			if self.num_balls_to_stealth_launch > 0:
				self.num_balls_to_stealth_launch -= 1
			else:
				self.num_balls_in_play += 1
			# If more balls need to be launched, delay 1 second 
			if self.num_balls_to_launch > 0:
				self.delay(name='launch', event_type=None, delay=1.0, handler=self.common_launch_code)
			else:
				self.launch_in_progress = False
				if self.launch_callback:
					self.launch_callback()
		# Otherwise, wait 1 second before trying again.
		else:
			self.log.info('common_launch_code says... shooter not clear')
			self.delay(name='launch', event_type=None, delay=1.0, \
				   handler=self.common_launch_code)

	def dummy(self):
		self.log.info('Calling: dummy')
		pass

	def shooter_lane_switch_handler(self,sw):
		self.log.info("Placeholder until autolauncher works")
            #if self.autolaunch == True:
                #self.log.info("Shooter lane autolaunch = "+str(self.autolaunch))
                ##self.game.coils.autoLaunch.pulse(100)
                #self.autolaunch=False

        # The trough mode can handle the extra ball lamp
        def update_lamps(self):
            if self.extra_ball == True:
                self.game.lamps.shootAgain.schedule(schedule=0xFF00FF00)
            elif self.game.utilities.get_player_stats('extra_balls') > 0:
                self.game.lamps.shootAgain.enable()
            else:
                self.game.lamps.shootAgain.disable()

        def mode_stopped(self):
		self.cancel_delayed('check_switches')

        def sw_debug_active(self,sw):
            self.log.info("Balls in play = "+str(self.num_balls_in_play))
            self.log.info("Balls in trough = "+str(self.num_balls()))
        