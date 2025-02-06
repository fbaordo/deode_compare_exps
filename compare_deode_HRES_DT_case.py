import os
import numpy as np
import sys

from compare_deode_case_utils import get_accPrepFromGrib, get_accPrepFromGrib_ec, \
get_windSpeedFromGrib, get_windSpeedFromGrib_ec, plot_compare_data

import warnings
warnings.filterwarnings('ignore')

#########################
# configure case
#########################
# 2024092600 - flooding DK - peak around 15 UTC on 27 Sep
# 2024121400 - storm DK - peak around midnight 20241216 
# 2024120400 - Roger Norway case 

# - deode experiments/HRES/DT grib files are expected in local folder on ATOS:
#   /perm/${USER}/deode_exps/${YYYY}${MM}${DD}${HH}/${expID}

# top path
topPath = '/perm/miag/deode_exps'

# Analysis time (YYYYMMDDHH)
anTime  = '2024120400'

# expID list
expsList = ['CY46h1_HARMONIE_AROME_nwp_NOR_20241204_500morig_20241204',
            'CY46h1_HARMONIE_AROME_nwp_NOR_20241204_1000m_20241204',   
            'HRES']

# GribId List for each experiment in expsList
expsGribId = ['GRIBPFDEOD',
              'GRIBPFDEOD',
              'HRES']

# Label for each experiment in expsList 
expsLabel = ['LAM 500m',
             'LAM 1000m',
             'Global 9000m']

#Seelct variable to plot, Available: 'accPrep' 'windSpeed'
varsToComapre = ['windSpeed'] 

# Select time steps to plots ('target valid time') 
# plots all time steps e.g. 1 to 48 --> fcSteps = np.arange(1,49,1)
# aotherwise, focus on  particular time steps
fcSteps = np.arange(48,49,1) 

# Only for accumulated precipitation
strAccPre = '24h'
accPreStep = 24

# Lat/Lon Domain
# DK [18, 4, 52, 59]
# IR [-2.5, -15.5, 48, 57]
# NO [0, 14, 55.5, 62.5]
bbox = [0, 14, 55.5, 62.5]

# figure (subplots= maps*expNum + 2) additional 2 plots: histogram + boxplot
figRowlNum = 2 
figColNum = 3
figWidth  = 16 
figHeight = 12
#################################

pathDiagPlots = os.path.join(topPath, anTime, 'compareExp')  

#get data from experiemnts

# loop over fc steps to plots
for fcStep in fcSteps:

    if fcStep < 10:
        strfcStep = '0'+str(fcStep)
    else:
        strfcStep = str(fcStep)
    
    dataExps = []
    latExps  = []
    lonExps  = []
    strUnitsExps = []
    # loop over var to comapre
    for var in varsToComapre:

        for index, strExp in enumerate(expsList):    

            gribId = expsGribId[index]
            
            if strExp != 'DT' and strExp != 'HRES': 
                grbFileName = 'surface_{0}+00{1}h00m00s'.format(gribId,strfcStep)
            else:
                grbFileName = '{0}_{1}T{2}.grb'.format(gribId,anTime,strfcStep)

            grbFile = os.path.join(topPath, anTime, strExp, grbFileName)

            if not os.path.exists(grbFile):
                print('ERROR: grib file: {0} not found!'.format(grbFile))
                sys.exit(1)
                
            print('grib file: {0}'.format(grbFile))

            #############################
            # get the other grib files
            #############################
            if var == 'accPrep':
                
                fcStepLenght = fcStep - accPreStep
                
                if fcStepLenght < 10:
                    strfcStepLenght = '0'+str(fcStepLenght)
                else:
                    strfcStepLenght = str(fcStepLenght)

                if strExp != 'DT' and strExp != 'HRES': 
                    grbFileNameAcc = 'surface_{0}+00{1}h00m00s'.format(gribId,strfcStepLenght)
                else:
                    grbFileNameAcc = '{0}_{1}T{2}.grb'.format(gribId,anTime,strfcStepLenght)
                
                grbFileAcc = os.path.join(topPath, anTime, strExp, grbFileNameAcc)

                if not os.path.exists(grbFileAcc):
                    print('ERROR: grib file for accumulated prec: {0} not found!'.format(grbFileAcc))
                    sys.exit(1)

                print('grib file for accumulated prec: {0}'.format(grbFileAcc))

                # now get data for each exp
                if strExp != 'DT' and strExp != 'HRES': 
                    mylat, mylon, data2Plot, \
                    strValidTime, strUnits = get_accPrepFromGrib(grbFileAcc,grbFile)                    
                    dataExps.append(data2Plot)
                    latExps.append(mylat)
                    lonExps.append(mylon)                    
                    strUnitsExps.append(strUnits)
                    print(' -->  got {0} data for deode exp, strValidTime {1}'.format(var,strValidTime))
                else:
                    mylat, mylon, data2Plot, \
                    strValidTime, strUnits = get_accPrepFromGrib_ec(grbFileAcc,grbFile)
                    dataExps.append(data2Plot)
                    latExps.append(mylat)
                    lonExps.append(mylon)
                    strUnitsExps.append(strUnits)                    
                    print(' --> got {0} data for DT/HRES, strValidTime {1}'.format(var,strValidTime))
                    
            else:
                # now get data for each exp
                if strExp != 'DT' and strExp != 'HRES': 
                    mylat, mylon, data2Plot, \
                    strValidTime, strUnits = get_windSpeedFromGrib(grbFile)
                    dataExps.append(data2Plot)
                    latExps.append(mylat)
                    lonExps.append(mylon)
                    strUnitsExps.append(strUnits)                     
                    print(' -->  got {0} data for deode exp, strValidTime {1}'.format(var,strValidTime))
                else:                    
                    mylat, mylon, data2Plot, \
                    strValidTime, strUnits = get_windSpeedFromGrib_ec(grbFile)
                    dataExps.append(data2Plot)
                    latExps.append(mylat)
                    lonExps.append(mylon)
                    strUnitsExps.append(strUnits)                                         
                    print(' --> got {0} data for DT/HRES, strValidTime {1}'.format(var,strValidTime))

        
        #do plot for experimets
        plot_compare_data(dataExps, latExps, lonExps, expsLabel, strUnitsExps, var, 
                          strValidTime, bbox, strAccPre, 
                          figRowlNum, figColNum, figWidth, figHeight, pathDiagPlots,
                          minmap=1, maxmap=26, stepmap=2, minHist=-0.5, maxHist=25, binHist=1)
