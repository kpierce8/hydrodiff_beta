import sys, string, os, arcgisscripting, time, shutil, wx

try:
    del gp
except:
    pass

gp = arcgisscripting.create()
gp.OverwriteOutput = True
gp.SetProduct("ArcInfo")
gp.CheckOutExtension("spatial")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Conversion Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Analysis Tools.tbx")
   
#The TARGET is the linework being annotated and checked for coincidence with the
#COMPARE layer, for which buffers have been generated.


# #####################################################################################

##def getParams(bob):
##    target = bob.Target
##    targID = bob.Targid
##    id_match = bob.TargKey
##    length_field = bob.Targlength
##    bufferRoot = bob.Buffer
##    buffID = bob.Buffid
##    id_field = bob.BuffKey
##    testfile2 = open("c:/data/testdir/pythontest2.txt", mode = 'w+')
##    testfile2.write(id_match)
    
    
    
# Waterbody Layer
#wabody = "L:/gis_data_mgmt/hydroframework/HydroDiff/NHD_WB_AREA_W1_24.shp"
#wabodykey = "ComID"
#wa_match = "ComID"
# #####################################################################################
# #####################################################################################

# ######   RUN LIST  ########################################
#wrias = ['06'] # 06 and 14 are both small
# ###########################################################



import HD_subroutines_func2 as subs




def Main(bob):
    target = bob.Target
    targID = bob.Targid
    id_match = bob.TargKey
    length_field = bob.Targlength[0:10]
    bufferRoot = bob.Buffer
    buffID = bob.Buffid
    id_field = bob.BuffKey
    wrias = bob.WRIAs 
    radii = bob.RADII
    #wabody = "L:/gis_data_mgmt/hydroframework/HydroDiff/NHD_WB_AREA_W1_24.shp"
    wabody = bob.WaterBody
    wabodykey = bob.WaBodyID

    subsetT = bob.SubsetT
    subsetC = bob.SubsetC

    try:
        dowaterba = int(wabody)
    except:    
        dowaterba = 0
    
    #testfile3 = open("c:/data/testdir/pythontest3.txt", mode = 'w+')
    #testfile3.write(target + '\n' + str(wrias[0]) + ' , ' + str(wrias[1]) + ' str ' + str(wrias))
    #outpath = "C:/data/Hydrodiff" #script arg 4
    outpath = bob.RootFolder
    identities = outpath + "/identity/" + targID + "_"
    resulttarg = outpath + "/results/"+ targID + "vs" + buffID + "/" + targID + "_" #script arg 5
    buffsource = outpath + "/buffersource/" + bufferRoot

    print length_field
    
    try:
       os.makedirs(resulttarg)
    except OSError:
       print "Directory already exists"    

    for n in range(0,len(wrias)):
        wria = wrias[n] 
        
        buffpath = outpath + "/buffers/" + buffID + "_" + str(wria)  #script arg 3 to buffer destination
        subs.hydrodiff_setup(wria, target, buffpath, outpath, resulttarg, buffsource, radii, subsetT, subsetC)   
        subs.CheckBuffer(wria, resulttarg, buffpath, radii)
        subs.HydroPointSampling(wria, resulttarg, buffpath, identities, radii, outpath)
        subs.ClipEnd(wria, resulttarg, outpath, buffpath, id_match, identities, wabody, wabodykey, dowaterba)
        subs.EndCalc(wria, resulttarg, length_field)
        subs.IntersectIntegrate(wria, resulttarg, id_field, id_match, identities, wabodykey, radii, outpath, dowaterba)



