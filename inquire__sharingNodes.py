import numpy as np

# ========================================================= #
# ===  inquire__sharingNodes.py                         === #
# ========================================================= #

def inquire__sharingNodes( nodes=None, elems=None, physNums=None, \
                           mshFile=None, elementType="tetra", skip_empty=True ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( ( nodes is None ) or ( elems is None ) or ( physNums is None ) ):
        print( "[inquire__sharingNodes.py] nodes / elems / physNums is None." )
        print( "[inquire__sharingNodes.py] try to load mshFile..." )
        if ( mshFile is not None ):
            import nkMeshRoutines.load__meshio as lms
            meshdict  = lms.load__meshio( mshFile=mshFile, elementType=elementType, \
                                          returnType="dict" )
            nodes     = meshdict["points"]
            elems     = meshdict["cells"]
            physNums  = meshdict["physNums"]
            print( "[inquire__physNumOnNodes.py] #. of Nodes    :: {0}"\
                   .format(    nodes.shape[0] ) )
            print( "[inquire__physNumOnNodes.py] #. of Elems    :: {0}"\
                   .format(    elems.shape[0] ) )
            print( "[inquire__physNumOnNodes.py] #. of physNums :: {0}"\
                   .format( physNums.shape[0] ) )
        else:
            sys.exit( "[inquire__sharingNodes.py] mshFile == ???" )
    
    # ------------------------------------------------- #
    # --- [2] inquire nodes in each physNum         --- #
    # ------------------------------------------------- #
    physNum_set  = set( physNums )
    nPhysNums    = len( physNum_set )
    nodesSetDict = {}
    for ik,hphys in enumerate( physNum_set ):
        key               = "{0}".format( hphys )
        index             = np.where( physNums == hphys )
        nodesSetDict[key] = set( np.reshape( elems[index], (-1,) ) )

    # ------------------------------------------------- #
    # --- [3] inquire common nodes                  --- #
    # ------------------------------------------------- #
    table  = {}
    for hphys1 in physNum_set:
        key1        = "{0}".format( hphys1 )
        table[key1] = {}
        for hphys2 in physNum_set:
            key2 = "{0}".format( hphys2 )
            if ( hphys1 == hphys2 ):
                ( table[key1] )[key2] = set()
            else:
                ( table[key1] )[key2] = nodesSetDict[key1] & nodesSetDict[key2]

    # ------------------------------------------------- #
    # --- [4] skip empty sets                       --- #
    # ------------------------------------------------- #
    if ( skip_empty ):
        for hphys1 in physNum_set:
            for hphys2 in physNum_set:
                key1 = "{0}".format(hphys1)
                key2 = "{0}".format(hphys2)
                if ( len( table[key1][key2] ) == 0 ):
                    ( table[key1] ).pop( key2 )
    return( table )
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    mshFile    = "msh/model.msh"
    shareNodes = inquire__sharingNodes( mshFile=mshFile )
    print( shareNodes.keys() )
    print( shareNodes["301"].keys() )
    print( shareNodes["302"].keys() )
    print( shareNodes["303"].keys() )
    
