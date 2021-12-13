import numpy as np


# ========================================================= #
# ===  calculate tetrahedral mesh volume                === #
# ========================================================= #

def calculate__tetraVolume( elems=None, nodes=None, index_from_one=False ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( elems is None ): sys.exit( "[calculate__tetraVolume.py] elems == ???" )
    if ( nodes is None ): sys.exit( "[calculate__tetraVolume.py] nodes == ???" )

    # - elems :: [ node1, node2, node3, node4 ] :: [ nElems, 4 ]
    # - nodes :: [ x, y, z ]                    :: [ nNodes, 3 ]
    if ( elems.shape[1] != 4 ):
        print( "[calculate__tetraVolume.py] illegal elems shape :: {0} ".format( elems.shape ) )
    if ( nodes.shape[1] != 3 ):
        print( "[calculate__tetraVolume.py] illegal nodes shape :: {0} ".format( nodes.shape ) )

    # ------------------------------------------------- #
    # --- [2] index from 1 / 0                      --- #
    # ------------------------------------------------- #
    if ( index_from_one ):
        elems[:,:] = elems[:,:] - 1
        
    # ------------------------------------------------- #
    # --- [3] calculate volume of the element       --- #
    # ------------------------------------------------- #
    onesixth      = 1.0 / 6.0
    nd0, nd1      = nodes[ elems[:,0],:], nodes[ elems[:,1],:]
    nd2, nd3      = nodes[ elems[:,2],:], nodes[ elems[:,3],:]
    vc1, vc2, vc3 = nd1-nd0, nd2-nd0, nd3-nd0
    matrix        = np.concatenate( [vc1[:,:,None],vc2[:,:,None],vc3[:,:,None]], axis=2 )
    volumes       = onesixth * np.linalg.det( matrix )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( volumes )

    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkMeshRoutines.load__nastranFile as lnf
    inpFile      = "msh/model.bdf"
    nodes, elems = lnf.load__nastranFile( inpFile=inpFile )
    elems        = np.copy( elems[:,2:] )
    
    volumes      = calculate__tetraVolume( elems=elems, nodes=nodes )
    total        = np.sum( volumes )
    print( " total volume :: {0}".format( total ) )
    print( " estimated    :: ( 1 + 1 ) - 1/8 = 15/8 = 1.875" )





    # for iv,vert in enumerate( elems ):
    #     iv0,iv1,iv2,iv3 =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3 = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3     =    nd1 - nd0,    nd2 - nd0,    nd3 - nd0
    #     matrix          = np.concatenate( [vc1[:,None],vc2[:,None],vc3[:,None]], axis=1 )
    #     volumes[iv]     = onesixth * np.linalg.det( matrix )
