import numpy as np


# ========================================================= #
# ===  calculate edge length of a tetrahedral element   === #
# ========================================================= #

def calculate__tetraEdgeLength( elems=None, nodes=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( elems is None ): sys.exit( "[calculate__tetraEdgeLength.py] elems == ???" )
    if ( nodes is None ): sys.exit( "[calculate__tetraEdgeLength.py] nodes == ???" )

    # - elems :: [ node1, node2, node3, node4 ] :: [ nElems, 4 ]
    # - nodes :: [ x, y, z ]                    :: [ nNodes, 3 ]
    if ( elems.shape[1] != 4 ):
        print( "[calculate__tetraEdgeLength.py] illegal elems shape :: {0} ".format( elems.shape ) )
    if ( nodes.shape[1] != 3 ):
        print( "[calculate__tetraEdgeLength.py] illegal nodes shape :: {0} ".format( nodes.shape ) )

    # ------------------------------------------------- #
    # --- [2] calculate  in-radius of the element   --- #
    # ------------------------------------------------- #
    nd0, nd1      = nodes[ elems[:,0]-1,:], nodes[ elems[:,1]-1,:]
    nd2, nd3      = nodes[ elems[:,2]-1,:], nodes[ elems[:,3]-1,:]
    vc1, vc2, vc3 = nd1-nd0, nd2-nd0, nd3-nd0
    vc4, vc5, vc6 = nd2-nd1, nd3-nd1, nd3-nd2
    l1 , l2       = np.linalg.norm(vc1,axis=1), np.linalg.norm(vc2,axis=1)
    l3 , l4       = np.linalg.norm(vc3,axis=1), np.linalg.norm(vc4,axis=1)
    l5 , l6       = np.linalg.norm(vc5,axis=1), np.linalg.norm(vc6,axis=1)
    length        = np.concatenate( [l1[:,None],l2[:,None],l3[:,None],\
                                     l4[:,None],l5[:,None],l6[:,None]], axis=1 )
    
    # ------------------------------------------------- #
    # --- [3] return                                --- #
    # ------------------------------------------------- #
    return( length )

    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkMeshRoutines.load__nastranFile as lnf
    inpFile      = "msh/model.bdf"
    nodes, elems = lnf.load__nastranFile( inpFile=inpFile )
    elems        = np.copy( elems[:,2:] )
    
    length       = calculate__tetraEdgeLength( elems=elems, nodes=nodes )
    averaged     = np.average( length )
    print()
    print( "[calculate__tetraEdgeLength] averaged length :: {0} ".format( averaged )  )
    print()








    # for iv,vert in enumerate( elems ):
    #     # -- [2-1] surface area -- #
    #     iv0,iv1,iv2,iv3 =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3 = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3,vc4 = nd1-nd0, nd2-nd0, nd1-nd3, nd2-nd3
    #     s1              = 0.5 * np.sum( ( np.cross( vc1, vc2 ) )**2 )
    #     s2              = 0.5 * np.sum( ( np.cross( vc1, vc3 ) )**2 )
    #     s3              = 0.5 * np.sum( ( np.cross( vc2, vc4 ) )**2 )
    #     s4              = 0.5 * np.sum( ( np.cross( vc3, vc4 ) )**2 )
    #     area[iv,:]      = np.array( [s4,s3,s2,s1] )
