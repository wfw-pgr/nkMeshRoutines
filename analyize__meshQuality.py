import numpy                    as np
import nkUtilities.plot1D       as pl1
import nkUtilities.load__config as lcf


# ========================================================= #
# ===  analyze mesh Quality                             === #
# ========================================================= #

def analyze__meshQuality( indicator="rho", inpFile="dat/mesh_quality.dat", \
                          mshFile  =None , pngFile="png/mesh_quality.png", \
                          DataRange=None , nBins=50, normalize=True,  ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( mshFile is not None ):
        import nkMeshRoutines.assess__meshQuality as amq
        amq.assess__meshQuality( inpFile=mshFile, outFile=inpFile )
        
    # ------------------------------------------------- #
    # --- [2] load qualities                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data    = lpf.load__pointFile( inpFile=inpFile, returnType="point" )

    # ------------------------------------------------- #
    # --- [3] gmsh rho                              --- #
    # ------------------------------------------------- #
    title_table  = { "volume":"Volume", "area":"Face Area", "length":"Averaged Edge Length", \
                       "rho":r"$\rho$", "eta":r"$\eta$", "gamma":r"$\gamma$" }
    item_table   = { "volume":0, "area":1, "length":2, "rho":3, "eta":4, "gamma":5 }
    
    idx          = item_table[indicator]
    Data         = np.ravel( Data[:,idx] )

    if ( DataRange is None ):
        dmin, dmax = np.min( Data ), np.max( Data )
    
    # ------------------------------------------------- #
    # --- [4] make histogram                        --- #
    # ------------------------------------------------- #
    ret,bins = np.histogram( Data, bins=nBins, range=DataRange )
    if ( normalize ):
        ret  = ret / np.sum( ret )
    bins     = ( 0.5 * ( bins + np.roll( bins, +1 ) ) )[1:]
    xTitle   = title_table[indicator]
    
    config           = lcf.load__config()
    config["xTitle"] = xTitle
    config["yTitle"] = "Normalized Frequency"
    
    fig    = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__bar( xAxis=bins, yAxis=ret )
    fig.set__axis()
    fig.save__figure()



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    mshFile = "test/model.bdf"
    pngFile = "test/mesh_quality.png"
    datFile = "test/mesh_quality.dat"
    analyze__meshQuality( mshFile=mshFile, pngFile=pngFile, inpFile=datFile )
