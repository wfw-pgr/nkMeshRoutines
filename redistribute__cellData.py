import numpy                       as np
import nkUtilities.load__pointFile as lpf

# ========================================================= #
# === redistrube  cellData to nodeData from File        === #
# ========================================================= #

def redistribute__cell2node( inpFile =None, elemFile=None, nodeFile=None ):

    # ------------------------------------------- #
    # --- :: inpFile  :: Data [nElems  ]   :: --- #
    # --- :: elemFile :: elems[nElems,3]   :: --- #
    # --- :: nodeFile :: nodes[nElems,3]   :: --- #
    # ------------------------------------------- #
    
    # ------------------------------------------------- #
    # --- [1] redistribute data                     --- #
    # ------------------------------------------------- #
    x_,y_,z_    = 0, 1, 2
    Data        = lpf.load__pointFile( inpFile= inpFile, returnType="point" )
    nodes       = lpf.load__pointFile( inpFile=nodeFile, returnType="point" )
    elems       = lpf.load__pointFile( inpFile=elemFile, returnType="point" )
    elems       = np.array( elems, dtype=np.int64 )
    Data        = np.copy( Data[:,z_] )
    ret         = redistribute__cellData( Data=Data, nodes=nodes, elems=elems )
    nodes[:,z_] = ret[:]

    # ------------------------------------------------- #
    # --- [2] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile     = "dat/nodeData.dat"
    spf.save__pointFile( outFile=outFile, Data=nodes )
    return()


# ========================================================= #
# ===  redistribute__cellData.py                        === #
# ========================================================= #

def redistribute__cellData( Data=None, elems=None, nodes=None, weight__type="uniform" ):
    
    # ------------------------------- #
    # --- :: Data [nElems  ]   :: --- #
    # --- :: elems[nElems,3]   :: --- #
    # --- :: nodes[nElems,3]   :: --- #
    # ------------------------------- #
    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] load data                             --- #
    # ------------------------------------------------- #
    nNodes   = nodes.shape[0]
    nodeData = np.zeros( nNodes )

    # ------------------------------------------------- #
    # --- [2] investigate used Element Numbers      --- #
    # ------------------------------------------------- #
    usedElems  = [ [] for ik in range( nNodes ) ]
    for iE,elem in enumerate(elems):
        for iN in range(3):
            ( usedElems[ elem[iN] ] ).append( iE )

    # ------------------------------------------------- #
    # --- [3] redistribute cellData onto nodeData   --- #
    # ------------------------------------------------- #
    if ( weight__type.lower() == "uniform" ):
        for iN in range( nNodes ):
            nodeData[iN] = np.average( Data[ usedElems[iN] ] )
    return( nodeData )

    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    inpFile  = "dat/mshape_lsm.dat"
    elemFile = "dat/elems.dat"
    nodeFile = "dat/nodes.dat"
    
    redistribute__cell2node( inpFile=inpFile, elemFile=elemFile, nodeFile=nodeFile )
