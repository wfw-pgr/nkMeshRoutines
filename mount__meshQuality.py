import os, sys
import numpy as np


# ========================================================= #
# ===  mount__meshQuality.py                            === #
# ========================================================= #

def mount__meshQuality( mshFile=None, inpFile=None, outFile="dat/mesh_quality.vtu" ):

    num_,mat_,nd1_,nd2_,nd3_,nd4_ = 0, 1, 2, 3, 4, 5
    cellDataName                  = [ "volume", "area", "length", "rho", "eta", "gamma" ]
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( mshFile is None ): sys.exit( "[mount__meshQuality.py] mshFile == ???" )

    # ------------------------------------------------- #
    # --- [2] load mesh File / quality Data         --- #
    # ------------------------------------------------- #
    import load__nastranFile as inf
    nodes, elems = inf.load__nastranFile( inpFile=mshFile )
    matNums      = elems[:,mat_]
    elems        = elems[:,nd1_:nd4_+1] - 1

    # ------------------------------------------------- #
    # --- [3] load / generate quality Data          --- #
    # ------------------------------------------------- #
    if ( inpFile is None ):
        import nkMeshRoutines.assess__meshQuality as amq
        inpFile  = mshFile
        quaFile  = "dat/mesh_quality.dat"
        Data     = amq.assess__meshQuality( inpFile=inpFile, outFile=quaFile )

    else:
        import nkUtilities.load__pointFile as lpf
        Data = lpf.load__pointFile( inpFile=inpFile, returnType="point" )

    # ------------------------------------------------- #
    # --- [4] construct unstructured Grid           --- #
    # ------------------------------------------------- #
    import nkVTKRoutines.construct__uGrid as cug
    cug.construct__uGrid( nodes=nodes, elems=elems, vtkFile=outFile, \
                          cellData=Data, cellDataName=cellDataName )
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    mshFile = "msh/model_light.bdf"
    mount__meshQuality( mshFile=mshFile )
