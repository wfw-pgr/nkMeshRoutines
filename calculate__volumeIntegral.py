import os, sys
import numpy as np


# ========================================================= #
# ===  calcualte__volumeIntegral.py                     === #
# ========================================================= #

def calculate__volumeIntegral( inpFile=None, target=None, physNum=None, \
                               elementType="tetra", silent=False ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[calculate__volumeIntegral.py] inpFile == ???" )
    if ( target  is None ): sys.exit( "[calculate__volumeIntegral.py] target  == ???" )

    # ------------------------------------------------- #
    # --- [2] load mesh file                        --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.load__meshio as lms
    rmesh    = lms.load__meshio( mshFile=inpFile, elementType=elementType )
    elems    = rmesh["cells"]
    nodes    = rmesh["points"]
    cellData = rmesh["cellData"]
    if   ( target is None ):
        print( "[calculate__volumeIntegral.py] target is None... [ERROR] " )
        sys.exit()
    elif ( target in cellData ):
        targetD = cellData[target]
    else:
        print( "[calculate__volumeIntegral.py] cannot find target (:{0}) in {1}... [ERROR] "\
               .format( target, inpFile ) )
        sys.exit()
    
    # ------------------------------------------------- #
    # --- [3] calculate volume of elements          --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.calculate__tetraVolume as ctv
    if ( elementType == "tetra" ):
        volumes  = ctv.calculate__tetraVolume( elems=elems, nodes=nodes )
    else:
        print( "[calculate__volumeIntegral.py] only tetra.... [ERROR]" )
        sys.exit()

    # ------------------------------------------------- #
    # --- [4] limit physNum                         --- #
    # ------------------------------------------------- #
    if ( physNum is not None ):
        if ( not( "physNums" in rmesh ) ):
            print( "[calculate__volumeIntegral.py] cannot find physNums in {}".format(inpFile))
            sys.exit()
        physNums = np.array( rmesh["physNums"], dtype=np.int64 )
        index    = np.where( physNums == physNum )
        volumes  = volumes[index]
        targetD  = targetD[index]

    # ------------------------------------------------- #
    # --- [5] calculate volume integral             --- #
    # ------------------------------------------------- #
    volSum = np.sum( volumes )
    volInt = np.sum( volumes * targetD )
    if ( volSum > 0.0 ):
        volAvg = volInt / volSum
    else:
        print( "[calculate__volumeIntegral.py] volume is negative.... [CAUTION] :: {}".format( volSum ) )
        volAvg = None

    # ------------------------------------------------- #
    # --- [6] display and return                    --- #
    # ------------------------------------------------- #
    if ( not( silent ) ):
        print( "-"*70 )
        print( "       target    :: {}".format( target ) )
        print( " volume total    :: {}".format( volSum ) )
        print( " volume integral :: {}".format( volInt ) )
        print( " volume average  :: {}".format( volAvg ) )
        print( "-"*70 )
        return( (volInt,volSum,volAvg) )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile = "test/out.vtu"
    target  = "density"
    physNum = None
    ret     = calculate__volumeIntegral( inpFile=inpFile, target=target, physNum=physNum )
    
