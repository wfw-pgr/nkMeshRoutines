import os, sys
import numpy as np


# ========================================================= #
# ===  convert__gmsh2nastran                            === #
# ========================================================= #

def convert__gmsh2nastran( inpFile=None, outFile=None, nodes_format=None, elementType="tetra" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[convert__gmsh2nastran.py] inpFile == ???" )
    if ( outFile is None ): outFile = inpFile.replace( ".msh", ".bdf" )
    print( "[convert__gmsh2nastran.py] convert {0} ==> {1}  :: ".format( inpFile, outFile ) )
    
    # ------------------------------------------------- #
    # --- [2] load gmsh File                        --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.load__meshio as lms
    ret     = lms.load__meshio( mshFile=inpFile, returnType="dict", elementType=elementType )

    points   = np.array( ret["points"] )
    cells    = np.array( ret["cells"] )
    if ( ret["physNums"] is not None ):
        physNums = np.array( ret["physNums"] )
    else:
        print( "[convert__gmsh2nastran.py] physNums is None :: {0} ".format( ret["physNums"] ) )
        print( "[convert__gmsh2nastran.py] set physNums = ones :: [ 1, 1, ..., 1 ] " )
        physNums = np.ones( (cells.shape[0],) )
        
    # ------------------------------------------------- #
    # --- [3] write nastran Data                    --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.save__nastranFile as snf
    snf.save__nastranFile( points=points, cells=cells, matNums=physNums, \
                           outFile=outFile, nodes_format=nodes_format )
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile = "test/model.msh"
    outFile = "test/converted.bdf"
    convert__gmsh2nastran( inpFile=inpFile, outFile=outFile )
