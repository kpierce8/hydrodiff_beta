#Boa:Frame:Frame2

import wx, os
import MAIN_GUI2 as mainRun
import CheckSetup as check
#from elementtree.ElementTree import Element, SubElement, ElementTree, dump, parse
from xml.etree.ElementTree import Element, SubElement, ElementTree, dump, parse
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
    RootFolder = ""
    WaterBody = ""
    WaBodyID = ""
    SubsetT = ""
    SubsetC = ""

newRun = HydroRun
gWria = ""

def create(parent):
    return Frame2(parent)

[wxID_FRAME2, wxID_FRAME2BUTTON1, wxID_FRAME2BUTTON2, wxID_FRAME2BUTTON3, 
 wxID_FRAME2CBUFFER, wxID_FRAME2CBUFFID, wxID_FRAME2CBUFFKEY, 
 wxID_FRAME2COMBOBOX1, wxID_FRAME2CROOT, wxID_FRAME2CTARGET, 
 wxID_FRAME2CTARGID, wxID_FRAME2CTARGKEY, wxID_FRAME2CTARGLENGTH, 
 wxID_FRAME2CWABODYID, wxID_FRAME2CWATER, wxID_FRAME2DELBUTTON, 
 wxID_FRAME2PANEL1, wxID_FRAME2SAVERUN, wxID_FRAME2STATICBOX1, 
 wxID_FRAME2STATICTEXT1, wxID_FRAME2STATICTEXT10, wxID_FRAME2STATICTEXT11, 
 wxID_FRAME2STATICTEXT12, wxID_FRAME2STATICTEXT13, wxID_FRAME2STATICTEXT14, 
 wxID_FRAME2STATICTEXT15, wxID_FRAME2STATICTEXT16, wxID_FRAME2STATICTEXT2, 
 wxID_FRAME2STATICTEXT3, wxID_FRAME2STATICTEXT4, wxID_FRAME2STATICTEXT5, 
 wxID_FRAME2STATICTEXT6, wxID_FRAME2STATICTEXT7, wxID_FRAME2STATICTEXT8, 
 wxID_FRAME2STATICTEXT9, wxID_FRAME2SUBSETC, wxID_FRAME2SUBSETT, 
 wxID_FRAME2TEXTRADII, wxID_FRAME2TEXTWRIAS, 
] = [wx.NewId() for _init_ctrls in range(39)]

class Frame2(wx.Frame):
    
    #file = open("C:/data/testdir/xmltest.xml", "r")
    file = open(os.getcwd() + "\\xmltest.xml", "r")
    tree=parse(file)
    runCollection = []
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME2, name='', parent=prnt,
              pos=wx.Point(366, 254), size=wx.Size(696, 527),
              style=wx.DEFAULT_FRAME_STYLE, title='HydroDiff 0.9')
        self.SetClientSize(wx.Size(688, 499))

        self.panel1 = wx.Panel(id=wxID_FRAME2PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(688, 499),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetBackgroundColour(wx.Colour(66, 160, 255))
        self.panel1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.comboBox1 = wx.ComboBox(choices=[], id=wxID_FRAME2COMBOBOX1,
              name='comboBox1', parent=self.panel1, pos=wx.Point(8, 16),
              size=wx.Size(200, 21), style=0, value='Select a RUN')
        self.comboBox1.Bind(wx.EVT_COMBOBOX, self.OnComboBox1Combobox,
              id=wxID_FRAME2COMBOBOX1)

        self.button1 = wx.Button(id=wxID_FRAME2BUTTON1, label='GetParameters',
              name='button1', parent=self.panel1, pos=wx.Point(537, 114),
              size=wx.Size(95, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME2BUTTON1)

        self.cTargID = wx.TextCtrl(id=wxID_FRAME2CTARGID, name='cTargID',
              parent=self.panel1, pos=wx.Point(133, 104), size=wx.Size(208, 21),
              style=0, value='Target Identifier e.g. "str24"')

        self.button2 = wx.Button(id=wxID_FRAME2BUTTON2, label='Refresh',
              name='button2', parent=self.panel1, pos=wx.Point(224, 16),
              size=wx.Size(75, 23), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME2BUTTON2)

        self.cTargKey = wx.TextCtrl(id=wxID_FRAME2CTARGKEY, name='cTargKey',
              parent=self.panel1, pos=wx.Point(133, 136), size=wx.Size(208, 21),
              style=0, value='Target Key Field')

        self.cTargLength = wx.TextCtrl(id=wxID_FRAME2CTARGLENGTH,
              name='cTargLength', parent=self.panel1, pos=wx.Point(133, 168),
              size=wx.Size(208, 21), style=0, value='Target Length Field')

        self.cBuffer = wx.TextCtrl(id=wxID_FRAME2CBUFFER, name='cBuffer',
              parent=self.panel1, pos=wx.Point(133, 200), size=wx.Size(208, 21),
              style=0, value='Polyline comparison feature (Buffer)')

        self.cBuffID = wx.TextCtrl(id=wxID_FRAME2CBUFFID, name='cBuffID',
              parent=self.panel1, pos=wx.Point(133, 232), size=wx.Size(208, 21),
              style=0, value='Buffer Identifier e.g. "NHD"')

        self.cTarget = wx.TextCtrl(id=wxID_FRAME2CTARGET, name='cTarget',
              parent=self.panel1, pos=wx.Point(133, 72), size=wx.Size(499, 21),
              style=0, value='Polyline analysis feature')

        self.cBuffKey = wx.TextCtrl(id=wxID_FRAME2CBUFFKEY, name='cBuffKey',
              parent=self.panel1, pos=wx.Point(134, 264), size=wx.Size(208, 21),
              style=0, value='Buffer Key Field')

        self.SaveRun = wx.Button(id=wxID_FRAME2SAVERUN, label='SaveRun',
              name='SaveRun', parent=self.panel1, pos=wx.Point(320, 17),
              size=wx.Size(75, 23), style=0)
        self.SaveRun.Bind(wx.EVT_BUTTON, self.OnSaveRunButton,
              id=wxID_FRAME2SAVERUN)

        self.button3 = wx.Button(id=wxID_FRAME2BUTTON3, label='Run',
              name='button3', parent=self.panel1, pos=wx.Point(512, 16),
              size=wx.Size(128, 40), style=0)
        self.button3.Enable(False)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button,
              id=wxID_FRAME2BUTTON3)

        self.textWRIAs = wx.TextCtrl(id=wxID_FRAME2TEXTWRIAS, name='textWRIAs',
              parent=self.panel1, pos=wx.Point(192, 416), size=wx.Size(248, 21),
              style=0, value='all')

        self.staticText1 = wx.StaticText(id=wxID_FRAME2STATICTEXT1,
              label='TargID', name='staticText1', parent=self.panel1,
              pos=wx.Point(40, 109), size=wx.Size(39, 13), style=0)
        self.staticText1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText2 = wx.StaticText(id=wxID_FRAME2STATICTEXT2,
              label='TargKey', name='staticText2', parent=self.panel1,
              pos=wx.Point(40, 140), size=wx.Size(47, 13), style=0)
        self.staticText2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText3 = wx.StaticText(id=wxID_FRAME2STATICTEXT3,
              label='Buffer', name='staticText3', parent=self.panel1,
              pos=wx.Point(40, 202), size=wx.Size(34, 13), style=0)
        self.staticText3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText4 = wx.StaticText(id=wxID_FRAME2STATICTEXT4,
              label='TargLength', name='staticText4', parent=self.panel1,
              pos=wx.Point(40, 171), size=wx.Size(65, 13), style=0)
        self.staticText4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText5 = wx.StaticText(id=wxID_FRAME2STATICTEXT5,
              label='BuffKey', name='staticText5', parent=self.panel1,
              pos=wx.Point(40, 264), size=wx.Size(43, 13), style=0)
        self.staticText5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText6 = wx.StaticText(id=wxID_FRAME2STATICTEXT6,
              label='BuffID', name='staticText6', parent=self.panel1,
              pos=wx.Point(40, 233), size=wx.Size(35, 13), style=0)
        self.staticText6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText8 = wx.StaticText(id=wxID_FRAME2STATICTEXT8,
              label='Target', name='staticText8', parent=self.panel1,
              pos=wx.Point(41, 80), size=wx.Size(38, 13), style=0)
        self.staticText8.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText7 = wx.StaticText(id=wxID_FRAME2STATICTEXT7,
              label='Subsets (e.g.WRIA, County)', name='staticText7',
              parent=self.panel1, pos=wx.Point(4, 421), size=wx.Size(172, 13),
              style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME2STATICBOX1, label='',
              name='staticBox1', parent=self.panel1, pos=wx.Point(16, 64),
              size=wx.Size(104, 320), style=1)
        self.staticBox1.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.staticBox1.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.staticBox1.SetForegroundColour(wx.Colour(192, 192, 192))

        self.DelButton = wx.Button(id=wxID_FRAME2DELBUTTON, label='DeleteRun',
              name='DelButton', parent=self.panel1, pos=wx.Point(416, 17),
              size=wx.Size(75, 23), style=0)
        self.DelButton.Bind(wx.EVT_BUTTON, self.OnDelButtonButton,
              id=wxID_FRAME2DELBUTTON)

        self.textRadii = wx.TextCtrl(id=wxID_FRAME2TEXTRADII, name='textRadii',
              parent=self.panel1, pos=wx.Point(572, 416), size=wx.Size(100, 21),
              style=0, value='1,10,40')

        self.staticText9 = wx.StaticText(id=wxID_FRAME2STATICTEXT9,
              label='Buffer Distances', name='staticText9', parent=self.panel1,
              pos=wx.Point(485, 421), size=wx.Size(79, 13), style=0)

        self.staticText10 = wx.StaticText(id=wxID_FRAME2STATICTEXT10,
              label='Press Get Parameters to Update', name='staticText10',
              parent=self.panel1, pos=wx.Point(440, 176), size=wx.Size(232, 13),
              style=0)

        self.staticText11 = wx.StaticText(id=wxID_FRAME2STATICTEXT11,
              label='Press Get Parameters to Update', name='staticText11',
              parent=self.panel1, pos=wx.Point(440, 208), size=wx.Size(232, 13),
              style=0)

        self.cRoot = wx.TextCtrl(id=wxID_FRAME2CROOT, name='cRoot',
              parent=self.panel1, pos=wx.Point(136, 296), size=wx.Size(504, 21),
              style=0, value='Enter root folder path')
        self.cRoot.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText12 = wx.StaticText(id=wxID_FRAME2STATICTEXT12,
              label='Root folder', name='staticText12', parent=self.panel1,
              pos=wx.Point(40, 296), size=wx.Size(63, 13), style=0)

        self.staticText13 = wx.StaticText(id=wxID_FRAME2STATICTEXT13,
              label='Water Bodies', name='staticText13', parent=self.panel1,
              pos=wx.Point(40, 328), size=wx.Size(76, 13), style=0)

        self.cWater = wx.TextCtrl(id=wxID_FRAME2CWATER, name='cWater',
              parent=self.panel1, pos=wx.Point(135, 328), size=wx.Size(505, 21),
              style=0, value='Enter water bodies path')
        self.cWater.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText14 = wx.StaticText(id=wxID_FRAME2STATICTEXT14,
              label='WaBody Key', name='staticText14', parent=self.panel1,
              pos=wx.Point(40, 356), size=wx.Size(71, 13), style=0)

        self.cWabodyid = wx.TextCtrl(id=wxID_FRAME2CWABODYID, name='cWabodyid',
              parent=self.panel1, pos=wx.Point(137, 355), size=wx.Size(207, 21),
              style=0, value='Enter Water body key field')

        self.cSubsetT = wx.TextCtrl(id=wxID_FRAME2SUBSETT, name='cSubsetT',
              parent=self.panel1, pos=wx.Point(192, 448), size=wx.Size(100, 21),
              style=0, value='textCtrl1')

        self.staticText15 = wx.StaticText(id=wxID_FRAME2STATICTEXT15,
              label='Target Subset field', name='staticText15',
              parent=self.panel1, pos=wx.Point(78, 452), size=wx.Size(107, 13),
              style=0)

        self.staticText16 = wx.StaticText(id=wxID_FRAME2STATICTEXT16,
              label='Buffer Subset Field', name='staticText16',
              parent=self.panel1, pos=wx.Point(305, 452), size=wx.Size(105, 13),
              style=0)

        self.cSubsetC = wx.TextCtrl(id=wxID_FRAME2SUBSETC, name='cSubsetC',
              parent=self.panel1, pos=wx.Point(424, 448), size=wx.Size(100, 21),
              style=0, value='textCtrl1')

    def __init__(self, parent):
        self._init_ctrls(parent)
        file = open(os.getcwd() + "\\xmltest.xml", "r")
        tree=parse(file)
        root = tree.getroot()
        bob = tree.getiterator("hrun")
        for i in bob:
            self.comboBox1.Append(i.attrib["runName"])
            self.runCollection.append(i.attrib["runName"])



    def OnComboBox1Combobox(self, event):
       root = self.tree.getroot()
       bob = self.tree.getiterator("hrun")
       for i in bob:
           if i.attrib["runName"] ==  self.comboBox1.Value:
               self.cBuffer.Value = str(i.findtext("buffer"))
               self.cBuffID.Value = str(i.findtext("buffid"))
               self.cTarget.Value = str(i.findtext("target"))
               self.cBuffKey.Value = str(i.findtext("buffkey"))
               self.cTargID.Value = str(i.findtext("targid"))
               self.cTargKey.Value = str(i.findtext("targkey"))
               self.cTargLength.Value = str(i.findtext("targlength"))
               self.cRoot.Value = str(i.findtext("rootfolder"))
               self.cWater.Value = str(i.findtext("waterbody"))
               self.cWabodyid.Value = str(i.findtext("wabodyid"))
               self.cSubsetT.Value = str(i.findtext("subsett"))
               self.cSubsetC.Value = str(i.findtext("subsetc"))
## XXX fix nulls when combobox changes!!

    def OnButton1Button(self, event):          
        newRun.RunID = self.comboBox1.GetValue()
        newRun.Target = self.cTarget.GetValue()
        newRun.Buffer = self.cBuffer.GetValue()
        newRun.TargKey = self.cTargKey.GetValue()
        newRun.BuffKey = self.cBuffKey.GetValue()
        newRun.Targid = self.cTargID.GetValue()
        newRun.Buffid = self.cBuffID.GetValue()
        newRun.Targlength = self.cTargLength.GetValue()
        newRun.RootFolder = self.cRoot.GetValue()
        newRun.WaterBody = self.cWater.GetValue()
        newRun.WaBodyID = self.cWabodyid.GetValue()
        newRun.SubsetT = self.cSubsetT.GetValue()
        newRun.SubsetC = self.cSubsetC.GetValue()      
        gWria = self.textWRIAs.GetValue()
        newRun.WRIAs = gWria.split(',')
        gRADII = self.textRadii.GetValue()
        newRun.RADII = gRADII.split(',')
        self.staticText10.Label = str(newRun.Target)
        self.staticText11.Label = newRun.Targid
        qrun = check.checkBuffers(newRun)
        print "checkBuffers: " + str(qrun)
        qrun2 = check.checkResults(newRun)
        print "checkResults: " + str(qrun2)
        qrun3 = check.checkFields(newRun)
        print "checkFields: " + str(qrun3)
        qrun4 = qrun + qrun2 + qrun3
        if qrun4 == int(3):
            self.button3.Enable(True)


        
    def OnButton2Button(self, event):
       self.comboRefresh()
       
    def comboRefresh(self):   
       root = self.tree.getroot()
       self.comboBox1.Clear()
       bob = root.getiterator("hrun")
       for i in bob:
           self.comboBox1.Append(i.attrib["runName"]) 
       
    def sendXML(self):
        root = self.tree.getroot()
        if self.comboBox1.Value in self.runCollection:
            bob = self.tree.getiterator("hrun")
            for i in bob:
                 if i.attrib["runName"] ==  self.comboBox1.Value:
                    i.find("target").text = self.cTarget.Value 
                    i.find("targid").text = self.cTargID.Value
                    i.find("targkey").text = self.cTargKey.Value
                    i.find("targlength").text = self.cTargLength.Value
                    i.find("buffid").text = self.cBuffID.Value
                    i.find("buffer").text = self.cBuffer.Value
                    i.find("buffkey").text =  self.cBuffKey.Value 
                    i.find("rootfolder").text = self.cRoot.Value 
                    i.find("waterbody").text = self.cWater.Value
                    i.find("wabodyid").text = self.cWabodyid.Value
                    i.find("subsett").text = self.cSubsetT.Value
                    i.find("subsetc").text = self.cSubsetC.Value
        else:
            hrun = SubElement(root, "hrun")
            hrun.attrib["runName"] = self.comboBox1.Value
            SubElement(hrun, "target").text = self.cTarget.Value 
            SubElement(hrun, "targid").text = self.cTargID.Value
            SubElement(hrun, "targkey").text = self.cTargKey.Value
            SubElement(hrun, "targlength").text = self.cTargLength.Value
            SubElement(hrun, "buffid").text = self.cBuffID.Value
            SubElement(hrun, "buffer").text = self.cBuffer.Value
            SubElement(hrun, "buffkey").text =  self.cBuffKey.Value  
            SubElement(hrun, "rootfolder").text = self.cRoot.Value
            SubElement(hrun, "waterbody").text = self.cWater.Value
            SubElement(hrun, "wabodyid").text = self.cWabodyid.Value
            SubElement(hrun, "subsett").text = self.cSubsetT.Value
            SubElement(hrun, "subsetc").text = self.cSubsetC.Value
        ElementTree(root).write(file=os.getcwd() + "\\xmltest.xml") 
        self.comboRefresh()  

    def OnSaveRunButton(self, event):
        self.sendXML()

    def OnButton3Button(self, event):
        mainRun.Main(newRun)

    def OnDelButtonButton(self, event):
        root = self.tree.getroot()
        bob = self.tree.getiterator("hrun")
        for i in bob:
           if i.attrib["runName"] ==  self.comboBox1.Value:
               root.remove(i)
               ElementTree(root).write(file=os.getcwd() + "\\xmltest.xml")
               self.comboRefresh()
               
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
