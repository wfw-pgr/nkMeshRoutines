import numpy as np


# ========================================================= #
# ===  save in elmer Node file format                   === #
# ========================================================= #
def save__elmerNodeFile( nodes=None, nodeFile=None, fmt=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( nodes    is None ): sys.exit( "[save__elmerNodeFile] nodes    == ???" )
    if ( nodeFile is None ): nodeFile = "out.nodes"
    if ( fmt      is None ): fmt      = "%d %d %+15.9e %+15.9e %+15.9e"


    # ------------------------------------------------- #
    # --- [2] save nodes in a File                  --- #
    # ------------------------------------------------- #
    nNodes      = nodes.shape[0]
    nComponents = nodes.shape[1]
    wData       = np.zeros( (nNodes,5) )
    
    if   ( nComponents == 3 ):
        wData[:,0  ] = np.arange( 1, nNodes+1 )
        wData[:,1  ] = np.ones  ( (nNodes,)  ) * ( -1 )
        wData[:,2: ] = nodes[:,:]    
    elif ( nComponents == 5 ):
        wData = nodes
        
    with open( nodeFile, "w" ) as f:
        np.savetxt( f, wData, fmt=fmt )

    print( "[save__elmerNodeFile] output :: {0} ".format( nodeFile ) )
    return()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    import nkUtilities.equiSpaceGrid3D as esg
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]
    nodes       = esg.equiSpaceGrid3D( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    	      			       x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    nodeFile    = "mesh.nodes"
    save__elmerNodeFile( nodes=nodes, nodeFile=nodeFile )
