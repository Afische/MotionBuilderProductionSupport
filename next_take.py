from __future__ import print_function
from pyfbsdk import FBSystem, FBPlayerControl, FBPlotOptions, FBConnect, FBCharacterPlotWhere

#Turn Vicon Stream Device offline and live, TP Vcam online and off live
def devices_offline():

    deviceList = FBSystem().Scene.Devices
    if deviceList:
        for device in deviceList:
            if device.Name == "Vicon Stream Device":
                device.Online = False
                device.Live = True
                device.RecordMode = True 
            elif device.Name == "TP Vcam":
                device.Online = True
                device.Live = False
                device.RecordMode = True
            else:
                continue
    else:
        print ('No device found')
        
def TPVCam_offline():

    deviceList = FBSystem().Scene.Devices
    if deviceList:
        for device in deviceList:
            if device.Name == "TP Vcam":
                device.Live = True
                device.RecordMode = True
                device.Online = False
    else:
        print ('No device found')

def plot_camera():

    constraints = FBSystem().Scene.Constraints
    for constraint in constraints:
        if "Auto_RS_VCam_Target_Constraint_Logic" == constraint.Name:
            constraint.Selected = True
            
    for camera in FBSystem().Scene.Cameras:
        if ("VCam_Target" in camera.LongName) or ("master" in camera.LongName.lower()) :
            camera.Selected = True
    
    FBSystem().CurrentTake.PlotTakeOnSelected(FBPlotOptions())

def plot_characters():

    characters = FBSystem().Scene.Characters
    for character in characters:
        character.PlotAnimation (FBCharacterPlotWhere.kFBCharacterPlotOnSkeleton,FBPlotOptions())
    
#Find all input or output nodes in a constraint box
def _find_animation_node(pParent, pName):

    l_result = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
            l_result = lNode
            break
    return l_result

#Connects constraint logic to camera
def disconnect_master_constraints():

    constraints = FBSystem().Scene.Constraints
    for constraint in constraints:
        if "Auto_RS_VCam_Target_Constraint_Logic" == constraint.Name:
            cameraConstraint = constraint

    cameraBoxes = cameraConstraint.Boxes
    for box in cameraBoxes:
        if "Auto_RS_VCam_Target" == box.Name:
            receiverBox = box
        
    receiverFOVNode = _find_animation_node(receiverBox.AnimationNodeInGet(), 'FieldOfView')
    receiverRotationNode = _find_animation_node(receiverBox.AnimationNodeInGet(), 'Rotation')
    receiverTranslationNode = _find_animation_node(receiverBox.AnimationNodeInGet(), 'Translation')
    receiverFOVNode.DisconnectAllSrc()
    receiverRotationNode.DisconnectAllSrc()
    receiverTranslationNode.DisconnectAllSrc()
    
    TPVCam_offline()


#entry
if __name__ == '__builtin__':
    liveTalent = True
    FBPlayerControl().GotoStart()
    TPVCam_offline()
    plot_camera()
    disconnect_master_constraints()