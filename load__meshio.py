import os, sys
import meshio
import numpy as np


# ========================================================= #
# ===  load__meshio.py                                  === #
# ========================================================= #

def load__meshio( mshFile=None, elementType=None, returnType="dict" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( mshFile        is None ): sys.exit( "[load__meshio.py] mshFile        == ???" )
    
    # ------------------------------------------------- #
    # --- [2] Load mesh File                        --- #
    # ------------------------------------------------- #
    rmesh         = meshio.read( mshFile )
    cells         = rmesh.cells_dict
    cellData      = rmesh.cell_data_dict
    points        = rmesh.points
    pointData     = rmesh.point_data
    cellType      = list( cells    .keys() )
    cellDataType  = list( cellData .keys() )
    pointDataType = list( pointData.keys() )


    # ------------------------------------------------- #
    # --- [3] fetch elementType data                --- #
    # ------------------------------------------------- #
    if ( elementType is not None ):
        if ( elementType in cellType ):
            cells    = cells   [elementType]
            cellData = { key:cellData[key][elementType] for key in cellDataType }
    
    # ------------------------------------------------- #
    # --- [4] make return dataset                   --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "list" ):
        return( [ cells, points, pointData, cellData ] )
        
    elif ( returnType.lower() == "dict" ):
        return( { "cells":cells, "points":points, "cellData":cellData, "pointData":pointData } )
    
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

    else:
        print( "[load__meshio.py] returnType == ??? :: {0}".format( returnType ) )
        print( "[load__meshio.py] ( list, dict, cell, point, celldata, pointData ) " )
        sys.exit()

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    ret = load__meshio( mshFile="msh/model.msh", elementType="tetra" )
    print( ret )
