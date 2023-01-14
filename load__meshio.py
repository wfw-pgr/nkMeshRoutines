import os, sys
import meshio
import numpy as np


# ========================================================= #
# ===  load__meshio.py                                  === #
# ========================================================= #

def load__meshio( mshFile=None, elementType=None, returnType="dict" ):

    #  -- elementType :: return only elementType: [ tetra, line, triangle, vertex, etc. ]
    #  -- returnType  :: return Data Type :: [ dict, list, elem, physNum, etc. ]

    # element number :: [ 0 ~ nElems-1 ]  <<<  [CAUTION] element Number begins from 0
    # node    number :: [ 0 ~ nNodes-1 ]
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( mshFile        is None ):
        sys.exit( "\033[31m" + "[load__meshio.py] mshFile        == ???    [ERROR]" + "\033[0m" )
        
    extension = ( mshFile.split( "." ) )[-1]

    if ( elementType is None ):
        print( "\033[31m" + "[load__meshio.py] elementType is None.... return all element's Data.... " + "\033[0m" )
        

    # ------------------------------------------------- #
    # --- [2] bdf by Gmsh exception                 --- #
    # ------------------------------------------------- #
    contents = None
    if ( extension.lower() == "bdf" ):
        with open( mshFile, "r" ) as f:
            line1 = f.readline()
            if ( ( ( line1.strip() ).lower() ) == "$ Created by Gmsh".lower() ):
                contents = f.read()
    if ( contents is not None ):
        mshFile = mshFile.replace( ".bdf", "_.bdf" )
        with open( mshFile, "w" ) as f:
            f.write( "$ Generated by nkMeshRoutines.save__nastranFile.py by N.K." + "\n" )
            f.write( "BEGIN BULK" + "\n" )
            f.write( contents )
            
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
        if   ( elementType.lower() in [ "all" ] ):
            pass
        elif ( elementType.lower() in cellType  ):
            cells    = cells[elementType]
            cellData = { key:cellData[key][elementType] for key in cellDataType }
            nCells   = [ cells.shape[0] ]
        else:
            print( "[load__meshio.py] elementType is NOT in cellType... [WARNING]" )

    if ( "nastran:ref"   in cellDataType ):
        physNums  = np.array( cellData["nastran:ref"]   )
    if ( "gmsh:physical" in cellDataType ):
        physNums  = np.array( cellData["gmsh:physical"] )
        
    print( "[load__meshio.py] loaded mshFile       ::   {0}".format( mshFile         ) )
    print( "[load__meshio.py] elementType          ::   {0}".format( elementType     ) )
    print( "[load__meshio.py] loaded points        ::   {0}".format( points.shape[0] ) )
    print( "[load__meshio.py] loaded cells         ::   {0}".format( nCells          ) )
    print( "[load__meshio.py] loaded cellType      :: [ {0} ]".format( ", ".join( cellType      ) ) )
    print( "[load__meshio.py] loaded cellDataType  :: [ {0} ]".format( ", ".join( cellDataType  ) ) )
    print( "[load__meshio.py] loaded pointDataType :: [ {0} ]".format( ", ".join( pointDataType ) ) )
    if ( physNums is None ):
        print( "[load__meshio.py] No physical Numbers  ::   {0}".format( physNums        ) )
    else:
        print( "[load__meshio.py] physNums'shape       ::   {0}".format( physNums.shape  ) )
        print( "[load__meshio.py] physNums             ::   {0}".format( set( physNums ) ) )
        

    print( "\n" + "-----------------------------------------------"*2 + "\n" )
 
    # ------------------------------------------------- #
    # --- [4] make return dataset                   --- #
    # ------------------------------------------------- #
    
    if   ( returnType.lower() == "list" ):
        return( [ cells, points, pointData, cellData, physNums ] )
        
    elif ( returnType.lower() == "dict" ):
        return( { "cells":cells, "points":points, "cellData":cellData, "pointData":pointData, \
                  "physNums":physNums } )
    
    elif ( returnType.lower() in [ "elem-node", "node-elem", "cell-point" ] ):
        return( [ cells, points ] )

    elif ( returnType.lower() in [ "node-elem-phys" ] ):
        return( [ points, cells, physNums ] )

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
    ret = load__meshio( mshFile="test/model.msh"    , elementType="tetra", returnType="dict" )
    ret = load__meshio( mshFile="test/model.bdf"    , elementType="tetra", returnType="dict" )
    ret = load__meshio( mshFile="test/converted.bdf", elementType="tetra", returnType="dict" )


    # ret = load__meshio( mshFile="test/model.msh"    , elementType="tetra", returnType="dict" )
    # cells = ret["cells"]
    # print( np.min( cells ), np.max( cells ) )
    
    # ret = load__meshio( mshFile="test/model.bdf"    , elementType="tetra", returnType="dict" )
    # cells = ret["cells"]
    # print( np.min( cells ), np.max( cells ) )
    
    # ret = load__meshio( mshFile="test/converted.bdf", elementType="tetra", returnType="dict" )
    # cells = ret["cells"]
    # print( np.min( cells ), np.max( cells ) )
