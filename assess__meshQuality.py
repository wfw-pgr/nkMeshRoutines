import numpy as np


# ========================================================= #
# ===  assess__meshQuality                              === #
# ========================================================= #

def assess__meshQuality( nodes=None, elems=None, inpFile=None, \
                         outFile="dat/mesh_quality.dat" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( ( nodes is None ) or ( elems is None ) ):
        if ( inpFile is not None ):
            import load__nastranFile as inf
            nodes, elems = inf.load__nastranFile( inpFile=inpFile )
        else:
            sys.exit( "[assess__meshQuality.py] nodes, elems = None, inpFile = None " )
    nElems = elems.shape[0]

    print()
    print( "[assess__meshQuality.py] Begin Mesh Quality Assessment... " )
    print()

    elems_    = np.copy( elems[:,2:] )
    
    # ------------------------------------------------- #
    # --- [2] volume / area / lengeh evaluation     --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.calculate__tetraVolume     as ctv
    import nkMeshRoutines.calculate__tetraFaceArea   as tfa
    import nkMeshRoutines.calculate__tetraEdgeLength as tel
    volumes    = ctv.calculate__tetraVolume    ( elems=elems_, nodes=nodes )
    faceArea   = tfa.calculate__tetraFaceArea  ( elems=elems_, nodes=nodes )
    length     = tel.calculate__tetraEdgeLength( elems=elems_, nodes=nodes )
    faceArea   = np.sum    ( faceArea, axis=1 )
    length_avg = np.average( length  , axis=1 )
    print( "[assess__meshQuality.py] calculated Volume / Area / Length " )

    # ------------------------------------------------- #
    # --- [3] rho: ratio of inradius & circumradius --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.calculate__tetraInOutRadius as ior
    rinn,rout = ior.calculate__tetraInOutRadius( elems=elems_, nodes=nodes )
    rho       = 3.0 * rinn / rout
    print( "[assess__meshQuality.py] calculated rho " )

    # ------------------------------------------------- #
    # --- [4] eta: vol^(2/3) / sum( length^2 )      --- #
    # ------------------------------------------------- #
    eta = volumes**( 2./3. ) / np.sum( length**2, axis=1 )
    print( "[assess__meshQuality.py] calculated eta" )

    # ------------------------------------------------- #
    # --- [5] gamma: vol/sum(S_face)/max(li)        --- #
    # ------------------------------------------------- #
    gamma = volumes / faceArea / np.max( length, axis=1 )
    print( "[assess__meshQuality.py] calculated gamma" )


    # ------------------------------------------------- #
    # --- [6] save in a file                        --- #
    # ------------------------------------------------- #
    print()
    print( "[assess__meshQuality.py] saving Data..." )
    names   = [ "volume", "area", "length", "rho", "eta", "gamma" ]
    Data    = np.concatenate( [ volumes[:,None], faceArea[:,None], length_avg[:,None], \
                                rho[:,None]    , eta     [:,None], gamma     [:,None] ], axis=1 )
    
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=outFile, Data=Data, names=names )
    print()
    return( Data )

    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    assess__meshQuality( inpFile="msh/model.bdf" )





    # ------------------------------------------------- #
    # --- [4] gamma :: volume / edge length         --- #
    # ------------------------------------------------- #
    # edge_length = np.zeros( (nElems  ) )
    # for iv,vert in enumerate( elems_ ):
    #     iv0,iv1,iv2,iv3 =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3 = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3     = nd1-nd0, nd2-nd0, nd3-nd0
    #     vc4,vc5,vc6     = nd2-nd1, nd3-nd1, nd3-nd2
    #     edge_length[iv] = np.sum( vc1**2 ) + np.sum( vc2**2 ) + np.sum( vc3**2 ) \
    #         +             np.sum( vc4**2 ) + np.sum( vc5**2 ) + np.sum( vc6**2 )
    # gamma     = volumes / edge_length**(1.5)
    # print( "[assess__meshQuality.py] calculated gamma " )
    # print()

    # ------------------------------------------------- #
    # --- [5] aspect ratio :: max(li) / min(lj)     --- #
    # ------------------------------------------------- #
    # aspect_ratio = np.zeros( (nElems  ) )
    # for iv,vert in enumerate( elems_ ):
    #     iv0,iv1,iv2,iv3  =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3  = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3      = nd1-nd0, nd2-nd0, nd3-nd0
    #     vc4,vc5,vc6      = nd2-nd1, nd3-nd1, nd3-nd2
    #     l1 ,l2 ,l3       = np.linalg.norm(vc1), np.linalg.norm(vc2), np.linalg.norm(vc3)
    #     l4 ,l5 ,l6       = np.linalg.norm(vc4), np.linalg.norm(vc5), np.linalg.norm(vc6)
    #     length           = np.array( [ l1,l2,l3,l4,l5,l6 ] )
    #     aspect_ratio[iv] = np.max( length ) / np.min( length )
    # print( "[assess__meshQuality.py] calculated aspect ratio " )
    # print()

    # ------------------------------------------------- #
    # --- [6] gmsh rho: min(lj) / max(li)           --- #
    # ------------------------------------------------- #
    # gmsh_rho = np.zeros( (nElems  ) )
    # for iv,vert in enumerate( elems_ ):
    #     iv0,iv1,iv2,iv3  =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3  = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3      = nd1-nd0, nd2-nd0, nd3-nd0
    #     vc4,vc5,vc6      = nd2-nd1, nd3-nd1, nd3-nd2
    #     l1 ,l2 ,l3       = np.linalg.norm(vc1), np.linalg.norm(vc2), np.linalg.norm(vc3)
    #     l4 ,l5 ,l6       = np.linalg.norm(vc4), np.linalg.norm(vc5), np.linalg.norm(vc6)
    #     length           = np.array( [ l1,l2,l3,l4,l5,l6 ] )
    #     gmsh_rho[iv]     = np.min( length ) / np.max( length )
    # print( "[assess__meshQuality.py] calculated rho(gmsh) " )
    # print()
        
    # gmsh_eta = np.zeros( (nElems  ) )
    # for iv,vert in enumerate( elems_ ):
    #     iv0,iv1,iv2,iv3  =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3  = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3      = nd1-nd0, nd2-nd0, nd3-nd0
    #     vc4,vc5,vc6      = nd2-nd1, nd3-nd1, nd3-nd2
    #     edge_length[iv]  = np.sum( vc1**2 ) + np.sum( vc2**2 ) + np.sum( vc3**2 ) \
    #         +              np.sum( vc4**2 ) + np.sum( vc5**2 ) + np.sum( vc6**2 )

    
    # # ------------------------------------------------- #
    # # --- [8] gmsh gamma: vol/sum(S_face)/max(li)   --- #
    # # ------------------------------------------------- #
    # gmsh_gamma = np.zeros( (nElems  ) )
    # for iv,vert in enumerate( elems_ ):
    #     iv0,iv1,iv2,iv3  =    vert[0]-1,    vert[1]-1,    vert[2]-1,    vert[3]-1
    #     nd0,nd1,nd2,nd3  = nodes[iv0,:], nodes[iv1,:], nodes[iv2,:], nodes[iv3,:]
    #     vc1,vc2,vc3      = nd1-nd0, nd2-nd0, nd3-nd0
    #     vc4,vc5,vc6      = nd2-nd1, nd3-nd1, nd3-nd2
    #     l1 ,l2 ,l3       = np.linalg.norm(vc1), np.linalg.norm(vc2), np.linalg.norm(vc3)
    #     l4 ,l5 ,l6       = np.linalg.norm(vc4), np.linalg.norm(vc5), np.linalg.norm(vc6)
    #     length           = np.array( [ l1,l2,l3,l4,l5,l6 ] )
    #     gmsh_gamma[iv]   = np.max( length )
    # gmsh_gamma = volumes / faceArea / gmsh_gamma


