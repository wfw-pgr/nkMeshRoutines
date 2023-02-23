import os, sys, meshio
import numpy as np

# ========================================================= #
# ===  edge Detectection for 2D triangulated mesh       === #
# ========================================================= #
def detect__boundaryLine_in2DMesh( elems=None, nodes=None, inpFile=None,  ):

    # -- return value :: [ ( element #. , pair( node #. in element ) ) ]
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( ( elems is None ) or ( nodes is None ) ):
        if ( inpFile is None ):
            sys.exit( "[detect__boundaryLine_in2DMesh.py] elems == ???" )
        else:
            import nkMeshRoutines.load__meshio as mio
            elems, nodes = mio.load__meshio( mshFile=inpFile, elementType="triangle", \
                                             returnType="elem-node" )

    # ------------------------------------------------- #
    # --- [2] detect boundary Line                  --- #
    # ------------------------------------------------- #
    nElems    = elems.shape[0]
    nNodes    = nodes.shape[0]
    eformat   = "{:0" + str( len(str(nElems)) )+ "}"
    nformat   = "{:0" + str( len(str(nNodes)) )+ "}"
    lineDict  = {}
    for iE,elem in enumerate( elems ):
        for pair in [ (0,1), (1,2), (2,0) ]:
            lkey1 = nformat.format( elem[pair[0]] ) + "-" + nformat.format( elem[pair[1]] )
            lkey2 = nformat.format( elem[pair[1]] ) + "-" + nformat.format( elem[pair[0]] )
            if   ( lkey1 in lineDict ):
                lineDict[lkey1] += [(iE,pair)]
            elif ( lkey2 in lineDict ):
                lineDict[lkey2] += [(iE,pair)]
            else:
                lineDict[lkey1]  = [(iE,pair)]

    # ------------------------------------------------- #
    # --- [3] Find lines whose count is 1           --- #
    # ------------------------------------------------- #
    lkey_stack = []
    elem_stack = []
    for lkey,value in lineDict.items():
        if ( len( lineDict[lkey] ) == 1 ):
            lkey_stack += [ lkey ]
            elem_stack += [ lineDict[lkey][0] ]
    return( elem_stack )
    
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    inpFile   = "test/poleSurface_2d.msh"
    elem_nums = detect__boundaryLine_in2DMesh( inpFile=inpFile )
    print( elem_nums )
