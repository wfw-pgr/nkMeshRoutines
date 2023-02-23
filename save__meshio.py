import os, sys, meshio
import numpy as np


# ========================================================= #
# ===  save__meshio.py                                  === #
# ========================================================= #

def save__meshio( outFile=None, elems=None, nodes=None, elementType=None, \
                  file_format="gmsh" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( elems   is None ): print( "[save__meshio.py] elems   == ??? " )
    if ( nodes   is None ): print( "[save__meshio.py] nodes   == ??? " )
    if ( outFile is None ): print( "[save__meshio.py] outFile == ??? " )
    if ( elementType is None ): print( "[save__meshio.py] elementType == ??? " )
    
    # ------------------------------------------------- #
    # --- [2] save in a file                        --- #
    # ------------------------------------------------- #
    cells = { elementType: elems }
    wmesh = meshio.Mesh( nodes, cells )
    wmesh.write( outFile, file_format=file_format )
    print( "[save__meshio.py] output File :: {} ".format( outFile ) )

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    save__meshio()

    
