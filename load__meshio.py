import os, sys
import meshio
import numpy as np


# ========================================================= #
# ===  load__meshio.py                                  === #
# ========================================================= #

def load__meshio( mshFile=None, elementType=None, returnType="dict", gmsh=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( mshFile        is None ): sys.exit( "[load__meshio.py] mshFile        == ???" )
    extension = ( mshFile.split( "." ) )[-1]
    if ( gmsh is None ):
        if ( extension.lower() == "msh" ):
            gmsh = True
        else:
            gmsh = False
    else:
        gmsh = False
    
    # ------------------------------------------------- #
    # --- [2] Load mesh File                        --- #
    # ------------------------------------------------- #
    print( "[load__meshio.py] loading {0} from meshIO....       ".format( mshFile ), end="" )
    rmesh         = meshio.read( mshFile )
    cells         = rmesh.cells_dict
    cellData      = rmesh.cell_data_dict
    points        = rmesh.points
    pointData     = rmesh.point_data
    cellType      = list( cells    .keys() )
    cellDataType  = list( cellData .keys() )
    pointDataType = list( pointData.keys() )
    physNums      = None

    # ------------------------------------------------- #
    # --- [3] fetch elementType data                --- #
    # ------------------------------------------------- #
    if ( elementType is not None ):
        if ( elementType in cellType ):
            cells    = cells   [elementType]
            cellData = { key:cellData[key][elementType] for key in cellDataType }
    if ( gmsh ):
        physNums  = np.array( cellData["gmsh:physical"]["tetra"] )
    
    # ------------------------------------------------- #
    # --- [4] make return dataset                   --- #
    # ------------------------------------------------- #
    print( "[Done]" )
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
    ret = load__meshio( mshFile="msh/model.msh", elementType="tetra" )
    print( ret )
