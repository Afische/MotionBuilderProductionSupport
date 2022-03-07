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
    print control.Caption, " take has been created!"
    CloseTool(tool)
    liveTalent = False
    name_new_take(liveTalent)

def populate_layout(mainLyt):
    x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(100,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("main","main", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("main",lyt)
    
    l = FBLabel()
    l.Caption = "If camera coverage, select audio tracks before clicking the button!"
    l.Justify = FBTextJustify.kFBTextJustifyCenter
    l.Style = FBTextStyle.kFBTextStyleBold
    l.WordWrap = True
    lyt.Add(l,150, space = 75)
    
    a = FBButton()
    a.Caption = "Live Talent"
    a.Justify = FBTextJustify.kFBTextJustifyRight
    lyt.Add(a,80, height=50)
    a.OnClick.Add(live_talent)
    
    b = FBButton()
    b.Caption = "Camera Coverage"
    b.Justify = FBTextJustify.kFBTextJustifyRight
    lyt.Add(b,100, height=50)
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
    tool.StartSizeX = 500
    tool.StartSizeY = 100
    populate_layout(tool)
    ShowTool(tool)

#entry
if __name__ == '__builtin__':
    create_tool()
