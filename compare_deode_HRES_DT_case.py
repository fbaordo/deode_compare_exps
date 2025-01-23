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
# 2024092600 - flooding - peak around 15 UTC on 27 Sep
# 2024121400 - storm - peak around midnight 20241216 

topPath = '/perm/miag/deode_exps'
anTime  = '2024112200'

expsList = ['CY46h1_HARMONIE_AROME_IRL_1500x1500_500m_v1',
            'CY48t3_ALARO_IRL_1500x1500_500m_v1',   #DT',
            'CY48t3_AROME_IRL_1500x1500_500m_v1', 'DT','HRES']

expsGribId = ['GRIBPFDEOD',
              'GRIBPFDEOD',
              'GRIBPFDEOD', 'DT','HRES']

expsLabel = ['CY46-HARMONIE-AROME',
             'CY48-ALARO',
             'CY48-AROME', 'DT','HRES']

#option: 'accPrep' 'windSpeed'
varsToComapre = ['accPrep'] 

# plots all time steps e.g. 1 to 48  
#fcSteps = np.arange(1,49,1)
#focus on  particular time steps
fcSteps = np.arange(48,49,1) 

# accumulated precipitation
strAccPre = '24h'
accPreStep = 24

# DK [18, 4, 52, 59]
bbox = [-2.5, -15.5, 48, 57]
 # figure (subplots= maps*expNum + 1)
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
                          minmap=1, maxmap=60, stepmap=4, minHist=-0.5, maxHist=160, binHist=1)
