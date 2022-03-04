from pyfbsdk import FBSystem, FBPlayerControl
import copy

#Create new camera for every take in the scene
def copy_cameras(masterCam): 
    masterCam = masterCam
    FBPlayerControl().GotoStart()
    takeCount = FBSystem().CurrentTake.GetLayerCount()  
    for take in FBSystem().Scene.Takes:
      takeCount -= 1
      FBSystem().CurrentTake = FBSystem().Scene.Takes[takeCount]
      try:
          cameraDuplicate = copy.copy(masterCam)
      except:
          print ("No Master Camera Found. Make sure it is named RS_VCam_Target or contains 'master'")
          break
      cameraDuplicate.Name = take.Name
      
#Returns master camera
def find_master_cam():
    for camera in FBSystem().Scene.Cameras:
        if ("VCam_Target" in camera.LongName) or ("master" in camera.LongName.lower()) :
            masterCam = camera
            print (masterCam)
        else:
            print ("No Master Camera Found. Make sure it is named RS_VCam_Target or contains 'master'")
  
    copy_cameras(masterCam)

#entry
if __name__ == '__builtin__':
  find_master_cam()