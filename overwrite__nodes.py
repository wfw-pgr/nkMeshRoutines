import os, sys
import meshio
import numpy as np

# ========================================================= #
# ===  overwrite__nodes.py                               === #
# ========================================================= #

def overwrite__nodes( nodes=None, mshFile=None, outFile=None ):

    # element number :: [ 0 ~ nElems-1 ]  <<<  [CAUTION] element Number begins from 0

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( nodes  is None ):
        sys.exit( "\033[31m" + "[save__modifiedNodeMesh.py] nodes  == ??? [ERROR]" + "\033[0m" )
    if ( mshFile is None ):
        sys.exit( "\033[31m" + "[save__modifiedNodeMesh.py] mshFile == ??? [ERROR]" + "\033[0m" )
    extension = ( mshFile.split( "." ) )[-1]
    if ( outFile is None ):
        outFile = mshFile.replace( extension, "_.{}".format( extension ) )

    # ------------------------------------------------- #
    # --- [2] load mesh FIle                        --- #
    # ------------------------------------------------- #
    rmesh         = meshio.read( mshFile )
    rmesh.points  = np.copy( nodes )
    if ( not( "gmsh:physical" in rmesh.cell_data ) ):
        print( "[overwrite__nodes.py] cannot find gmsh:physical..... create dummy. " )
        if ( "gmsh:geometrical" in rmesh.cell_data ):
            print( "[overwrite__nodes.py] use gmsh:geometrical " )
            rmesh.cell_data["gmsh:physical"] = rmesh.cell_data["gmsh:geometrical"]
    meshio.write( outFile, rmesh, file_format="gmsh" )
    print( "\n"+"[overwrite__node.py] output File :: {}".format( outFile ) + "\n" )
    return( outFile )
    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    x_, y_, z_ = 0, 1, 2
   
    mshFile = "test/circle.msh"
    outFile = "test/circle_mod.msh"
    import nkMeshRoutines.load__meshio as mio
    nodes   = mio.load__meshio( mshFile=mshFile, elementType="triangle", returnType="point" )
    nodes[:,z_]  = np.sqrt( nodes[:,x_]**2 + nodes[:,y_]**2 )
    print( nodes.shape )
    
    overwrite__nodes( mshFile=mshFile, nodes=nodes, outFile=outFile )


