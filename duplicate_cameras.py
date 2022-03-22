from pyfbsdk import FBSystem, FBPlayerControl, FBMessageBox
import copy

#Create new camera for all best takes in the scene
def copy_cameras(masterCam): 
    masterCam = masterCam
    FBPlayerControl().GotoStart()
    count, bestCount = 0, 0
    for take in FBSystem().Scene.Takes:
        FBSystem().CurrentTake = FBSystem().Scene.Takes[count]
        takeName = FBSystem().CurrentTake.Name
        if ("best" in takeName.lower()):
            try:
                cameraDuplicate = copy.copy(masterCam)
                bestCount += 1
            except:
                continue
            cameraDuplicate.Name = take.Name
        else:
            pass
        count += 1
            
    if (bestCount < 1):
        FBMessageBox( "Note", "No 'best' takes to duplicate camera", "OK" )
      
#Returns master camera
def find_master_cam():
    for camera in FBSystem().Scene.Cameras:
        if ("VCam_Target" in camera.LongName) or ("master" in camera.LongName.lower()):
            masterCam = camera
        else:
            continue
    try:
        copy_cameras(masterCam)
    except:
        print("No Master Camera Found. Make sure it is named MasterCam or contains 'master'")

#entry
if __name__ == '__builtin__':
  find_master_cam()
