import procgame.game
import pinproc
import wx

class SwitchInputGUI_Mode(procgame.game.Mode):
    """docstring for SwitchInputGUI_Mode"""
    switchmatrix = {}

    def __init__(self, game):
        super(SwitchInputGUI_Mode, self).__init__(game=game, priority=100)

        app = wx.App(redirect=False)
        frame = wx.Frame(None, -1, 'Switch Matrix OSC Client')
        gs = wx.GridSizer(9, 8, 5, 5) # rows, cols, gap
        # app.MainLoop()
        
        self.states = {}
        
        sw_sorted = []
        for sw in self.game.switches:
            sw_sorted += [sw.number]
        sw_sorted = sorted(sw_sorted)

        # switches.sort(lambda x, y: y.yaml_number < x.yaml_number)
        # switches = sorted(self.game.switches.items(), key=operator.itemgetter(1))

        for sw_num in sw_sorted:
            print("looking up %s" % sw_sorted)
            sw = self.game.switches[sw_num]
#           for event_type in ['closed']:
            switch_code = str(sw.yaml_number[1:])
            print("binding " + switch_code)
            sname = sw.name

            button = self.makeButton(frame, sname, switch_code, sw.number)
            gs.Add(button, 0, wx.EXPAND)

            self.add_switch_handler(name=sw.name, event_type='closed', delay=None, handler=self._switch_changed_closed)
            self.add_switch_handler(name=sw.name, event_type='open', delay=None, handler=self._switch_changed_open)
            self._switch_changed_open(sw);

        frame.SetSizer(gs)
        frame.Show()
        # app.MainLoop()
                

##############################################
# GUI Event Handlers
##############################################
                                                                                                                                                                                                                                                                                        
    def onLeftButtonDOWN(self,event):
        self.sendOSC(event, True)
        print "LEFT Button  [%s] DOWN!" % event.EventObject.id

    def onLeftButtonUP(self,event):
        self.sendOSC(event, False)
        print "LEFT Button [%s] UP!" % event.EventObject.id

    def onRightButton(self,event):
        btn = event.EventObject
        self.sendOSC(event, not(self.states[btn.id]))
        print "RIGHT Button [%s] pressed!" % btn.id

    def sendOSC(self, evt_src, new_state=None):
        btn = evt_src.EventObject

        # addr = '/sw/%s' % btn.GetLabel()
        switch_number = btn.game_num#pinproc.decode(self.game.machine_type, btn.id)
        if(self.states[btn.id]==False and new_state==True):
            btn.SetBackgroundColour(wx.GREEN)
            self.states[btn.id]=True
            new_state = pinproc.EventTypeSwitchClosedDebounced
            self.game.desktop.key_events.append({'type': new_state, 'value': switch_number})  # add these switch close events to the queue
        elif(self.states[btn.id]==True and new_state==False):
            btn.SetBackgroundColour(wx.NullColour)
            self.states[btn.id]=False        
            new_state = pinproc.EventTypeSwitchOpenDebounced
            self.game.desktop.key_events.append({'type': new_state, 'value': switch_number})  # add these switch close events to the queue
        else:
            print("click ignored")

        btn.ClearBackground()

    ##############################################
    # GUI: Button Maker
    ##############################################
    def makeButton(self, frame, sname,switch_code, game_num):
        button = wx.Button(frame, label='%s\n%s' % (sname, switch_code))

        button.SetToolTipString(sname)

        button.id = switch_code
        button.game_num = game_num
        self.states[button.id] = False
        button.Bind(wx.EVT_LEFT_DOWN, self.onLeftButtonDOWN)
        button.Bind(wx.EVT_LEFT_UP, self.onLeftButtonUP)
        button.Bind(wx.EVT_RIGHT_DOWN, self.onRightButton)

        button.SetBackgroundColour(wx.NullColour)
        button.ClearBackground()

        return button

    
    # def mode_tick(self):
    #   for event in pygame.event.get((MOUSEBUTTONDOWN, MOUSEBUTTONUP)):
    #       if event.type == pygame.MOUSEBUTTONDOWN:
    #           mouse_loc = pygame.mouse.get_pos()
    #           col = mouse_loc[0]/18
    #           row = (mouse_loc[1]-128)/18
    #           print ("clicked row:" + str(row) + "; col: " + str(col))
    #           try:
    #               if(self.switchmatrix.has_key(str(col)+str(row))):
    #                   sw = self.switchmatrix[str(col)+str(row)]
    #                   print(" clicked: " + sw.yaml_number)

    #                   if(sw.state):
    #                       new_state = pinproc.EventTypeSwitchClosedDebounced
    #                   else:
    #                       new_state = pinproc.EventTypeSwitchOpenDebounced

    #                   self.game.desktop.key_events.append({'type': new_state, 'value': sw.number})  # add these switch close events to the queue
    #                   print ("state changed")
    #           finally:
    #               pass
        
    def mode_started(self):
        # nothing
        pass

    def _switch_changed_open(self, sw):
        #tempSurface = self.font.render(sw.name, True, self.fontDim)

        #self.screen.blit(tempSurface, (40*col,128+20*row))
        # self.screen.blit(self.lightDim, (18*sw.col,128+18*sw.row))
        return procgame.game.SwitchContinue     
    
    def _switch_changed_closed(self, sw):
        #tempSurface = self.font.render(sw.name, True, self.fontLit)
        # self.screen.blit(self.lightLit, (18*sw.col,128+18*sw.row))
        #self.screen.blit(tempSurface, (40*col,128+20*row))
        return procgame.game.SwitchContinue

