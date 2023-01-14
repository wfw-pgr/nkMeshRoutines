import os, sys
import numpy  as np
import pandas as pd
import meshio
import nkMeshRoutines.load__meshio as mio
import nkUtilities.load__pointFile as lpf


# ========================================================= #
# ===  convert__withMeshIO                              === #
# ========================================================= #

def convert__withMeshIO( points=None, cells=None, cellData={}, pointData={}, replaceData=True, \
                         mshFile=None, cellDataFile=None, pointDataFile=None, outFile=None, \
                         elementType="tetra" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( ( points is None ) or ( cells is None ) ):
        if ( mshFile        is None ):
            print( "\033[31m" + "[convert__withMeshIO.py] mshFile  == ???   [ERROR]" + \
                   "\033[0m" )
            sys.exit()
        else:
            mesh_dict   = mio.load__meshio( mshFile=mshFile, elementType=elementType )
            cells       = [ ( elementType, mesh_dict["cells"] ) ]
            points      = mesh_dict["points"]
            if ( replaceData ):
                pass
            else:
                cellData    = {  **cellData, **( mesh_dict["cellData"]  ) }
                pointData   = { **pointData, **( mesh_dict["pointData"] ) }
    if ( outFile is None ):
        ext     = os.path.splitext( mshFile )
        outFile = mshFile.replace( ext, ".vtu" )
        
    # ------------------------------------------------- #
    # --- [2] load csv file                         --- #
    # ------------------------------------------------- #
    if ( cellDataFile is not None ):
        ext = os.path.splitext( cellDataFile )[1]
        if ( ext.lower() == ".csv" ):
            csvData_l  = pd.read_csv( cellDataFile )
            columns    = ( csvData_l.columns ).to_list()
            cellData_l = { clm:csvData_l[clm].to_numpy() for clm in columns }
            cellData   = { **cellData, **cellData_l }
        else:
            cellData_l = lpf.load__pointFile( inpFile=inpFile, returnType="dict" )
            cellData   = { **cellData, **cellData_l }

    if ( pointDataFile is not None ):
        ext = os.path.splitext( pointDataFile )[1]
        if ( ext.lower() == ".csv" ):
            csvData_l   = pd.read_csv( pointDataFile )
            columns     = ( csvData_l.columns ).to_list()
            pointData_l = { clm:csvData_l[clm].to_numpy() for clm in columns }
            pointData   = { **pointData, **pointData_l }
        else:
            pointData_l = lpf.load__pointFile( inpFile=inpFile, returnType="dict" )
            pointData   = { **pointData, **pointData_l }
            
    # ------------------------------------------------- #
    # --- [3] save mesh                             --- #
    # ------------------------------------------------- #
    for key in cellData.keys():
        if ( cellData[key].ndim == 1 ):
            cellData[key] = np.reshape( cellData[key], (1,-1) )
        else:
            cellData[key] = np.transpose( cellData[key] )

    wmesh = meshio.Mesh( points, cells, cell_data=cellData, point_data=pointData )
    wmesh.write( outFile )
    return( wmesh )
    
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    mshFile       = "msh/model.bdf"
    cellDataFile  = "dat/cellData.csv"
    outFile       = "msh/output.vtu"
    convert__withMeshIO( mshFile=mshFile, cellDataFile=cellDataFile, outFile=outFile )
    
