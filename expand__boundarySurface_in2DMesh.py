import os, sys, meshio
import numpy as np

# ========================================================= #
# ===  expand boundary surface outward                  === #
# ========================================================= #
def expand__boundarySurface_in2DMesh( elems=None, nodes=None, expandRate=0.50, \
                                      inpFile=None, outFile=None, file_format="gmsh" ):

    # -- return value :: [ ( element #. , pair( node #. in element ) ) ]
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( ( elems is None ) or ( nodes is None ) ):
        if ( inpFile is None ):
            sys.exit( "[expand__boudarySurface_in2DMesh.py] elems == ???" )
        else:
            import nkMeshRoutines.load__meshio as mio
            elems, nodes = mio.load__meshio( mshFile=inpFile, elementType="triangle", \
                                             returnType="elem-node" )

    # ------------------------------------------------- #
    # --- [2] detect boundary Line                  --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.detect__boundaryLine_in2DMesh as dbl
    boundaryLines = dbl.detect__boundaryLine_in2DMesh( elems=elems, nodes=nodes )

    # ------------------------------------------------- #
    # --- [3] modify nodes                          --- #
    # ------------------------------------------------- #
    for iE, pair in boundaryLines:
        remain       = int( list( set( [0,1,2] ) - set( pair ) )[0] )
        p1, p2       = pair[0], pair[1]
        iN0, iN1,iN2 = elems[iE,remain], elems[iE,p1], elems[iE,p2]        # --  node #.
        nodes[iN1,:] = ( nodes[iN1,:] - nodes[iN0,:] ) * expandRate + nodes[iN1,:]
        nodes[iN2,:] = ( nodes[iN2,:] - nodes[iN0,:] ) * expandRate + nodes[iN2,:]

    # ------------------------------------------------- #
    # --- [4] save in a file                        --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        elems = { "triangle": elems }
        wmesh = meshio.Mesh( nodes, elems )
        wmesh.write( outFile, file_format=file_format )
        print( "[expand__boundarySurface_in2DMesh.py] output File :: {} ".format( outFile ) )
        
    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    return( nodes, elems )

        
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    inpFile   = "test/poleSurface_3d.msh"
    outFile   = "test/poleSurface_3d_expanded.msh"
    elem_nums = expand__boundarySurface_in2DMesh( inpFile=inpFile, outFile=outFile )
    print( elem_nums )
