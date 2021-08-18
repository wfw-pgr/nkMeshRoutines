import sys
import numpy as np

# ========================================================= #
# ===  edge Detectection for 2D triangulated mesh       === #
# ========================================================= #
def extract__edgeFrom2DMesh( elems=None, elemFile=None ):

    #  -- for 2D triangular mesh (201) contents are below :: --  #
    #   - 0   :: element Number     - #
    #   - 1   :: element Type (201) - #
    #   - 2   :: material Num       - #
    #   - 3-5 :: vertex Node Num    - #
    num_, typ_, mat_, vt1_, vt2_, vt3_ = 0, 1, 2, 3, 4, 5

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( elems    is None ):
        if ( elemFile is None ):
            sys.exit( "[edgeDetect2D] elems == ???, elemFile == ???" )
        else:
            with open( elemFile, "r" ) as f:
                elems = np.loadtxt( f, dtype=np.int )

    # ------------------------------------------------- #
    # --- [2] Extract Edges                         --- #
    # ------------------------------------------------- #
    #  -- [2-1] count appearance times of the line  --  #
    nElems   = elems.shape[0]
    lineDict = {}
    for iE in range( nElems ):
        for va, vb in [ (vt1_,vt2_), (vt2_,vt3_), (vt3_,vt1_) ]:
            # minv / maxv :: lower / higher value of the node, 
            minv, maxv = min( elems[iE,va], elems[iE,vb] ), max( elems[iE,va], elems[iE,vb] )
            hlinekey   = "line_p{0}_p{1}".format( minv, maxv )
            if  ( not( hlinekey in lineDict ) ):
                lineDict[hlinekey] = { "minv":minv, "maxv":maxv, "count":0 }
            lineDict[hlinekey]["count"] += 1

    #  -- [2-2] Find lines whose count is 1 --  #
    #  -- if the used count >= 2, the line is not edge -- #
    edgeLines = []
    for hkey in lineDict.keys():
        if ( lineDict[hkey]["count"] == 1 ):
            edgeLines.append( [ int( lineDict[hkey]["minv"] ), int( lineDict[hkey]["maxv"] ) ] )

            
    # ------------------------------------------------- #
    # --- [3] reordering                            --- #
    # ------------------------------------------------- #
    nLines      = len( edgeLines )
    stack       = [ edgeLines.pop() ]
    while( len( edgeLines ) > 0 ):
        target      = stack[-1][1]
        for ik,edge in enumerate( edgeLines ):
            if   ( edge[0] == target ):
                stack.append( [edge[0],edge[1]] )
                edgeLines.pop(ik)
                break
            elif ( edge[1] == target ):
                stack.append( [edge[1],edge[0]] )
                edgeLines.pop(ik)
                break

    if ( len( stack ) != nLines ):
        print( len(stack), nLines )
        sys.exit( "[edgeDetect2D] not closed line loop  ***ERROR*** :: reordering failed !!" )

    return( stack )


# ======================================== #
# ===  テスト用実行部                  === #
# ======================================== #
if ( __name__=="__main__" ):

    elemFile  = "test/mesh.elements"
    with open( elemFile, "r" ) as f:
        elems = np.loadtxt( f )
    edgeLines = extract__edgeFrom2DMesh( elems=elems )
    print( edgeLines )
    
    nodeFile  = "test/mesh.nodes"
    with open( nodeFile, "r" ) as f:
        node = np.loadtxt( f )
    n_, s_, x_, y_, z_ = 0, 1, 2, 3, 4

    import nkUtilities.plot1D as pl1
    import matplotlib.cm      as cm
    nL  = len(edgeLines)
    fig = pl1.plot1D( pngFile="out.png" )
    for ik,pts in enumerate( edgeLines ):
        iL1,iL2 = pts[0], pts[1]
        xpos    = np.array( [ node[iL1-1,x_], node[iL2-1,x_] ] )
        ypos    = np.array( [ node[iL1-1,y_], node[iL2-1,y_] ] )
        fig.add__plot( xpos, ypos, color=cm.jet( ik/nL ) )
    fig.set__axis()
    fig.save__figure()
