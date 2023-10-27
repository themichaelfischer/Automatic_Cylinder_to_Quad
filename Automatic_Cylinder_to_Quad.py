''' Automatic Cylinder to Quad Script by Michael Fischer V1.1'''
''' !!!BEFORE YOU USE!!!: Go to component mode and select an edge on an object. Ctrl + Right click on an open space
    To edges > To Contiguous Edges Options > Change Maximum 2D Angle to 90+ '''
'''HOW TO USE: Select 2 edges on the end of your cylinder and run the script'''

import maya.cmds as cmds
import maya.mel as mel

#Step 1: Grab 2 edges and store vertices in a variable
sel = cmds.ls(selection = True)

try:
    sel_iso1 = sel[0].partition("[")
    sel_iso2 = sel_iso1[-1].partition("]")[0]
    sel_iso3 = sel_iso2.partition(":")
    
    sel_r1 = int(sel_iso3[0])
    sel_r2 = int(sel_iso3[-1])

except:
    pass

vert_order = cmds.polyListComponentConversion(toVertex =True)
vert_len = len(vert_order)

obj_name = vert_order[0].partition(".")[0]
cmds.select(obj_name)

mel.eval("DeleteHistory")
if len(sel) == 1:
    cmds.select("{0}[{1}]".format(sel_iso1[0],sel_r1),"{0}[{1}]".format(sel_iso1[0],sel_r2))
else:
    cmds.select(sel[0],sel[1])
    
#Step 2: Grab continous edges, then go to faces, then decrease selection once, to contained edges
''' Don't know how to set max 2d Angle higher. Script will break here if cylindfer is a 6 edged or less cylinder'''
mel.eval("SelectContiguousEdges")

#Switching back and forth so vert count is accurate since edges group on counting\

mel.eval("PolySelectConvert 3")

num_edges = cmds.ls(selection = True)

num_iso1 = num_edges[-1].partition("[")[-1]
num_iso2 = num_iso1.partition("]")[0]
num_iso3 = num_iso2.partition(":")

range1 = int(num_iso3[0])
range2 = int(num_iso3[-1])
range = range2 - range1 + len(num_edges)
if range%2 != 0:
    range += 1


mel.eval("PolySelectConvert 20")

mel.eval("PolySelectConvert 1")
mel.eval("ShrinkLoopPolygonSelectionRegion")

mel.eval("PolySelectConvert 20")

edge_sel = cmds.ls(selection = True)[0]


if ".e" in edge_sel:
    print ("edges")
    mel.eval("doDelete")
else:
    print ("faces")

#Stpe 3: Reorder vertices with those 3 vertices to reoder from. 
cmds.select(obj_name)

vertz = False

try:
    if len(vert_order) == 1:
        print ('1')
        vert_p1 = vert_order[0].partition('[')[-1]
        vert_p2 = vert_p1.partition(']')[0]
        vert_p3 = vert_p2.partition(':')
        vert_range1 = int(vert_p3[0])
        vert_range2 = int(vert_p3[-1])
        vert_range3 = int(vert_range1 + 1)
        other_vert_order1 = "{0}.vtx[{1}]".format(obj_name,vert_range1)
        other_vert_order2 = "{0}.vtx[{1}]".format(obj_name,vert_range2)
        other_vert_order3 = "{0}.vtx[{1}]".format(obj_name,vert_range3)
        verts = []
        verts.append(other_vert_order1)
        verts.append(other_vert_order2)
        verts.append(other_vert_order3)
        vertz = True
    elif len(vert_order) == 2:
        vert_p1 = vert_order[0].partition('[')[-1]
        vert_p2 = vert_p1.partition(']')[0]
        vert_p3 = vert_p2.partition(':')

        if vert_p3[1] == ':':
            # If double in the first variable
            vert_range1 = int(vert_p3[0])
            vert_range2 = int(vert_p3[-1])
            vert2_p1 = vert_order[1].partition('[')[-1]
            vert2_p2 = vert2_p1.partition(']')[0]
            vert_range3 = int(vert2_p2)
            
            other_vert_order1 = "{0}.vtx[{1}]".format(obj_name,vert_range1)
            other_vert_order2 = "{0}.vtx[{1}]".format(obj_name,vert_range2)
            other_vert_order3 = "{0}.vtx[{1}]".format(obj_name,vert_range3)
            verts = []
            verts.append(other_vert_order1)
            verts.append(other_vert_order2)
            verts.append(other_vert_order3)
            vertz = True
            
        else:
            vert_p1 = vert_order[1].partition('[')[-1]
            vert_p2 = vert_p1.partition(']')[0]
            vert_p3 = vert_p2.partition(':')
            vert_range1 = int(vert_p3[0])
            vert_range2 = int(vert_p3[-1])
            vert2_p1 = vert_order[0].partition('[')[-1]
            vert2_p2 = vert2_p1.partition(']')[0]
            vert_range3 = int(vert2_p2)
            other_vert_order1 = "{0}.vtx[{1}]".format(obj_name,vert_range1)
            other_vert_order2 = "{0}.vtx[{1}]".format(obj_name,vert_range2)
            other_vert_order3 = "{0}.vtx[{1}]".format(obj_name,vert_range3)
            verts = []
            verts.append(other_vert_order1)
            verts.append(other_vert_order2)
            verts.append(other_vert_order3)
            vertz = True
            
except:
    pass

if vertz == True:
    try:
        cmds.meshReorder(verts[0],verts[1],verts[2])
    except:
        pass
    try:
        cmds.meshReorder(verts[0],verts[2],verts[1])
    except:
        pass
    try:
        cmds.meshReorder(verts[1],verts[0],verts[2])
    except:
        pass
    try:
        cmds.meshReorder(verts[1],verts[2],verts[0])
    except:
        pass
    try:
        cmds.meshReorder(verts[2],verts[0],verts[1])
    except:
        pass
    try:
        cmds.meshReorder(verts[2],verts[1],verts[0])
    except:
        pass
    
else:
    cmds.meshReorder(vert_order[0],vert_order[1],vert_order[2])

#Step 4: loop iterating from range of number of edges that was found in the select edge continous and half it
x = 1
y = x + 1

#While loop that connect vertices to one another iteration from +1 to -1 of the range
print (range)
try:   
    while x < range/2:
        cmds.polyConnectComponents("{0}.vtx[{1}]".format(obj_name,x),"{0}.vtx[{1}]".format(obj_name,(range-y)))
        x = x +1
        y = x + 1
except:
    pass

mel.eval("DeleteHistory")

mel.eval("SelectEdgeMask")








































































