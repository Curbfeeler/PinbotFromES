#!/usr/bin/python
#
#    ________  ______   __                        __   ____  _____ ______   _________            __     
#   / ____/ / / /  _/  / /_  ____ _________  ____/ /  / __ \/ ___// ____/  / ____/ (_)__  ____  / /_    
#  / / __/ / / // /   / __ \/ __ `/ ___/ _ \/ __  /  / / / /\__ \/ /      / /   / / / _ \/ __ \/ __/    
# / /_/ / /_/ // /   / /_/ / /_/ (__  )  __/ /_/ /  / /_/ /___/ / /___   / /___/ / /  __/ / / / /_      
# \____/\____/___/  /_.___/\__,_/____/\___/\__,_/   \____//____/\____/   \____/_/_/\___/_/ /_/\__/      
                                                                                                      
#     ____              ____        ____                  ______                                                                                                                                                                                                                                      
#    / __/___  _____   / __ \__  __/ __ \_________  _____/ ____/___ _____ ___  ___                                                                                                                                                                                                                    
#   / /_/ __ \/ ___/  / /_/ / / / / /_/ / ___/ __ \/ ___/ / __/ __ `/ __ `__ \/ _ \                                                                                                                                                                                                                   
#  / __/ /_/ / /     / ____/ /_/ / ____/ /  / /_/ / /__/ /_/ / /_/ / / / / / /  __/                                                                                                                                                                                                                   
# /_/  \____/_/     /_/    \__, /_/   /_/   \____/\___/\____/\__,_/_/ /_/ /_/\___/                                                                                                                                                                                                                    
#                         /____/                                                                                                                                                                                                                                                                      
#
# - MOcean
#
# GUI stuff from :  http://zetcode.com/wxpython/layout/

import OSC
from optparse import OptionParser
import socket
import wx
import yaml

states = {}

server_ip = socket.gethostbyname(socket.gethostname())

parser = OptionParser()

parser.add_option("-a", "--address",
                  action="store", type="string", 
                  dest="server_ip", default=server_ip,
                  help="Address of server.  Default is %s." % server_ip)

parser.add_option("-p", "--port",
                  action="store", type="int", 
                  dest="server_port", default=9000,
                  help="Port on OSC server.  Default is 9000.")

parser.add_option("-y", "--yaml",
                  action="store", type="string", 
                  dest="yaml_file", default='game.yaml',
                  help="The yaml file name for the machine definition.  Default is 'game.yaml'.")

(options, args) = parser.parse_args()
options = vars(options)

osc_client = OSC.OSCClient()
osc_client.connect((server_ip, options['server_port']))

##############################################
# GUI Event Handlers
##############################################
                                                                                                                                                                                                                                                                                        
def onLeftButtonDOWN(event):
    sendOSC(event, True)
    print "LEFT Button  [%s] DOWN!" % event.EventObject.id

def onLeftButtonUP(event):
    sendOSC(event, False)
    print "LEFT Button [%s] UP!" % event.EventObject.id

def onRightButton(event):
    btn = event.EventObject
    sendOSC(event, not(states[btn.id]))
    print "RIGHT Button [%s] pressed!" % btn.id

def sendOSC(evt_src, new_state=None):
    btn = evt_src.EventObject
    addr = '/sw/%s' % btn.id
    # addr = '/sw/%s' % btn.GetLabel()
    osc_msg = OSC.OSCMessage(addr)
    if(states[btn.id]==False and new_state==True):
        btn.SetBackgroundColour(wx.GREEN)
        states[btn.id]=True
        osc_msg.append(1)
        print('%s %s' % (addr, 1) )
    elif(states[btn.id]==True and new_state==False):
        btn.SetBackgroundColour(wx.NullColour)
        states[btn.id]=False        
        osc_msg.append(0)
        print('%s %s' % (addr, 0) )
    else:
        print("click ignored")
    osc_client.send(osc_msg)
    btn.ClearBackground()

##############################################
# GUI: Button Maker
##############################################
def makeButton(frame, sname,switch_code):
    button = wx.Button(frame, label='%s\n%s' % (sname, switch_code))

    button.SetToolTipString(sname)

    button.id = switch_code
    states[button.id] = False
    button.Bind(wx.EVT_LEFT_DOWN, onLeftButtonDOWN)
    button.Bind(wx.EVT_LEFT_UP, onLeftButtonUP)
    button.Bind(wx.EVT_RIGHT_DOWN, onRightButton)

    button.SetBackgroundColour(wx.NullColour)
    button.ClearBackground()

    return button

##############################################
# main()
##############################################

def main():
    # make the GUI components
    app = wx.App(redirect=False)
    frame = wx.Frame(None, -1, 'Switch Matrix OSC Client')
    gs = wx.GridSizer(9, 8, 5, 5) # rows, cols, gap

    # hold all the switches so we can know which 
    # ones are outside the matrix
    game_switches = {}

    # load the yaml file to find all the switches
    yaml_data = yaml.load(open(options['yaml_file'], 'r'))
    if 'PRSwitches' in yaml_data:
      switches = yaml_data['PRSwitches']
      for name in switches:
        item_dict = switches[name]
        yaml_number = str(item_dict['number'])
          
        if 'label' in item_dict:
          swlabel = item_dict['label']
        if 'type' in item_dict:
          swtype = item_dict['type']
        game_switches[yaml_number] = name


    # go through the matrix trying to find switches from the yaml
    for r in range(0,8):
        for c in range(0,8):
            switch_code = 'S%s%s' % (c+1, r+1)
            try:
              sname = game_switches[switch_code]
              # remove the switch from the list
              del game_switches[switch_code]
            except Exception, e:
              print "Failed to find a definition for switch matrix location: %s" % e.message
              sname = "N/A"
            button = makeButton(frame, sname, switch_code)
            gs.Add(button, 0, wx.EXPAND)

    print "Adding remaining dedicated switches..."
    print game_switches

    # anything left in that dict wasn't in the matrix (i.e., a dedicated switch)
    for (switch_code,sname) in game_switches.iteritems():
      button = makeButton(frame, sname, switch_code)
      gs.Add(button, 0, wx.EXPAND)

    frame.SetSizer(gs)
    frame.Show()
    app.MainLoop()

    # END main()

if __name__ == '__main__':
    main()