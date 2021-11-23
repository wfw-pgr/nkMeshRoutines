import os, sys
import meshio
import numpy as np


# ========================================================= #
# ===  load__meshio.py                                  === #
# ========================================================= #

def load__meshio( mshFile=None, elementType=None, returnType="dict", gmsh_physical=True ):

    #  -- elementType :: return only elementType: [ tetra, line, triangle, vertex, etc. ]
    #  -- returnType  :: return Data Type :: [ dict, list, elem, physNum, etc. ]

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( mshFile        is None ):
        sys.exit( "[load__meshio.py] mshFile        == ???" )
    extension = ( mshFile.split( "." ) )[-1]
    
    # ------------------------------------------------- #
    # --- [2] Load mesh File                        --- #
    # ------------------------------------------------- #
    #  -- [2-1] Load mesh File using meshIO         --  #
    print( "\n" + "-----------------------------------------------"*2 )
    print( "[load__meshio.py] loading {0} from meshIO.... ".format( mshFile ) )
    print( "-----------------------------------------------"*2 + "\n" )

    rmesh         = meshio.read( mshFile )
    cells         = rmesh.cells_dict
    cellData      = rmesh.cell_data_dict
    points        = rmesh.points
    pointData     = rmesh.point_data
    cellType      = list( cells    .keys() )
    cellDataType  = list( cellData .keys() )
    pointDataType = list( pointData.keys() )
    physNums      = None

    #  -- [2-2] number of cell counting             --  #
    nCells = []
    for ckey in cellType:
        nCell     = ( cells[ckey] ).shape[0]
        nCells   += [ nCell ]
    
    #  -- [2-3] extract certain elementType         --  #
    if ( elementType is not None ):
        if ( elementType in cellType ):
            cells    = cells[elementType]
            cellData = { key:cellData[key][elementType] for key in cellDataType }
            nCells   = [ cells.shape[0] ]
            cells_are_array = True

    if ( ( gmsh_physical is True ) and ( "gmsh:physical" in cellDataType ) ):
        physNums  = np.array( cellData["gmsh:physical"] )
    
    print( "[load__meshio.py] loaded mshFile       ::   {0}".format( mshFile         ) )
    print( "[load__meshio.py] elementType          ::   {0}".format( elementType     ) )
    print( "[load__meshio.py] loaded points        ::   {0}".format( points.shape[0] ) )
    print( "[load__meshio.py] loaded cells         ::   {0}".format( nCells          ) )
    if ( ( gmsh_physical ) and ( "gmsh:physical" in cellDataType ) ):
        print( "[load__meshio.py] gmsh:physical Found  ::   {0}".format( physNums    ) )
    else:
        print( "[load__meshio.py] NO gmsh:physical     ::   {0}".format( physNums    ) )
        
    print( "[load__meshio.py] loaded cellType      :: [ {0} ]"\
           .format( ", ".join( cellType      ) ) )
    print( "[load__meshio.py] loaded cellDataType  :: [ {0} ]"\
           .format( ", ".join( cellDataType  ) ) )
    print( "[load__meshio.py] loaded pointDataType :: [ {0} ]"\
           .format( ", ".join( pointDataType ) ) )

    print( "\n" + "-----------------------------------------------"*2 + "\n" )
 
    # ------------------------------------------------- #
    # --- [4] make return dataset                   --- #
    # ------------------------------------------------- #
    
    if   ( returnType.lower() == "list" ):
        return( [ cells, points, pointData, cellData, physNums ] )
        
    elif ( returnType.lower() == "dict" ):
        return( { "cells":cells, "points":points, "cellData":cellData, "pointData":pointData, \
                  "physNums":physNums } )
    
    elif ( returnType.lower() in [ "node-elem", "cell-point" ] ):
        return( [ cells, points ] )

    elif ( returnType.lower() in [ "cell", "elem", "cells", "elems" ] ):
        return( cells )

    elif ( returnType.lower() in [ "point", "node", "points", "nodes" ] ):
        return( points )

    elif ( returnType.lower() in [ "celldata", "elemdata" ] ):
        return( cellData )

    elif ( returnType.lower() in [ "pointdata", "nodedata" ] ):
        return( pointData )

    elif ( returnType.lower() in [ "physnums" ] ):
        return( physNums )

    else:
        print( "[load__meshio.py] returnType == ??? :: {0}".format( returnType ) )
        print( "[load__meshio.py] ( list, dict, cell, point, celldata, pointData ) " )
        sys.exit()
        


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    ret = load__meshio( mshFile="test/model.msh", elementType="tetra", gmsh_physical=False )
    print( list( ret.keys() ) )
