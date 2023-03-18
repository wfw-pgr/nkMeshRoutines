import os, sys
import numpy                       as np
import nkMeshRoutines.load__meshio as mio
import nkUtilities.save__pointFile as spf

# ========================================================= #
# ===  assign__materialProperty.py                      === #
# ========================================================= #

def assign__materialProperty( inpFile=None, propertyFile=None, elementType="tetra", \
                              matNumKey=None, outFile=None, names=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile      is None ): sys.exit( "[assign__materialProperty.py] inpFile      == ???" )
    if ( propertyFile is None ): sys.exit( "[assign__materialProperty.py] propertyFile == ???" )

    # ------------------------------------------------- #
    # --- [2] read files                            --- #
    # ------------------------------------------------- #
    mesh_dict   = mio.load__meshio( mshFile=inpFile, elementType=elementType )
    cells       = [ ( elementType, mesh_dict["cells"] ) ]
    points      = mesh_dict["points"]
    if ( matNumKey is not None ):
        physNums = mesh_dict["cellData"][matNumKey]
    else:
        if ( mesh_dict["physNums"] is not None ):
            physNums = mesh_dict["physNums"]
        else:
            print( "[assign__materialProperty.py] physNums == ??? " )
            sys.exit()
            
    # ------------------------------------------------- #
    # --- [3] assign material files                 --- #
    # ------------------------------------------------- #
    mat_ = 0
    import nkUtilities.load__pointFile as lpf
    properties    =   lpf.load__pointFile( inpFile=propertyFile, returnType="point" )
    if ( names is None ):
        names     = ( lpf.load__pointFile( inpFile=propertyFile, returnType="info"  ) )["names"]
    matNums       = properties[:,mat_]
    index         = np.argsort( properties[:,mat_] )
    properties    = properties[index]
    matNums_p     = np.array( properties[:,mat_], dtype=np.int64 )
    matNums_m     = np.array( physNums          , dtype=np.int64 )
    matNums_p_set = set( list( matNums_p ) )
    matNums_m_set = set( list( matNums_m ) )
    if ( matNums_m_set <= matNums_p_set ):
        matNums_set = list( matNums_p_set & matNums_m_set )
    else:
        print( "[assign__materialProperty.py] unknwon matNum exists.... " )
        print( "matNums_p_set :: ", matNums_p_set )
        print( "matNums_m_set :: ", matNums_m_set )
        print()
        sys.exit()

    # ------------------------------------------------- #
    # --- [4] assign material property              --- #
    # ------------------------------------------------- #
    propertyData = np.zeros( (matNums_m.shape[0],properties.shape[1]) )
    for ik,matNum in enumerate(matNums_set):
        index = np.where( matNums_m == matNum )
        propertyData[index,:] = properties[ik,:]
        
    # ------------------------------------------------- #
    # --- [5] save in a file                        --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        extention = ( outFile.split( "." ) )[-1]
        if   ( extention.lower() in [ "dat", "csv" ] ):
            spf.save__pointFile( outFile=outFile, Data=propertyData )
        elif ( extention.lower() in [ "vtu", "msh" ] ):
            import nkMeshRoutines.convert__withMeshIO as cwm
            cellData = { name:propertyData[:,ik] for ik,name in enumerate(names) }
            cwm.convert__withMeshIO( mshFile=inpFile, cellData=cellData, \
                                     outFile=outFile, elementType=elementType )
    return( propertyData )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile      = "test/model.msh"
    propertyFile = "test/property.conf"
    outFile      = "test/out2.vtu"
    names        = [ "matNum_add", "density_add", "specific_heat_add" ]
    assign__materialProperty( inpFile=inpFile, propertyFile=propertyFile, \
                              outFile=outFile, names=names )
