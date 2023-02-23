import os, sys
import gmsh
import meshio
import numpy as np
import scipy as sp

# ========================================================= #
# ===  modify__2Dmesh_into_3Dmesh.py                    === #
# ========================================================= #

def modify__2Dmesh_into_3Dmesh( inpFile=None, outFile=None, elementType="triangle",
                                ref_="z", interpolateData=None, function=None, parameters=[] ):

    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile     is None ):
        sys.exit( "[modify__2Dmesh_into_3Dmesh.py] inpFile == ???" )
    extension = ( inpFile.split( "." ) )[-1]
    if ( outFile     is None ):
        outFile = inpFile.replace( "."+extension, "_."+extension )
    if   ( type(ref_) == int ):
        if ( ( ref_ >= 0 ) and ( ref_ <= 2 ) ):
            ref_ = ["x","y","z"][ ref_ ]
        else:
            print( "[modify__2Dmesh_into_3Dmesh.py] ref_ should be  x / y / z " )
            sys.exit()
    elif ( type(ref_) == str ):
        if ( ref_ in [ "x", "y", "z" ] ):
            pass
        else:
            print( "[modify__2Dmesh_into_3Dmesh.py] ref_ should be  x / y / z " )
            sys.exit()
    else:
        print( "[modify__2Dmesh_into_3Dmesh.py] ref_ should be  x / y / z " )
        sys.exit()

    # ------------------------------------------------- #
    # --- [2] load mesh                             --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.load__meshio as mio
    rmesh = mio.load__meshio( mshFile=inpFile, elementType=elementType )
    nodes = rmesh["points"]
    elems = rmesh["cells"]

    # ------------------------------------------------- #
    # --- [3] modification                          --- #
    # ------------------------------------------------- #
    # -- [3-1] interpolation                        --  #
    if ( interpolateData is not None ):
        coord    = np.copy( interpolateData[:,x_:y_+1] )
        value    = np.copy( interpolateData[:,z_]      )
        function = sp.interpolate.LinearNDInterpolator( coord, value )
    if ( function is None ):
        print( "\033[31m" + "[modify__2Dmesh_into_3Dmesh.py] no function or"\
               " interpolateData is defined.... [ERROR] " + "\033[0m" )
        sys.exit()
    
    # -- [3-2] function                             --  #
    if ( ref_ == "x" ):
        c1, c2, cA = y_, z_, x_
    if ( ref_ == "y" ):
        c1, c2, cA = x_, z_, y_
    if ( ref_ == "z" ):
        c1, c2, cA = x_, y_, z_
    nodes[:,cA] = function( nodes[:,c1], nodes[:,c2], *parameters )

    # ------------------------------------------------- #
    # --- [4] write in a mesh File                  --- #
    # ------------------------------------------------- #
    cells = { elementType: elems }
    wmesh = meshio.Mesh( nodes, cells )
    wmesh.write( outFile, file_format="gmsh" )
    print( "[modify__2Dmesh_into_3Dmesh.py] output file :: {} ".format( outFile ) )
    return( nodes )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    inpFile    = "test/poleSurface_2d.msh"
    outFile    = "test/poleSurface_3d.msh"
    function   = lambda x,y,r: (-0.12)*np.sqrt( 1.0+np.round( (x/r)**2+(y/r)**2, 10 ) ) + 0.2
    parameters = [ 1.0 ]

    ret        = modify__2Dmesh_into_3Dmesh( inpFile=inpFile, outFile=outFile, \
                                             function=function, parameters=parameters )
    print( ret )
    print( ret.shape )
