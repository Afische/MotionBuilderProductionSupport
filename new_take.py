from __future__ import print_function
from pyfbsdk import FBSystem, FBTake, FBPlayerControl, FBConstraintManager, FBConnect, FBFindModelByLabelName

#Incrementally rename take, create a new take using new name, copy take data if there is camera coverage
def name_new_take(liveTalent):
    FBPlayerControl().GotoStart()
    liveTalent = liveTalent
    currentTake = FBSystem().CurrentTake.Name
    takeChar = currentTake[-1]
        
    #If regular take
    if takeChar.isdigit():
        takeNumber = int(takeChar)
        takeNumber += 1
        takeChar = str(takeNumber)
        newName = currentTake[:-1]
        newName += takeChar
    #If _best take
    else:
        takeChar = currentTake[-6]
        takeNumber = int(takeChar)
        takeNumber += 1
        takeChar = str(takeNumber)
        newName = currentTake[:-6]
        newName += takeChar

    #If previs/ live talent, shooting new scene don't copy data
    if liveTalent == True:
        newTake = FBTake(newName)
        FBSystem().Scene.Takes.append(newTake)
    
    #If camera coverage, copy data
    else:
        newTake = FBSystem().CurrentTake.CopyTake(newName)
        #Change take for selected audio if camera coverage
        for component in FBSystem().Scene.Components:
            if (".wav") in component.LongName or (".mp3") in component.LongName:
                if component.Selected == True:
                    component.CurrentTake = FBSystem().CurrentTake
        

#Find all input or output nodes in a constraint box
def _find_animation_node(pParent, pName):

    l_result = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
            l_result = lNode
            break
    return l_result

#Turns on all devices
def devices_online():

    deviceList = FBSystem().Scene.Devices
    if deviceList:
        for device in deviceList:
            device.Live = True
            device.RecordMode = True
            device.Online = True
    else:
        print ('No device found')
        
#Connects constraint logic to camera
def connect_master_constraints():

    constraints = FBSystem().Scene.Constraints
    for constraint in constraints:
        if "Auto_RS_VCam_Target_Constraint_Logic" == constraint.Name:
            cameraConstraint = constraint
    try:
        cameraBoxes = cameraConstraint.Boxes
        for box in cameraBoxes:
            if "Multiply (a x b)" == box.Name:
                multiplyBox = box
            elif "Auto_RS_VCam_Target" == box.Name:
                receiverBox = box
            elif "Camera" == box.Name:
                senderBox = box
                
        multiplyNode = _find_animation_node(multiplyBox.AnimationNodeOutGet(), 'Result')
        receiverFOVNode = _find_animation_node(receiverBox.AnimationNodeInGet(), 'FieldOfView')
        senderRotationNode = _find_animation_node(senderBox.AnimationNodeOutGet(), 'Rotation')
        receiverRotationNode = _find_animation_node(receiverBox.AnimationNodeInGet(), 'Rotation')
        senderTranslationNode = _find_animation_node(senderBox.AnimationNodeOutGet(), 'Translation')
        receiverTranslationNode = _find_animation_node(receiverBox.AnimationNodeInGet(), 'Translation')
        FBConnect(multiplyNode, receiverFOVNode)
        FBConnect(senderRotationNode, receiverRotationNode)
        FBConnect(senderTranslationNode, receiverTranslationNode)
    
    except:
        print("Camera constraint Auto_RS_VCam_Target_Constraint_Logic not found")
    
    devices_online()
    print("Devices online")

#entry
if __name__ == '__builtin__':
    liveTalent = False
    name_new_take()
    connect_master_constraints()
