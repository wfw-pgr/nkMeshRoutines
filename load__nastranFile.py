import numpy as np
import os, sys

# ========================================================= #
# ===  load nastran File                                === #
# ========================================================= #

def load__nastranFile( inpFile="msh/model.bdf", returnAll=False, index_from_zero=True ):

    # ------------------------------------------------- #
    # --- [1] inpFile                               --- #
    # ------------------------------------------------- #
    with open( inpFile, "r" ) as f:
        lines = f.readlines()

    # ------------------------------------------------- #
    # --- [2] nastran bdf reading                   --- #
    # ------------------------------------------------- #
    
    grid, cbar     = [], []
    ctria3, ctetra = [], []

    for line in lines:

        if ( ( line.strip() )[0] == "$" ):
            continue
        if ( len( line.strip() ) == 0   ):
            continue
        if ( ( line.strip() )         == "BEGIN BULK" ):
            continue
        if ( ( line.strip() ).lower() == "enddata" ):
            break

        words          = line.split( "," )
        
        if   ( words[0] == "GRID"   ):
            #  -- point :: [ num, MatNum, x, y, z ] -- #
            grid.append  ( [   int(words[1]),   int(words[2]), \
                             float(words[3]), float(words[4]), float(words[5]) ] )
        elif ( words[0] == "CBAR"   ):
            #  -- lines :: [ num, MatNum, node1, node2, handle?, handle?, handle? ] -- #
            cbar.append  ( [   int(words[1]),   int(words[2]),   int(words[3]),  int(words[4]), \
                             float(words[5]), float(words[6]), float(words[7]) ] )
        elif ( words[0] == "CTRIA3" ):
            #  -- triangle surface :: [ num, MatNum, node1, node2, node3 ] -- #
            ctria3.append( [ int(words[1]), int(words[2]), \
                             int(words[3]), int(words[4]), int(words[5])  ] )
        elif ( words[0] == "CTETRA" ):
            #  -- tetrahedral volume :: [ num, MatNum, node1, node2, node3, node4 ] -- #
            ctetra.append( [ int(words[1]), int(words[2]), int(words[3]), \
                             int(words[4]), int(words[5]), int(words[6])  ] )
        else:
            print( "[load__nastranFile] NOT supported shape :: {0} is found... ".format( words[0] ) )

    grid   = np.array(   grid )
    cbar   = np.array(   cbar )
    ctria3 = np.array( ctria3, dtype=np.int64 )
    ctetra = np.array( ctetra, dtype=np.int64 )

    if ( ( index_from_zero ) and ( ctria3.size > 0 ) ):
        if ( np.min(ctria3[:,2:]) != 1 ): 
            print( "[load__nastranFile.py] index_from_zero == True, "\
                   "but ctria3 begins from {0} [CAUTION] ".format( np.min(ctria3[:,2:]) ) )
        ctria3[:,2:] = ctria3[:,2:] - 1
        
    if ( ( index_from_zero ) and ( ctetra.size > 0 ) ):
        if ( np.min(ctetra[:,2:]) != 1 ): 
            print( "[load__nastranFile.py] index_from_zero == True, "\
                   "but ctetra begins from {0} [CAUTION] ".format( np.min(ctetra[:,2:]) ) )
        ctetra[:,2:] = ctetra[:,2:] - 1
    
    if ( returnAll ):
        ret    = { "grid":grid, "cbar":cbar, "ctria3":ctria3, "ctetra":ctetra }
    else:
        nodes  = np.array( grid[:,2:], dtype=np.float64 )
        elems  = np.copy ( ctetra )
        ret    = ( nodes, elems )
    return( ret )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    inpFile = "test/model.bdf"
    nodes, elems = load__nastranFile( inpFile=inpFile, index_from_zero=True )
    print( " nodes :: {0}".format( nodes.shape ) )
    print( " elems :: {0}".format( elems.shape ) )
    print( " min(elems), max(elems) :: {0}, {1}".format( np.min( elems[:,2:] ), np.max( elems[:,2:] ) ) )
