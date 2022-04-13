import numpy as np

# ========================================================= #
# ===  inquire__nodesInPhysNum.py                       === #
# ========================================================= #

def inquire__nodesInPhysNum( mshFile=None, elementType="tetra" ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( mshFile is None ): sys.exit( "[inquire__nodesInPhysNum.py] mshFile == ???" )
    
    # ------------------------------------------------- #
    # --- [2] load mesh from MeshIO                 --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.load__meshio as lms
    meshdict  = lms.load__meshio( mshFile=mshFile, elementType=elementType, \
                                  returnType="dict" )
    nodes     = meshdict["points"]
    elems     = meshdict["cells"]
    physNums  = meshdict["physNums"]
    print( "[inquire__nodesInPhysNum.py] #. of Nodes    :: {0}".format(    nodes.shape[0] ) )
    print( "[inquire__nodesInPhysNum.py] #. of Elems    :: {0}".format(    elems.shape[0] ) )
    print( "[inquire__nodesInPhysNum.py] #. of physNums :: {0}".format( physNums.shape[0] ) )

    # ------------------------------------------------- #
    # --- [3] inquire physNum                       --- #
    # ------------------------------------------------- #
    physNum_set  = set( physNums )
    nPhysNums    = len( physNum_set )
    nodesSetDict = {}
    for ik,hphys in enumerate( physNum_set ):
        key               = "{0}".format( hphys )
        index             = np.where( physNums == hphys )
        nodesSetDict[key] = set( np.reshape( elems[index], (-1,) ) )
    return( nodesSetDict )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    mshFile = "msh/model.msh"
    ret = inquire__nodesInPhysNum( mshFile=mshFile )
    print( ret )
    print()

    intersect = np.array( list( ret["301"] & ret["302"] ) )
    print( intersect )
    print( intersect.shape )
    print()
