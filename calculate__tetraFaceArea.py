import numpy as np


# ========================================================= #
# ===  calculate face area of a tetrahedral element     === #
# ========================================================= #

def calculate__tetraFaceArea( elems=None, nodes=None, index_from_one=False ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( elems is None ): sys.exit( "[calculate__tetraFaceArea.py] elems == ???" )
    if ( nodes is None ): sys.exit( "[calculate__tetraFaceArea.py] nodes == ???" )

    # - elems :: [ node1, node2, node3, node4 ] :: [ nElems, 4 ]
    # - nodes :: [ x, y, z ]                    :: [ nNodes, 3 ]
    if ( elems.shape[1] != 4 ):
        print( "[calculate__tetraFaceArea.py] illegal elems shape :: {0} ".format( elems.shape ) )
    if ( nodes.shape[1] != 3 ):
        print( "[calculate__tetraFaceArea.py] illegal nodes shape :: {0} ".format( nodes.shape ) )

    # ------------------------------------------------- #
    # --- [2] index from 1 / 0                      --- #
    # ------------------------------------------------- #
    if ( index_from_one ):
        elems[:,:] = elems[:,:] - 1
        
    # ------------------------------------------------- #
    # --- [2] calculate  in-radius of the element   --- #
    # ------------------------------------------------- #
    nd0, nd1      = nodes[ elems[:,0],:], nodes[ elems[:,1],:]
    nd2, nd3      = nodes[ elems[:,2],:], nodes[ elems[:,3],:]
    vc1, vc2      = nd1-nd0, nd2-nd0
    vc3, vc4      = nd1-nd3, nd2-nd3
    face1         = 0.5 * np.sqrt( np.sum( ( np.cross( vc3, vc4 ) )**2, axis=1 ) )
    face2         = 0.5 * np.sqrt( np.sum( ( np.cross( vc2, vc4 ) )**2, axis=1 ) )
    face3         = 0.5 * np.sqrt( np.sum( ( np.cross( vc1, vc3 ) )**2, axis=1 ) )
    face4         = 0.5 * np.sqrt( np.sum( ( np.cross( vc1, vc2 ) )**2, axis=1 ) )
    area          = np.concatenate( [face1[:,None],face2[:,None],\
                                     face3[:,None],face4[:,None]], axis=1 )

    # ------------------------------------------------- #
    # --- [3] return                                --- #
    # ------------------------------------------------- #
    return( area )

    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkMeshRoutines.load__nastranFile as lnf
    inpFile      = "msh/model.bdf"
    nodes, elems = lnf.load__nastranFile( inpFile=inpFile )
    elems        = np.copy( elems[:,2:] )
    
    area         = calculate__tetraFaceArea( elems=elems, nodes=nodes )
    averaged     = np.average( np.sum( area, axis=1 ) )
    print()
    print( "[calculate__tetraFaceArea] averaged area :: {0} ".format( averaged )  )
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
