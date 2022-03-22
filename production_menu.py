"""
Creates the custom Live Production menu in Motionbuilder 
that contains all the Live Production tools.

"""
from __future__ import print_function
import functools
from pyfbsdk import FBMenuManager

# constants
MENU_NAME = 'Live-Production'

# globals
function_map = dict()

def event_menu(control, event):
    global function_map
    function_map[event.Id]()

def _pre_record_prep():
    import liveproduction.new_take
    reload(liveproduction.new_take)
    liveproduction.new_take.connect_master_constraints()
    
def _create_new_take():
    import liveproduction.popup
    reload(liveproduction.popup)
    liveproduction.popup.create_tool()
    
def _devices_offline():
    import liveproduction.next_take
    reload(liveproduction.next_take)
    liveproduction.next_take.devices_offline()
    
def _plot_camera():
    import liveproduction.next_take
    reload(liveproduction.next_take)
    liveproduction.next_take.plot_camera()
    
def _plot_characters():
    import liveproduction.next_take
    reload(liveproduction.next_take)
    liveproduction.next_take.plot_characters()
    
def _post_record_prep():
    import liveproduction.next_take
    reload(liveproduction.next_take)
    liveproduction.next_take.disconnect_master_constraints()
    
def _duplicate_cameras():
    import liveproduction.duplicate_cameras
    reload(liveproduction.duplicate_cameras)
    liveproduction.duplicate_cameras.find_master_cam()


if __name__ == '__builtin__':
    # Look for the menu, otherwise make one
    if not FBMenuManager().GetMenu(MENU_NAME):
        FBMenuManager().InsertAfter(None, 'Help', MENU_NAME)
    menu = FBMenuManager().GetMenu(MENU_NAME)
    menu.OnMenuActivate.Add(event_menu)

    # Add items to the menu
    menu.InsertFirst('Turn Devices On + Connect Constraints', 1)
    menu.InsertLast('Create New Take', 2)
    menu.InsertLast('Devices Offline', 3)
    menu.InsertLast('Plot Camera', 4)
    menu.InsertLast('Plot Characters', 5)
    menu.InsertLast('Disconnect Constraints + Turn TP VCam Offline', 6)
    menu.InsertLast('Duplicate Cameras', 7)

    # Map menu items to functions
    function_map[1] = _pre_record_prep
    function_map[2] = _create_new_take
    function_map[3] = _devices_offline
    function_map[4] = _plot_camera
    function_map[5] = _plot_characters
    function_map[6] = _post_record_prep
    function_map[7] = _duplicate_cameras
