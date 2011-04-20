import sys, string, os, arcgisscripting, time, wx, re
gp = arcgisscripting.create()
gp.SetProduct("ArcInfo")
gp.CheckOutExtension("spatial")
gp.OverwriteOutput = True
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Conversion Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Analysis Tools.tbx")

allTest = re.compile(r'^all$', re.IGNORECASE)


def checkBuffers(newrun):
    wria = newrun.WRIAs[0]
    radii = newrun.RADII
    btempDICT = {}
    myFiles = os.listdir(newrun.RootFolder + "/buffersource/")
    for i in radii:                  
        btempDICT[i] = newrun.Buffer + str(i) + ".shp"
        if str(btempDICT[i]) not in myFiles:
            wx.MessageBox(str(btempDICT[i]) + " does not exist")
            return 0
        else:
            return 1
def checkResults(newrun):
    myFiles = os.listdir(newrun.RootFolder + "/results/")
    if str(newrun.Targid + "vs" + newrun.Buffid) not in myFiles:
        try:
            os.mkdir(str(newrun.RootFolder + "/results/" + newrun.Targid + "vs" + newrun.Buffid))
        except:
            print "folder exists, irrelevant capitalization difference"
            return 1
    else:
            return 1      

def checkFields(newrun):
    myFields= []
    target = newrun.Target
    getFields = gp.listfields(target)
    fields = getFields.next()
    try:
        while fields:
            myFields.append(fields.Name)
            fields = getFields.next()
    except:
        print "no more fields"        
    print myFields
    print newrun.TargKey
    if newrun.TargKey not in myFields:
        wx.MessageBox(str(newrun.TargKey) + " not in table")
    if newrun.Targlength not in myFields: 
        r1 = re.compile(r'.*shap.*|.*len.*', re.I)
        lenFields = []
        for a in myFields:
            if r1.search(a): lenFields.append(r1.search(a).group(0))
        print lenFields
        wx.MessageBox("Change length field to one of " + str(lenFields))
        return 0
    else:
        return 1

            



if __name__ == "__main__":

    app = wx.PySimpleApp()
    class HydroRun(object):
        RunID = ""
        Target = ""
        Buffer = ""
        TargKey = "" 
        BuffKey = ""
        Targid = ""
        Buffid = ""
        Targlength = ""
        WRIAs = []
        RADII = []
    newrun = HydroRun
    newrun.Target = "C:/data/hydrocompare/str24.shp"
    newrun.Buffer = "NHD_1711"
    newrun.Buffid = "NHD"
    newrun.Targid = "str24uu"
    newrun.WRIAs = ["02"]
    newrun.TargKey = 'LLIDkk'
    newrun.Targlength = 'Length'
    wria = newrun.WRIAs[0]
    outpath = "C:/data/Hydrodiff" 
    buffpath = "C:/data/hydrodiff/buffers/" + newrun.Buffid + "_" + str(wria)
    buffsource = "C:/data/hydrodiff/buffersource/" + newrun.Buffer
    resulttarg = outpath + "/results/"+ newrun.Targid + "vs" + newrun.Buffid + "/" + newrun.Targid + "_" #script arg 5
    newrun.RADII = [1,10,50]
    checkBuffers(newrun)
    checkResults(newrun)
    checkFields(newrun)
    del app
