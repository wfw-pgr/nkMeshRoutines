import numpy as np
import os, sys
import gmsh

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__geometry( dimtags={} ):

    table   = { "circle.01": { "geometry_type":"circle", "centering":False, \
                               "xc":0.0, "yc":0.0, "zc":0.0, "rc":1.0 }, \
    }
    import nkGmshRoutines.geometrize__fromTable as gft
    dimtags = gft.geometrize__fromTable( table=table, dimtags=dimtags )
    return( dimtags )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] initialization of the gmsh            --- #
    # ------------------------------------------------- #
    gmsh.initialize()
    gmsh.option.setNumber( "General.Terminal", 1 )
    gmsh.option.setNumber( "Mesh.Algorithm"  , 5 )
    gmsh.option.setNumber( "Mesh.Algorithm3D", 4 )
    gmsh.option.setNumber( "Mesh.SubdivisionAlgorithm", 0 )
    gmsh.model.add( "model" )
    
    # ------------------------------------------------- #
    # --- [2] Modeling                              --- #
    # ------------------------------------------------- #
    sample__model = "make"     #  -- [ "import" / "make" ] --  #

    if   ( sample__model == "import" ):
        dimtagsFile = None
        stpFile     = "test/model.stp"
        import nkGmshRoutines.import__stepFile as isf
        dimtags     = isf.import__stepFile( inpFile=stpFile, dimtagsFile=dimtagsFile )
        
    elif ( sample__model == "make"   ):
        dimtags = {}
        dimtags = make__geometry( dimtags=dimtags )
        gmsh.model.occ.synchronize()
    
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = False         # from nkGMshRoutines/test/mesh.conf, phys.conf
    uniform_size     = 0.080
    if ( mesh_from_config ):
        meshFile = "dat/mesh.conf"
        physFile = "dat/phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, dimtags=dimtags )
    else:
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( uniform=uniform_size, dimtags=dimtags )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "test/poleSurface_2d.msh" )
    gmsh.finalize()

