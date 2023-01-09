import os, sys
import meshio
import numpy as np
import nkUtilities.cprint as cpr
import nkUtilities.load__constants as lcn

# ========================================================= #
# ===  code for PHITS-FEM simulation                    === #
# ========================================================= #
#
# --------------------------------------------------------- #
#
#  [INPUT]  
#             * density.conf   ( .conf style parameters )
#             * model.msh      ( gmsh format )
#  [OUTPUT]
#             * model.bdf      ( NASTRAN large field format )
#
#  [HOWTO]
#             * convert__gmsh2phits( inpFile="model.msh", densityFile="density.conf" )
#
#  [Contents of density.conf]
#       301        float    -7.6
#       302        float    -1.0                  etc.
#       
# --------------------------------------------------------- #
#


# ========================================================= #
# ===  convert__gmsh2phits                              === #
# ========================================================= #

def convert__gmsh2phits( inpFile=None, outFile=None, density=None, densityFile=None ):

    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[import.py] inpFile == ???"    )
    if ( outFile is None ): outFile = inpFile.replace( ".msh", ".bdf" )
    if ( density is None ):
        if ( densityFile is None ):
            cpr.cprint( "[convert__gmsh2phits.py] density == ??? , densityFile == ??? [ERROR]" )
            sys.exit()
        else:
            density = lcn.load__constants( inpFile=densityFile )

    # ------------------------------------------------- #
    # --- [2] load mesh elements & nodes            --- #
    # ------------------------------------------------- #
    print( "[save__nastranFile.py] loading gmsh FIle :: {0}".format( inpFile ), end=""  )
    import nkMeshRoutines.load__meshio as lms
    ret      = lms.load__meshio( mshFile=inpFile, returnType="dict", elementType="tetra" )
    print( "     [Done]" )

    # ------------------------------------------------- #
    # --- [3] Open / Begin Bulk statement           --- #
    # ------------------------------------------------- #
    print( "[save__nastranFile.py] saving nastranFile :: {0}".format( outFile ), end="" )
    f = open( outFile, "w" )
    f.write( "$ Generated by nkMeshRoutines.convert__gmsh2phits by N.K." + "\n" )
    f.write( "BEGIN BULK" + "\n" )

    # ------------------------------------------------- #
    # --- [4] add GRID Card                         --- #
    # ------------------------------------------------- #
    f.write( "$\n" + "$ GRID cards (nodes)" + "\n" + "$\n" )
    nPoints         = ret["points"].shape[0]
    GRID_cards      = np.array( np.repeat( "GRID*   ", nPoints ), dtype=object )
    GRID_continues  = np.array( np.repeat( "*       ", nPoints ), dtype=object )
    GRID_returns    = np.array( np.repeat( "\n"      , nPoints ), dtype=object )
    GRID_IDs        = np.arange( nPoints ) + 1
    coord_IDs1      = np.zeros( (nPoints,) )
    coord_IDs2      = np.zeros( (nPoints,) )
    GRID_fmt        = "".join( ["%8s","%16d","%16d","%16.9e","%16.9e","%s", "%8s", "%16.9e","%16d"] )
    GRID_Data       = np.concatenate( [GRID_cards[:,None], GRID_IDs[:,None], coord_IDs1[:,None], \
                                       ret["points"][:,x_][:,None], ret["points"][:,y_][:,None], \
                                       GRID_returns[:,None], GRID_continues[:,None], \
                                       ret["points"][:,z_][:,None], coord_IDs2[:,None] ], axis=1 )
    np.savetxt( f, GRID_Data, fmt=GRID_fmt, delimiter="" )

    # ------------------------------------------------- #
    # --- [4] add CTETRA Card                       --- #
    # ------------------------------------------------- #
    f.write( "$\n" + "$ CTETRA cards (elements) " + "\n" + "$\n" )
    nCells          = ret["cells"].shape[0]
    CTETRA_cards    = np.array( np.repeat( "CTETRA  ", nCells ), dtype=object )
    CTETRA_IDs      = np.arange( nCells ) + 1
    CTETRA_Data     = np.concatenate( [ CTETRA_cards[:,None]   , CTETRA_IDs[:,None], \
                                        ret["physNums"][:,None], ret["cells"] ], axis=1 )
    CTETRA_fmt      = "".join( ["%8s","%8d","%8d","%8d","%8d","%8d","%8d"] )
    np.savetxt( f, CTETRA_Data, fmt=CTETRA_fmt, delimiter="" )

    # ------------------------------------------------- #
    # --- [5] add PSOLID Card                       --- #
    # ------------------------------------------------- #
    f.write( "$\n" + "$ PSOLID cards ( Material info ) " + "\n" + "$\n" )
    physNums_set    = list( set( ret["physNums"] ) )
    nPSOLID         = len( physNums_set )
    PSOLID_cards    = np.array( np.repeat( "PSOLID  ", nPSOLID ), dtype=object )
    PSOLID_PIDs     = np.array( physNums_set )
    PSOLID_MIDs     = np.array( physNums_set )
    PSOLID_coordIDs = np.zeros( (nPSOLID,) )
    PSOLID_fmt      = "".join( ["%8s","%8d","%8d","%8d" ] )
    PSOLID_Data     = np.concatenate( [ PSOLID_cards[:,None], PSOLID_PIDs[:,None], \
                                        PSOLID_MIDs[:,None], PSOLID_coordIDs[:,None] ], axis=1 )
    np.savetxt( f, PSOLID_Data, fmt=PSOLID_fmt, delimiter="" )

    # ------------------------------------------------- #
    # --- [6] add MAT1 Card                         --- #
    # ------------------------------------------------- #
    f.write( "$\n" + "$ MAT1 cards ( Material Data :: Density ) " + "\n" + "$\n" )
    MAT1_MIDs       = PSOLID_MIDs
    nMAT1           = len( MAT1_MIDs )
    MAT1_cards      = np.array( np.repeat( "MAT1*   ", nMAT1 ), dtype=object )
    MAT1_continues  = np.array( np.repeat( "*       ", nMAT1 ), dtype=object )
    MAT1_returns    = np.array( np.repeat( "\n"      , nMAT1 ), dtype=object )
    MAT1_zeroData1  = np.zeros( (nMAT1,3) )
    MAT1_zeroData2  = np.zeros( (nMAT1,3) )
    keys            = [ str(num) for num in MAT1_MIDs ]
    for key in keys:
        if ( key in density ):
            pass
        else:
            cpr.cprint( "[convert__gmsh2phits.py] Cannot Find {} in density dict.... [ERROR]".format( key) )
            sys.exit()
    MAT1_density    = np.array( [ density[key] for key in keys ] )
    
    MAT1_Data       = np.concatenate( [ MAT1_cards[:,None], MAT1_MIDs[:,None], \
                                        MAT1_zeroData1, MAT1_returns[:,None], \
                                        MAT1_continues[:,None], MAT1_density[:,None], \
                                        MAT1_zeroData2 ], axis=1 )
    MAT1_fmt        = "".join( ["%8s", "%16d", "%16.9e", "%16.9e", "%16.9e", "%s", \
                                "%8s", "%16.9e", "%16.9e", "%16.9e", "%16.9e" ] )
    np.savetxt( f, MAT1_Data, fmt=MAT1_fmt, delimiter="" )

    # ------------------------------------------------- #
    # --- [7] ENDDATA & Close File                  --- #
    # ------------------------------------------------- #
    f.write( "$\n" + "ENDDATA" + "\n" )
    f.close()
    print( "             [Done]" )
    return()
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    densityFile = "dat/density.conf"
    inpFile     = "msh/model.msh"
    convert__gmsh2phits( inpFile=inpFile, densityFile=densityFile )
    
