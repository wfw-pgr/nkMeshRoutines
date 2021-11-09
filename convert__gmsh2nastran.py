import os, sys
import numpy as np


# ========================================================= #
# ===  convert__gmsh2nastran                            === #
# ========================================================= #

def convert__gmsh2nastran( inpFile=None, outFile=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[convert__gmsh2nastran.py] inpFile == ???" )
    if ( outFile is None ): outFile = inpFile.replace( ".msh", ".bdf" )
    
    # ------------------------------------------------- #
    # --- [2] load gmsh File                        --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.load__meshio as lms
    ret     = lms.load__meshio( mshFile=inpFile, returnType="dict" )
    print( "[convert__gmsh2nastran.py] converting {0} ==> {1}".format( inpFile, outFile ) )
    points  = np.array( ret["points"] )
    cells   = np.array( ret["cells"]["tetra"] )
    physNum = np.array( ret["cellData"]["gmsh:physical"]["tetra"] )

    # ------------------------------------------------- #
    # --- [3] write nastran Data                    --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.save__nastranFile as snf
    snf.save__nastranFile( points=points, cells=cells, matNums=physNum, outFile=outFile )
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile = "msh/model.msh"
    outFile = "msh/out.bdf"
    convert__gmsh2nastran( inpFile=inpFile, outFile=outFile )
