from pyfbsdk import *
from pyfbsdk_additions import *
from new_take import name_new_take

# Button creation
def live_talent(control, event):
    print control.Caption, " take has been created!"
    CloseTool(tool)
    liveTalent = True
    name_new_take(liveTalent)
    
def camera_coverage(control, event):
    #Change take for selected audio if camera coverage
    for component in FBSystem().Scene.Components:
        if (".wav") in component.LongName or (".mp3") in component.LongName:
            if component.Selected == True:
                print (component.LongName) 
    component.CurrentTake = FBSystem().CurrentTake
    print control.Caption, " take has been created!"
    CloseTool(tool)
    liveTalent = False
    name_new_take(liveTalent)

def populate_layout(mainLyt):
    x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("main","main", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("main",lyt)
    
    b = FBButton()
    b.Caption = "Live Talent"
    b.Justify = FBTextJustify.kFBTextJustifyRight
    lyt.Add(b,80)
    b.OnClick.Add(live_talent)
    
    b = FBButton()
    b.Caption = "Camera Coverage"
    b.Justify = FBTextJustify.kFBTextJustifyRight
    lyt.Add(b,100)
    b.OnClick.Add(camera_coverage)
    
    #b = FBButton()
    #b.Caption = "Check1"
    #b.Style = FBButtonStyle.kFBCheckbox 
    #b.Justify = FBTextJustify.kFBTextJustifyLeft
    #lyt.Add(b,60)
    #b.OnClick.Add(BtnCallback)
    
def create_tool():
    # Tool creation will serve as the hub for all other controls
    global liveTalent 
    liveTalent = False
    global tool
    tool = FBCreateUniqueTool("Create New Take")
    tool.StartSizeX = 300
    tool.StartSizeY = 100
    populate_layout(tool)
    ShowTool(tool)

#entry
if __name__ == '__builtin__':
    create_tool()
