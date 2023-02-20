import numpy as np
import os, sys
import gmsh

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__geometry( dimtags={} ):

    table   = { "circle01": { "geometry_type":"circle", \
                              "xc":0.0, "yc":0.0, "zc":0.0, "rc":0.5 }, \
                "quad01"  : { "geometry_type":"quad", \
                              "x0":-0.6, "y0":-0.6, "z0":0.0, "dx":1.2, "dy":1.2, "dz":0.0 }, 
                "quad02"  : { "boolean_type":"cut", \
                              "targetKeys":["quad01"], "toolKeys":["circle01"], "removeObject":True, "removeTool":False }
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
        stpFile     = "msh/model.stp"
        import nkGmshRoutines.import__stepFile as isf
        dimtags     = isf.import__stepFile( inpFile=stpFile, dimtagsFile=dimtagsFile )
        
    elif ( sample__model == "make"   ):
        dimtags = {}
        dimtags = make__geometry( dimtags=dimtags )
        gmsh.model.occ.synchronize()
    print( dimtags )
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()
    
    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = True         # from nkGMshRoutines/test/mesh.conf, phys.conf
    uniform_size     = 0.1
    if ( mesh_from_config ):
        meshFile = "test/mesh_circle.conf"
        physFile = "test/phys_circle.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, \
                                       dimtags=dimtags, target="surf" )
    else:
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( uniform=uniform_size, dimtags=dimtags )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write( "test/circle.msh" )
    gmsh.finalize()

