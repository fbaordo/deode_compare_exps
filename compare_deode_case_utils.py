import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import metview as mv
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# add colots if needed (for hist plot)
colorList = ['k', 'b', 'r', 'g', 'm','y']

def get_accPrepFromGrib(grbFile,grbFile2):

    myFC = mv.read(grbFile) 
    myFC = mv.grib_set(myFC,["gridType",'lambert'])

    myFC2 = mv.read(grbFile2) 
    myFC2 = mv.grib_set(myFC2,["gridType",'lambert'])

    tirf2 = myFC2.select(shortName="tirf")
    tirf1 = myFC.select(shortName="tirf")

    tsnowp2 = myFC2.select(shortName="tsnowp")
    tsnowp1 = myFC.select(shortName="tsnowp")

    tgrp2 = myFC2.select(shortName="tgrp")
    tgrp1 = myFC.select(shortName="tgrp")

    tp2 = tirf2 + tsnowp2 + tgrp2
    tp1 = tirf1 + tsnowp1 + tgrp1

    acc_tp = tp2 - tp1
    
    myData  = acc_tp.to_dataset()
    varname = list(myData.keys())[0]

    strANtime    = str(myData.time.data)
    strValidTime = str(myData.valid_time.data)[0:13]
    strUnits     = str(myData[varname].attrs['units'])
    
    data2Plot = myData[varname].data
    mylat     = myData.latitude.data
    mylon     = myData.longitude.data

    
    return mylat, mylon, data2Plot, strValidTime, strUnits

def get_accPrepFromGrib_ec(grbFile,grbFile2):

    myFC = mv.read(grbFile) 
    myFC2 = mv.read(grbFile2) 
 
    tp2 = myFC2.select(shortName="tp")
    tp1 = myFC.select(shortName="tp")

    acc_tp = (tp2 - tp1)*1000.
    
    myData  = acc_tp.to_dataset()
    varname = list(myData.keys())[0]

    strANtime    = str(myData.time.data)
    strValidTime = str(myData.valid_time.data)[0:13]
    strUnits     = str(myData[varname].attrs['units'])    
    
    data2Plot = myData[varname].data
    mylat     = myData.latitude.data
    mylon     = myData.longitude.data

    return mylat, mylon, data2Plot, strValidTime,strUnits

def get_windSpeedFromGrib(grbFile):

    myFC = mv.read(grbFile) 
    myFC = mv.grib_set(myFC,["gridType",'lambert'])

    u_10m =  myFC.select(shortName='10u')
    v_10m =  myFC.select(shortName='10v')
    windSpeed = mv.sqrt(u_10m*u_10m + v_10m*v_10m)
    
    myWindSpeed  = windSpeed.to_dataset()
    varname = list(myWindSpeed.keys())[0]

    strANtime    = str(myWindSpeed.time.data)
    strValidTime = str(myWindSpeed.valid_time.data)[0:13]
    strUnits     = str(myWindSpeed[varname].attrs['units'])
    
    data2Plot = myWindSpeed[varname].data
    mylat     = myWindSpeed.latitude.data
    mylon     = myWindSpeed.longitude.data

    return mylat, mylon, data2Plot, strValidTime, strUnits

def get_windSpeedFromGrib_ec(grbFile):

    myFC = mv.read(grbFile) 

    u_10m =  myFC.select(shortName='10u')
    v_10m =  myFC.select(shortName='10v')
    windSpeed = mv.sqrt(u_10m*u_10m + v_10m*v_10m)
    
    myWindSpeed  = windSpeed.to_dataset()
    varname = list(myWindSpeed.keys())[0]

    strANtime    = str(myWindSpeed.time.data)
    strValidTime = str(myWindSpeed.valid_time.data)[0:13]
    strUnits     = str(myWindSpeed[varname].attrs['units'])
    
    data2Plot = myWindSpeed[varname].data
    mylat     = myWindSpeed.latitude.data
    mylon     = myWindSpeed.longitude.data

    return mylat, mylon, data2Plot, strValidTime, strUnits

def plot_compare_data(dataExps, latExps, lonExps, expsLabel, strUnitsExps, var, 
                      strValidTime, bbox, strAccPre,
                      figRowlNum, figColNum, figWidth, figHeight, 
                      pathDiagPlots, minmap=None, maxmap=None, stepmap=None,
                      minHist=None, maxHist=None, binHist=None):


    # plots are map plot for each experiment + 1 plot to compare histogram of values

    fig = plt.figure(figsize=(figWidth,figHeight),dpi=100)

    if var == 'accPrep':
        strSupTitle = var + '['+ strAccPre +'] - Valid time: ' + strValidTime
        strCmap = 'ocean_r'
    else:
        strSupTitle = var + ' - Valid time: ' + strValidTime
        strCmap = 'jet'
    
    plt.suptitle(strSupTitle, fontweight="bold", fontsize=16)

    # maps
    for nE in range(0,len(expsLabel)):

        data2Plot = dataExps[nE]
        mylat     = latExps[nE]
        mylon     = lonExps[nE]
        strExp    = expsLabel[nE]
        strUnit   = strUnitsExps[nE]

        eMin = str('{:.2f}'.format(np.nanmin(data2Plot)))
        eMax = str('{:.2f}'.format(np.nanmax(data2Plot)))
        eMean = str('{:.2f}'.format(np.nanmean(data2Plot)))
        eStd = str('{:.2f}'.format(np.nanstd(data2Plot)))        

        strTitle = strExp +   '\n min/max/mean/std: ' +  eMin +'/'+ eMax + '/' + eMean + '/' + eStd
        
        ax = plt.subplot(figRowlNum, figColNum, int(nE+1), projection=ccrs.PlateCarree())

        plt.title(strTitle, fontweight="bold")

        # default min/max for colorbar
        myMin = int(np.nanmin(data2Plot))
        myMax = int(np.nanmax(data2Plot))
        if (myMin + myMax) > 1:
            myStep = 1
        else:
            myStep = 0.5
    
        if minmap is not None: 
            myMin = int(minmap)
        
        if maxmap is not None: 
            myMax = int(maxmap)
        
        if stepmap is not None:
            myStep = int(stepmap)
        
        bounds = np.arange(myMin,myMax,myStep)

        im = plt.pcolormesh(mylon, mylat, data2Plot, 
                            transform=ccrs.PlateCarree(),cmap=strCmap, 
                            vmin=bounds[0], vmax=bounds[len(bounds)-1])                    
        ax.coastlines()
        ax.gridlines(draw_labels=["bottom", "left"])
        ax.set_extent(bbox, crs=ccrs.PlateCarree())
    
        cbar = plt.colorbar(im, location='bottom', boundaries=bounds,
                            ticks=bounds,extend='both',shrink=0.9, pad=0.06) 

        if var == 'accPrep':
            cbar.set_label('mm', rotation=0, labelpad=5, fontsize=10, fontweight="bold")
        else:
            cbar.set_label(strUnit, rotation=0, labelpad=5, fontsize=10, fontweight="bold")
            
    
    # histogram
    histMin     = 0  
    histMax     = 50 
    histBinSize = 0.5
    if minHist is not None: 
        histMin = minHist
    
    if maxHist is not None: 
        histMax = maxHist
    
    if binHist is not None:
        histBinSize = binHist    

    myBins = np.arange(histMin, histMax+histBinSize, histBinSize)
    bSize = str('{:.2f}'.format(histBinSize))

    ax = plt.subplot(figRowlNum, figColNum, int(len(expsLabel)+1))
    for nE in range(0,len(expsLabel)):

        data2Plot = dataExps[nE]
        strExp    = expsLabel[nE]
        plt.hist(np.ravel(data2Plot), bins=myBins, alpha=0.8, 
                 label=strExp, color=colorList[nE], histtype='step', density=False, linewidth=2)
        
    plt.grid(True)
    plt.ylabel('Frequency', fontsize=10, fontweight="bold")
    plt.xlabel('Bin size: ' + bSize, fontsize=10, fontweight="bold")
    plt.yscale('log')
    #plt.xlim([XminLim, XmaxLim])
    #plt.ylim([YminLim, YmaxLim])
    plt.legend()

    fig.tight_layout()
    
    # save plot
    if not os.path.exists(pathDiagPlots):
        os.makedirs(pathDiagPlots)
            
    myPng = 'compare.'+var+'.'+strValidTime+'.png'

    plotname = os.path.join(pathDiagPlots, myPng)    
    plt.savefig(plotname)

    print('****************************************************')
    print('Valid time: ' + strValidTime)
    print('Expr list: ' + str(expsLabel))
    print('Compare plot saved as: ' +plotname)
    print('****************************************************')

    plt.close()    

    return None



