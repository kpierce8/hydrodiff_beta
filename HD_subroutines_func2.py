import sys, string, os, arcgisscripting, time, wx, re

gp = arcgisscripting.create()
gp.SetProduct("ArcInfo")
gp.CheckOutExtension("spatial")
gp.OverwriteOutput = True
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Conversion Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Analysis Tools.tbx")


def hydrodiff_setup(wria, target, buffpath, outpath, resulttarg, buffsource, radii, subsetT, subsetC):
    progMax = 100
    prog = wx.ProgressDialog("WRIA %s elapsed time" % wria, "Hydrodiff_Setup: Step 1 of 6",
                             maximum = progMax, style = wx.PD_ELAPSED_TIME | wx.PD_AUTO_HIDE)
    count = 0

    # Links to source data
    WChydro_shp = target
      # Output locations
    wcwria_shp = resulttarg + wria + ".shp"
 
    bsourceDICT = {}
    outputDICT = {}
    layerDICT = {}
    allTest = re.compile(r'^all$', re.IGNORECASE)
    for i in radii:
        bsourceDICT[i] = buffsource + str(i) + ".shp"
        print str(bsourceDICT[i])
        outputDICT[i] = buffpath + wria + "buf" + str(i) + ".shp"
        print outputDICT[i]
        layerDICT[i] = "str24_buf" + str(i) + "_Layer"
        print str(layerDICT[i])
        gp.MakeFeatureLayer_management(str(bsourceDICT[i]), str(layerDICT[i]))
        if re.match(allTest, wria) is None: gp.SelectLayerByAttribute_management(layerDICT[i], "NEW_SELECTION", ' "%s" =  %i' % (subsetC, string.atoi(wria)))
        gp.CopyFeatures_management(layerDICT[i], outputDICT[i], "", "0", "0", "0")
        count  += 20
        prog.Update(count)
        
    # MAKE copy to process
    gp.MakeFeatureLayer_management(WChydro_shp, 'wchydro_Layer')
    if re.match(allTest, wria) is None: gp.SelectLayerByAttribute_management('wchydro_Layer', "NEW_SELECTION", ' "%s" =  %d' % (subsetT, string.atoi(wria)))
    gp.CopyFeatures_management('wchydro_Layer', wcwria_shp)
    prog.Update(95)

    # ADD Fields
    # Process: Add Field COWBUF...
    gp.AddField_management(wcwria_shp, "COWBUF", "SHORT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field COWSEG...
    gp.AddField_management(wcwria_shp, "COWSEG", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
    ##
    # Process: Add Field MID_IN...
    gp.AddField_management(wcwria_shp, "MID_IN", "SHORT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
    prog.Update(100)
    prog.Destroy()


def CheckBuffer(wria, resulttarg, buffpath, radii):
    
    targ_temp1 = resulttarg + wria + ".shp"
    
    #Iteration Logic
    SSize = 2000
    Long = 0

    nrecords = gp.getcount(targ_temp1)
    progMax = nrecords
    prog = wx.ProgressDialog("WRIA %s " % wria,"Check Buffer: Step 2 of 6",
                            maximum = progMax, style = wx.PD_ELAPSED_TIME | wx.PD_AUTO_HIDE)
    count = 0
    
    import time
    print time.ctime()
    if SSize > nrecords:
        prog.Update(.5*nrecords)
    else:
        prog.Update(.5*SSize)

    btempDICT = {}
    
    for i in radii: 
        n = 0
        btempDICT[i] = buffpath + wria + "buf" + str(i) + ".shp"
        while n*SSize < nrecords:
           
            bob = time.time()
            SQLExp = ' "FID" >= ((%d + %d)  * %d) AND "FID" < ((%d + 1 + %d) * %d)' % (n, Long, SSize, n, Long, SSize)     
            gp.MakeFeatureLayer_management(targ_temp1, 'targ_lay', SQLExp)
            gp.MakeFeatureLayer_management(str(btempDICT[i]), 'buf_lay%s' % str(i))
           
            if i < 2:
                gp.CalculateField_management('targ_lay', 'COWBUF', 'x', 'PYTHON', 'x = 0') 
                gp.SelectLayerByAttribute_management('targ_lay', 'NEW_SELECTION', ' "COWBUF" = 0 ')                          
                gp.SelectLayerByLocation_management('targ_lay', 'COMPLETELY_WITHIN', 'buf_lay%s' % str(i))
                gp.CalculateField_management('targ_lay', 'COWBUF', 'x', 'PYTHON', 'x = %s' % str(i))
               
            else:
             
                gp.SelectLayerByAttribute_management('targ_lay', 'NEW_SELECTION', ' "COWBUF" = 0 ') 
                gp.SelectLayerByLocation_management('targ_lay', 'COMPLETELY_WITHIN', 'buf_lay%s' % str(i), '0', 'SUBSET_SELECTION')
                gp.CalculateField_management('targ_lay', 'COWBUF', 'x', 'PYTHON', 'x = %s' % str(i))
         
            n +=1

    prog.Update(nrecords)    
    prog.Destroy()    



def HydroPointSampling(wria, temptarg, buffpath, identities, radii, outpath):
  
    # Local variables...
    buf1_shp = buffpath + wria + "buf1.shp"
    wchydro_shp = temptarg + wria + ".shp"
    progMax = 4
    prog = wx.ProgressDialog("WRIA %s " % wria,"HydroPointSampling: Step 3 of 6",
                             maximum = progMax, style = wx.PD_ELAPSED_TIME | wx.PD_AUTO_HIDE)
    count = 0

    # 1 Process: Make XY Event Layer from MIDPOINTS
    gp.MakeXYEventLayer_management(wchydro_shp, "Xmid", "Ymid", 'point_Layer')

    # 2 Process: Make Layer of Midpoints with 0 buffer designation
    gp.MakeFeatureLayer_management('point_Layer', 'zero_Layer', '"COWBUF" = 0', "")
    # 3 Process make working layer for all TARGET
    gp.MakeFeatureLayer_management('point_Layer', 'all_Layer', "", "")
    # 4 Process: Select ZEROs that fall in 1-ft boundary
    gp.SelectLayerByLocation_management('zero_Layer', "COMPLETELY_WITHIN", buf1_shp, "", "NEW_SELECTION")
    # Copy selected Zero-layer features and allLayer to temporary shapefiles
    gp.CopyFeatures_management('zero_Layer',outpath + '/output/zeroLayer.shp')
    gp.CopyFeatures_management('all_Layer',outpath + '/output/allLayer.shp')

    # 5 Process: Update MID_IN layer to 1001 and select 1-ft predicate passes and also update to MID_IN = 1001
    gp.CalculateField_management('zero_Layer', "MID_IN", "1001", "VB", "")
    gp.SelectLayerByAttribute_management('all_Layer', "NEW_SELECTION", ' "COWBUF" = 1')
    gp.CalculateField_management('all_Layer', "MID_IN", "1001", "VB", "")

    # 6 Process: Select Remaining non-designated TARGET features
    gp.SelectLayerByAttribute_management('zero_Layer', "NEW_SELECTION", ' "COWBUF" = 0 ')

    # 7 Process: Tag remaining features with COWBUF = 9999 to denote problem features.
    gp.CalculateField_management('zero_Layer', "COWBUF", "9999", "VB", "")

    # 8 Process: Select Layer By Attribute (2)...
    gp.SelectLayerByAttribute_management('zero_Layer', "CLEAR_SELECTION", "")
    prog.Update(1)
    #######################################################################
    #Create Identity_analysis files for crosswalks

    bsourceDICT = {}
    identityDICT = {}

    for i in radii:
        bsourceDICT[i] = buffpath + wria + "buf" + str(i) + ".shp"
        print str(bsourceDICT[i])
        identityDICT[i] = identities + wria + "_Identity" +  str(i) + ".shp"
        print identityDICT[i]
        if i < 2:           
            gp.SelectLayerByAttribute_management('point_Layer', "NEW_SELECTION", '"MID_IN" = 1001')
            gp.MakeFeatureLayer_management('point_Layer', 'Output_Layer', "", "")
            gp.Identity_analysis('Output_Layer', bsourceDICT[i], identityDICT[i], "ALL", "", "NO_RELATIONSHIPS")
            prog.Update(2)
        else:
            gp.SelectLayerByAttribute_management('point_Layer', "NEW_SELECTION", '"COWBUF" = %s' % str(i))
            gp.MakeFeatureLayer_management('point_Layer', 'Output_Layer', "", "")
            gp.Identity_analysis('Output_Layer', str(bsourceDICT[i]), str(identityDICT[i]), "ALL", "", "NO_RELATIONSHIPS")
            prog.Update(3)        
   
    prog.Update(4)
    prog.Destroy()
	

def ClipEnd(wria, temptarg, outpath, buffpath, KeyField, identities, wabody, wabodykey, dowaterba):
     
    progMax = 5
    prog = wx.ProgressDialog("WRIA %s " % wria,"Clip End: Step 4 of 6",
                             maximum = progMax, style = wx.PD_ELAPSED_TIME | wx.PD_AUTO_HIDE)
    count = 0
    
    targ_temp1 = temptarg + wria + ".shp"
    targ_intersect = temptarg + wria + "WA_INTER.shp"


    ############################################
    ##Do BUFFER 40 Clip
    buf_temp40 =  buffpath + wria + "buf40.shp"
    clip_temp40 =  outpath + "/buffers/cliptemp40_" + wria + ".shp"

    gp.MakeFeatureLayer_management(targ_temp1, 'targ_Layer' )
    gp.Clip_analysis('targ_Layer',buf_temp40,clip_temp40)
    gp.MakeFeatureLayer_management(clip_temp40, 'clip_Layer40')

    try:
        gp.addfield_management(clip_temp40,"Clip40L","float")   
    except:
        gp.DeleteField_management(clip_temp40,"Clip40L")
        gp.addfield_management(clip_temp40,"Clip40L","float") 

    rows = gp.UpdateCursor(clip_temp40)
    row = rows.Next()

    prog.Update(1)
    # The Length of the clipped piece needs to be added to a field on the clipped feature
    while row:    # Create the geometry object
        newval = row.shape
        row.setvalue("Clip40L", newval.Length)
        rows.UpdateRow(row)
        row = rows.Next()

    del row, rows

    #Loop through sorted datasets and lookup matching data
    # Add clip length field to TARGET
    try:
        gp.addfield_management(targ_temp1,"Clip40L","float")   
    except:
        gp.DeleteField_management(targ_temp1,"Clip40L")
        gp.addfield_management(targ_temp1,"Clip40L","float") 

    x = 1
    hydcur = gp.updatecursor('targ_Layer',"","","",'%s' % (KeyField))
    intercur = gp.searchcursor('clip_Layer40',"","","",'%s' % (KeyField))
    f_row = intercur.next()
    while f_row:
        x += 1    
        search_val = f_row.GetValue('%s' % (KeyField))    
        i_row = hydcur.next()  
        while i_row:
            checkval = f_row.GetValue('%s' % (KeyField))
            if search_val == i_row.GetValue('%s' % (KeyField)):
                nowval = f_row.GetValue('%s' % (KeyField))
                newval = f_row.getvalue('Clip40L')
                i_row.SetValue('Clip40L', newval)
                hydcur.updaterow(i_row)
                break
            else:        
                i_row = hydcur.next()
        #cur = gp.searchcursor('clip_Layer',"","","",'OBJECTID')
        f_row = intercur.next()
      

            
    del f_row, hydcur, intercur
    prog.Update(2)
	############################################
    ## Do buffer1 CLIP
    targ_temp1 = temptarg + wria + ".shp"
    buf_temp1 =  buffpath + wria + "buf1.shp"
    clip_temp1 =  outpath + "/buffers/cliptemp1_" + wria + ".shp"

    gp.MakeFeatureLayer_management(targ_temp1, 'targ_Layer' )
    gp.Clip_analysis('targ_Layer',buf_temp1,clip_temp1)
    gp.MakeFeatureLayer_management(clip_temp1, 'clip_Layer1')

    try:
        gp.addfield_management(clip_temp1,"Clip1L","float")   
    except:
        gp.DeleteField_management(clip_temp1,"Clip1L")
        gp.addfield_management(clip_temp1,"Clip1L","float") 

    rows = gp.UpdateCursor(clip_temp1)
    row = rows.Next()

    while row:    # Create the geometry object
        newval = row.shape
        row.setvalue("Clip1L", newval.Length)
        rows.UpdateRow(row)
        row = rows.Next()

    del row, rows

    #Loop through sorted datasets and lookup matching data

    try:
        gp.addfield_management(targ_temp1,"Clip1L","float")   
    except:
        gp.DeleteField_management(targ_temp1,"Clip1L")
        gp.addfield_management(targ_temp1,"Clip1L","float") 

    x = 1
    hydcur = gp.updatecursor('targ_Layer',"","","",'%s' % (KeyField))
    intercur = gp.searchcursor('clip_Layer1',"","","",'%s' % (KeyField))
    f_row = intercur.next()
    while f_row:
        x += 1    
        search_val = f_row.GetValue('%s' % (KeyField))    
        i_row = hydcur.next()  
        while i_row:
            checkval = f_row.GetValue('%s' % (KeyField))
            if search_val == i_row.GetValue('%s' % (KeyField)):
                nowval = f_row.GetValue('%s' % (KeyField))
                newval = f_row.getvalue('Clip1L')
                i_row.SetValue('Clip1L', newval)
                hydcur.updaterow(i_row)
                break
            else:        
                i_row = hydcur.next()
        #cur = gp.searchcursor('clip_Layer',"","","",'OBJECTID')
        f_row = intercur.next()
      

            
    del f_row, hydcur, intercur
    prog.Update(3)
    ############################################
    ## Do WABODY CLIP
    if dowaterba == 0:
        targ_temp1 = temptarg + wria + ".shp"
        buf_temp1 =  wabody
        clip_temp1 =  outpath + "/buffers/cliptempWAT_" + wria + ".shp"

        gp.MakeFeatureLayer_management(targ_temp1, 'targ_Layer' )
        gp.Clip_analysis('targ_Layer',buf_temp1,clip_temp1)
        gp.MakeFeatureLayer_management(clip_temp1, 'clip_LayerWA')

        try:
            gp.addfield_management(clip_temp1,"Clip1WA","float")   
        except:
            gp.DeleteField_management(clip_temp1,"Clip1WA")
            gp.addfield_management(clip_temp1,"Clip1WA","float") 

        rows = gp.UpdateCursor(clip_temp1)
        row = rows.Next()

        while row:    # Create the geometry object
            newval = row.shape
            row.setvalue("Clip1WA", newval.Length)
            rows.UpdateRow(row)
            row = rows.Next()

        del row, rows

        #Loop through sorted datasets and lookup matching data

        try:
            gp.addfield_management(targ_temp1,"Clip1WA","float")   
        except:
            gp.DeleteField_management(targ_temp1,"Clip1WA")
            gp.addfield_management(targ_temp1,"Clip1WA","float") 

        x = 1
        hydcur = gp.updatecursor('targ_Layer',"","","",'%s' % (KeyField))
        intercur = gp.searchcursor('clip_LayerWA',"","","",'%s' % (KeyField))
        f_row = intercur.next()
        while f_row:
            x += 1    
            search_val = f_row.GetValue('%s' % (KeyField))    
            i_row = hydcur.next()  
            while i_row:
                checkval = f_row.GetValue('%s' % (KeyField))
                if search_val == i_row.GetValue('%s' % (KeyField)):
                    nowval = f_row.GetValue('%s' % (KeyField))
                    newval = f_row.getvalue('Clip1WA')
                    i_row.SetValue('Clip1WA', newval)
                    hydcur.updaterow(i_row)
                    break
                else:        
                    i_row = hydcur.next()
            #cur = gp.searchcursor('clip_Layer',"","","",'OBJECTID')
            f_row = intercur.next()
          

                
        del f_row, hydcur, intercur

        prog.Update(4)
        #######Make WaClip center points features 
        try:
            gp.addfield_management(clip_temp1,"XmidClip","double")   
        except:
            gp.DeleteField_management(clip_temp1,"XmidClip")
            gp.addfield_management(clip_temp1,"XmidClip","double") 

        try:
            gp.addfield_management(clip_temp1,"YmidClip","double")   
        except:
            gp.DeleteField_management(clip_temp1,"YmidClip")
            gp.addfield_management(clip_temp1,"YmidClip","double") 



        x = 1
        intercur = gp.updatecursor('clip_LayerWA',"","","",'%s' % (KeyField))
        f_row = intercur.next()
        while f_row:
            x += 1
            newval = f_row.shape
            cstring = str(newval.Centroid)
          
            f_row.SetValue('XmidClip', cstring.split()[0])
           
            f_row.SetValue('YmidClip', cstring.split()[1])
            intercur.updaterow(f_row)
            f_row = intercur.next()

        # Perform identity analysis from midpoints and water bodies
        IdentityWA_shp = identities + wria + "_IdentityWA.shp"
        # 1 Process: Make XY Event Layer from MIDPOINTS
        gp.MakeXYEventLayer_management(clip_temp1, "XmidClip", "YmidClip", 'point_Layer')
        gp.MakeFeatureLayer_management('point_Layer', 'all_Layer', "", "")
        gp.MakeFeatureLayer_management(wabody, 'wab_Layer', "", "")
        gp.CopyFeatures_management('all_Layer',outpath + '/output/allLayerWA.shp')
        gp.Identity_analysis('all_Layer', wabody, IdentityWA_shp, "ALL", "", "NO_RELATIONSHIPS")
    prog.Update(5)
    prog.Destroy()

def EndCalc(wria, temptarg, length_field):
    progMax = 4
    prog = wx.ProgressDialog("WRIA %s " % wria,"Calculate %: Step 5 of 6",
                             maximum = progMax, style = wx.PD_ELAPSED_TIME | wx.PD_AUTO_HIDE)
    count = 0

    targ_temp1 = temptarg + wria + ".shp"
    gp.MakeFeatureLayer_management(targ_temp1, 'targ_Layer' )
    print targ_temp1

    try:
        gp.AddField_management(targ_temp1, "Clip_Perc", "FLOAT")    
    except:
        gp.DeleteField_management(targ_temp1, "Clip_Perc")
        gp.AddField_management(targ_temp1, "Clip_Perc", "FLOAT") 
        


    try:
        gp.AddField_management(targ_temp1, "WaBod_Perc", "FLOAT")    
    except:
        gp.DeleteField_management(targ_temp1, "WaBod_Perc")
        gp.AddField_management(targ_temp1, "WaBod_Perc", "FLOAT")     
      
    #gp.CalculateField_management(targ_temp1, "Clip_Km", "[Clip40l] * 0.0003048", "VB")
    try:
        
        gp.CalculateField_management(targ_temp1, "Clip_Perc", "[Clip40l] / [%s]" % (length_field), "VB")
        gp.CalculateField_management(targ_temp1, "WaBod_Perc", "[Clip1WA] / [%s]" % (length_field), "VB")
    except:
        print "length field = [%s]" % (length_field)

    gp.SelectLayerByAttribute_management('targ_Layer', "NEW_SELECTION", ' "COWBUF" = 9999')
    gp.SelectLayerByAttribute_management('targ_Layer', "SUBSET_SELECTION", ' "Clip_Perc" > 0.8 ')
    prog.Update(1)
    gp.CalculateField_management('targ_Layer', "COWBUF", "1080", "VB", "")
    gp.SelectLayerByAttribute_management('targ_Layer', "SUBSET_SELECTION", ' "Clip_Perc" > 0.95 ')
    gp.CalculateField_management('targ_Layer', "COWBUF", "1095", "VB", "")
    prog.Update(2)
    gp.SelectLayerByAttribute_management('targ_Layer', "NEW_SELECTION", ' "COWBUF" = 9999 ')
    gp.SelectLayerByAttribute_management('targ_Layer', "SUBSET_SELECTION", ' "Clip1l" = 0 ')
    gp.CalculateField_management('targ_Layer', "COWBUF", "1100", "VB", "")
    prog.Update(3)
    gp.SelectLayerByAttribute_management('targ_Layer', "NEW_SELECTION", ' "COWBUF" = 9999 ')
    gp.SelectLayerByAttribute_management('targ_Layer', "SUBSET_SELECTION", ' "Clip1l" < 2 ')
    gp.CalculateField_management('targ_Layer', "COWBUF", "1002", "VB", "")
    prog.Update(4)
    prog.Destroy()

	
def IntersectIntegrate(wria, temptarg, id_field, KeyField, identities, KeyField3, radii, outpath, dowaterba):    
  
    progMax = 4
    prog = wx.ProgressDialog("WRIA %s " % wria,"Integrate %: Step 6 of 6",
                             maximum = progMax, style = wx.PD_ELAPSED_TIME | wx.PD_AUTO_HIDE)
    count = 0
    wchydro_shp = temptarg + wria + ".shp"

    identityDICT = {}
    for i in radii:
        identityDICT[i] = identities + wria + "_Identity" + str(i)+ ".shp"

    print "hello 1"        
##    Identity10_shp = identities + wria + "_Identity10.shp"
##    Identity40_shp = identities + wria + "_Identity40.shp"
##    Identity100_shp = identities + wria + "_Identity100.shp"
 
    IdentityWA_shp = identities + wria + "_IdentityWA.shp"

    #Create new feature to append to and append indentify layers
    Intersects_shp = outpath + "/output/NEWintersects" + wria + ".shp"
    print "hello 2" 
    try:
        gp.AddField_management(wchydro_shp, "WABODY_ID", "LONG", "9")    
    except:
        gp.DeleteField_management(wchydro_shp, "WABODY_ID")
        gp.AddField_management(wchydro_shp, "WABODY_ID", "LONG", "9")
    print "hello 3" 
    try:
     gp.makefeaturelayer(Intersects_shp, "InterTemp")   
     gp.DeleteFeatures_management("InterTemp")
    except:
     print 'not there'

    print 'pause'
    generatorRadii = (r for r in radii)
    iterG = iter(generatorRadii)
    
    #Start loop through radii using a generator function
    gp.CopyFeatures_management(identityDICT[iterG.next()],Intersects_shp)
    #gp.CopyFeatures_management(Identity1_shp,"C:/data/bob.shp")
    try:
        while iterG:
            gp.Append_management(str(identityDICT[iterG.next()]),Intersects_shp)
    except:
        print "iter done"
    print "hello 4" 
    #gp.Append_management(str(Identity10_shp + ';' + Identity40_shp),Intersects_shp)
    ##gp.Append_management(str(Identity10_shp),Intersects_shp)

    oids = []
    comids= []
    comdict = {}

    getcom = gp.searchcursor(Intersects_shp,"","","",'%s' % (KeyField))
    i_row = getcom.next() 
    while i_row:    
        nowval = i_row.GetValue('%s' % (KeyField))
        newval = i_row.getvalue('%s' % (id_field))#('RIVERS_ID_')
        oids.append(nowval)
        comids.append(newval)
        i_row = getcom.next()
        comdict[nowval] = newval
    print 'Length of comdict is ' + str(len(comdict))
    prog.Update(1)
    #Create layer or plausible targets to reduce search time
    gp.MakeFeatureLayer_management(wchydro_shp, 'hydro_Layer', ' "COWBUF" <> 9999 ' )
    gp.CopyFeatures_management('hydro_Layer',"c:/data/bob.shp")
    print "starting loop"
    #Loop through sorted datasets and lookup matching data
    x = 1
    hydcur = gp.updatecursor('hydro_Layer',"","","",'%s' % (KeyField))
    f_row = hydcur.next()

    #intercur = gp.searchcursor(Intersects_shp,"","","",'%s' % (KeyField))
    while f_row:
        x += 1
        try:
            search_val = f_row.GetValue('%s' % (KeyField))
            newval = comdict[search_val]
            f_row.SetValue('COWSEG', newval)
            hydcur.updaterow(f_row)
        except KeyError: 
            print 'no match on ' +  str(x)  
        f_row = hydcur.next()
    prog.Update(2) 
    # #####WATER BODY INTEGRATION
    if dowaterba == 0:
        gp.MakeFeatureLayer_management(wchydro_shp, 'hydro_Layer')
        oidsw = []
        comidsw= []
        comdictw = {}
        getcom = gp.searchcursor(IdentityWA_shp,"","","",'%s' % (KeyField))
        w_row = getcom.next() 
        while w_row:    
            nowval = w_row.GetValue('%s' % (KeyField))
            newval = w_row.getvalue('%s' % (KeyField3))#('RIVERS_ID_')
            oidsw.append(nowval)
            comidsw.append(newval)
            w_row = getcom.next()
            comdictw[nowval] = newval
               
        prog.Update(3)
            #Loop through sorted datasets and lookup matching data
        x = 1
        hydcur2 = gp.updatecursor('hydro_Layer',"","","",'%s' % (KeyField))
        f2_row = hydcur2.next()

        #intercur = gp.searchcursor(Intersects_shp,"","","",'%s' % (KeyField2))
        while f2_row:
            x += 1
            try:
                search_val = f2_row.GetValue('%s' % (KeyField))
                newval = comdictw[search_val]
                f2_row.SetValue('WABODY_ID', newval)
                hydcur2.updaterow(f2_row)
            except KeyError: 
                print 'no match on ' +  str(x)  
            f2_row = hydcur2.next()

    prog.Update(4)
    prog.Destroy()
    print "Step 6 done"
            
        
def hydroDirectories(rootFolder):
    rootFolder = "c:/data/hydrotest/folders"
    try:
        os.makedirs(rootFolder)
    except OSError:
        print "Directory already exists"

    try:
        os.makedirs(rootFolder + "/target")
    except OSError:
        print "Directory already exists"

    try:
        os.makedirs(rootFolder + "/buffersource")
    except OSError:
        print "Directory already exists"

    try:
        os.makedirs(rootFolder + "/buffers")
    except OSError:
        print "Directory already exists"

    try:
        os.makedirs(rootFolder + "/output")
    except OSError:
        print "Directory already exists"

    try:
        os.makedirs(rootFolder + "/results")
    except OSError:
        print "Directory already exists"

    try:
        os.makedirs(rootFolder + "/identity")
    except OSError:
        print "Directory already exists"



	