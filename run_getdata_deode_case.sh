#!/bin/bash

#SBATCH --qos=np
#SBATCH --time=04:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH -o run_getdata_deode_case_%j.out
#SBATCH -e run_getdata_deode_case_%j.err
#SBATCH --job-name=run_getdata_deode_case

# Xiaohua
# 20240926 - flooding - peak around 15 UTC on 27 Sep
#/ec/res4/scratch/nhe/deode/CY46h1_HARMONIE_AROME_DAN_1500x1500_500m_v1/archive/2024/09/26/00
#/ec/res4/scratch/nhe/deode/CY46h1_HARMONIE_AROME_DAN_1500x1500_500m_v1/archive/2024/09/27/00

# 20241214 - storm - peak around midnight 20241216 
#/ec/res4/scratch/nhe/deode/CY46h1_HARMONIE_AROME_DAN_1500x1500_500m_v1/archive/2024/12/14/00
#/ec/res4/scratch/nhe/deode/CY46h1_HARMONIE_AROME_DAN_1500x1500_500m_v1/archive/2024/12/15/00

YYYY=2024
MM=11
DD=22
HH=00

expID=CY46h1_HARMONIE_AROME_IRL_1500x1500_500m_v1 #"CY48t3_ALARO_IRL_1500x1500_500m_v1  #CY48t3_AROME_IRL_1500x1500_500m_v1 #CY46h1_HARMONIE_AROME_DAN_1500x1500_500m_v1
userID=nhe

gribCopy=FALSE
getHRES=TRUE
getDT=TRUE
 
dtEXP=iekm
# retrieve some FC time steps
FC_TIME_STEP=(24 48)

# AREA to retrieve
# North/West/South/East	latitude/longitude coordinates of sub-area
# DK=59/4/52/18
AREA=57/-15.5/48/-2.5

##########
# apply grib copy to original DEODE grib file
##########
if [[ ${gribCopy} == "TRUE" ]] ; then
	sourcePath=/ec/res4/scratch/miag/${expID}   #/ec/res4/scratch/${userID}/deode/${expID}/archive/${YYYY}/${MM}/${DD}/${HH}
	gribFilesId=GRIBPFDEOD+
	targetPath=/perm/miag/deode_exps/${YYYY}${MM}${DD}${HH}/${expID}

	./deode_grib_copy.sh ${sourcePath} ${gribFilesId} ${targetPath}
fi

##########
# get HRES
##########
if [[ ${getHRES} == "TRUE" ]] ; then

	DATE=${YYYY}${MM}${DD}
	ANTIME=${HH}
	targetPath=/perm/miag/deode_exps/${YYYY}${MM}${DD}${HH}/HRES

	if [ ! -d "${archDir}" ] ; then
	  mkdir -p ${targetPath}
	fi
	
	cd ${targetPath}

for FCSTEP in ${FC_TIME_STEP[*]}
do

	myTarget=HRES_${DATE}${ANTIME}T${FCSTEP}.grb

	# 228.128 tp - total precipitation
        # 49.128 10fg - Maximum 10 metre wind gust since previous post-processing
	# 165.128 10u
        # 166.128 10v
        # 167.128 2t
	cat > mars_${myTarget}.inp << EOF

RETRIEVE,
     STREAM=oper,
     CLASS=od,
     EXPVER=1,
     AREA=${AREA},
     GRID=0.1/0.1,
     DATE=${DATE},
     TIME=${ANTIME},
     STEP=${FCSTEP},
     TYPE=FC,
     LEVTYPE=SFC,
     PARAM=49.128/165.128/166.128/167.128/228.128,
     TARGET=$myTarget
EOF

	mars mars_${myTarget}.inp

	echo "File retrieved: $myTarget"
	echo "Saved to: ${targetPath}"
	rm mars_${myTarget}.inp
done #FCSTEPS

fi  # getHRES

##########
# get DT
##########
if [[ ${getDT} == "TRUE" ]] ; then

	DATE=${YYYY}${MM}${DD}
	ANTIME=${HH}
	targetPath=/perm/miag/deode_exps/${YYYY}${MM}${DD}${HH}/DT

	if [ ! -d "${archDir}" ] ; then
	  mkdir -p ${targetPath}
	fi
	
	cd ${targetPath}

for FCSTEP in ${FC_TIME_STEP[*]}
do

	myTarget=DT_${DATE}${ANTIME}T${FCSTEP}.grb

	# 228.128 tp - total precipitation
        # 49.128 10fg - Maximum 10 metre wind gust since previous post-processing
	# 165.128 10u
        # 166.128 10v
        # 167.128 2t
	cat > mars_${myTarget}.inp << EOF

RETRIEVE,
     STREAM=oper,
     CLASS=rd,
     EXPVER=${dtEXP},
     AREA=${AREA},
     GRID=0.05/0.05,
     DATE=${DATE},
     TIME=${ANTIME},
     STEP=${FCSTEP},
     TYPE=FC,
     LEVTYPE=SFC,
     PARAM=49.128/165.128/166.128/167.128/228.128,
     TARGET=$myTarget
EOF

	mars mars_${myTarget}.inp

	echo "File retrieved: $myTarget"
	echo "Saved to: ${targetPath}"
	rm mars_${myTarget}.inp
done #FCSTEPS

fi  # getHRES
