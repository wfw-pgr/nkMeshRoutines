import numpy as np


# ========================================================= #
# ===  calculate in-out radius of a tetrahedral element === #
# ========================================================= #

def calculate__tetraInOutRadius( elems=None, nodes=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( elems is None ): sys.exit( "[calculate__tetraInOutRadius.py] elems == ???" )
    if ( nodes is None ): sys.exit( "[calculate__tetraInOutRadius.py] nodes == ???" )

    # - elems :: [ node1, node2, node3, node4 ] :: [ nElems, 4 ]
    # - nodes :: [ x, y, z ]                    :: [ nNodes, 3 ]
    if ( elems.shape[1] != 4 ):
        print( "[calculate__tetraInOutRadius.py] illegal elems shape :: {0} ".format( elems.shape ) )
    if ( nodes.shape[1] != 3 ):
        print( "[calculate__tetraInOutRadius.py] illegal nodes shape :: {0} ".format( nodes.shape ) )
    nElems   = elems.shape[0]

    # ------------------------------------------------- #
    # --- [2] calculate  in-radius of the element   --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.calculate__tetraVolume   as ctv
    import nkMeshRoutines.calculate__tetraFaceArea as tfa
    volumes  = ctv.calculate__tetraVolume  ( elems=elems, nodes=nodes )
    areas    = tfa.calculate__tetraFaceArea( elems=elems, nodes=nodes )
    areas    = np.sum( areas, axis=1 )
    rinn     = 3.0 * volumes / areas
    
    # ------------------------------------------------- #
    # --- [3] calculate out-radius of the element   --- #
    # ------------------------------------------------- #
    nd0, nd1      = nodes[ elems[:,0]-1,:], nodes[ elems[:,1]-1,:]
    nd2, nd3      = nodes[ elems[:,2]-1,:], nodes[ elems[:,3]-1,:]
    vc1, vc2, vc3 = nd0-nd1, nd0-nd2, nd2-nd3
    matrix        = np.concatenate( [vc1[:,None,:],vc2[:,None,:],vc3[:,None,:]], axis=1 )
    norm_sub1     = np.sum(nd0**2,axis=1) - np.sum(nd1**2,axis=1)
    norm_sub2     = np.sum(nd0**2,axis=1) - np.sum(nd2**2,axis=1)
    norm_sub3     = np.sum(nd2**2,axis=1) - np.sum(nd3**2,axis=1)
    bvector       = np.concatenate( [ norm_sub1[:,None], norm_sub2[:,None], \
                                      norm_sub3[:,None], ], axis=1 )
    centers       = 0.5 * np.matmul( np.linalg.inv( matrix ), bvector[:,:,None] )
    centers       = np.reshape( centers, ( nElems, 3 ) )
    rout          = np.linalg.norm( nd0 - centers, axis=1 )
    
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( rinn, rout )

    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkMeshRoutines.load__nastranFile as lnf
    inpFile      = "msh/model.bdf"
    nodes, elems = lnf.load__nastranFile( inpFile=inpFile )
    elems        = np.copy( elems[:,2:] )
    
    rinn,rout    = calculate__tetraInOutRadius( elems=elems, nodes=nodes )
    aspect       = 3.0 * rinn / rout
    print( np.min( aspect ), np.max( aspect ) )





    
    # for iv,vert in enumerate( elems ):
    #     # -- [2-1] surface area -- #
    #     iv0,iv1,iv2,iv3 =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3 = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3,vc4 = nd1-nd0, nd2-nd0, nd1-nd3, nd2-nd3
    #     s1              = 0.5 * np.sum( ( np.cross( vc1, vc2 ) )**2 )
    #     s2              = 0.5 * np.sum( ( np.cross( vc1, vc3 ) )**2 )
    #     s3              = 0.5 * np.sum( ( np.cross( vc2, vc4 ) )**2 )
    #     s4              = 0.5 * np.sum( ( np.cross( vc3, vc4 ) )**2 )
    #     s_tetra         = s1 + s2 + s3 + s4
    #     # -- [2-2] volume       -- #
    #     vc1,vc2,vc3     = nd1-nd0, nd2-nd0, nd3-nd0
    #     matrix          = np.concatenate( [vc1[:,None],vc2[:,None],vc3[:,None]], axis=1 )
    #     v_tetra         = onesixth * np.linalg.det( matrix )
    #     # -- [2-3] in-radius    -- #
    #     innradii[iv]    = 3.0 * v_tetra / s_tetra


    # outradii = np.zeros( (nElems  ) )
    # centers  = np.zeros( (nElems,3) )
    # for iv,vert in enumerate( elems ):
    #     iv0,iv1,iv2,iv3 =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3 = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3     =    nd0 - nd1,    nd0 - nd2,    nd2 - nd3
    #     matrix          = np.concatenate( [vc1[None,:],vc2[None,:],vc3[None,:]], axis=0 )
    #     bvector         = np.array( [ np.sum(nd0**2) - np.sum(nd1**2), \
    #                                   np.sum(nd0**2) - np.sum(nd2**2), \
    #                                   np.sum(nd2**2) - np.sum(nd3**2)  ] )
    #     centers[iv,:]   = 0.5 * np.dot( np.linalg.inv( matrix ), bvector )
    #     outradii[iv]    = np.linalg.norm( nd0 - centers[iv,:] )
