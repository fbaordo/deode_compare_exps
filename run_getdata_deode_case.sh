#!/bin/bash

#SBATCH --qos=nf
#SBATCH --time=01:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=run_getdata_deode_case
#SBATCH -o sbatchlogs/run_getdata_deode_case_%j.out
#SBATCH -e sbatchlogs/run_getdata_deode_case_%j.err

#############################################################################################
# Prepare grib data before plotting
# ASSUMPTIONS:

# - deode experiments are expected in local folder on ATOS (!!! CHECK THE RIGHT LOCATION and configure properly 'sourcePath' below in the script)
#   sourcePath can be somenthing like: 
#         /scratch/${userID}/deode/${expID}/archive/${YYYY}/${MM}/${DD}/${HH}
#         /scratch/${userID}/DE_NWP/deode/${YYYY}/${MM}/${DD}/${HH}/flooding/1/${expID}  (new workflow output structure)

# - target path where to store data:
#   targetPath=/perm/${USER}/deode_exps/${YYYY}${MM}${DD}${HH}/${expID}

# - HRES/DT are retrieved using a MARS request
#############################################################################################

# Analysis time
YYYY=2025
MM=01
DD=27
HH=00

# expID (to identify sourcePath)
expIDList=(AROME_2000m  AROME_500m  HARMONIE_AROME_2000m  HARMONIE_AROME_500m)
# UserID (to identify sourcePath)
userID=nhad
# expected string in DEODE grib file
gribFilesId=GRIBPFDEOD+

# active what data you want to get 

# grib copy for DEODE grib files --> check deode_grib_copy.sh if you want to add other surface variables
gribCopy=FALSE
# HRES/DT MARS RETRIEVAL
getHRES=FALSE
getDT=TRUE

# if getHRES or getDT, configure below

# Minimize data retrieval for HRES/DT retrieve only requested FC time steps and over a specifc lat/lon AREA 
dtEXP=iekm
FC_TIME_STEP=(1 48) 

# AREA to retrieve
# North/West/South/East	latitude/longitude coordinates of sub-area
# DK=59/4/52/18
# IR=57/-15.5/48/-2.5
# NO=62.5/0/55.5/14
# IT= 41.28, 5.4, 48, 15.42
AREA=48/5.4/41.25/15.45

##########
# apply grib copy to original DEODE grib file
##########
if [[ ${gribCopy} == "TRUE" ]] ; then

																																	
   for expID in "${expIDList[@]}"; do

        #!!! CHECK THE RIGHT LOCATION
	#sourcePath=/scratch/${userID}/deode/${expID}/archive/${YYYY}/${MM}/${DD}/${HH}
	sourcePath=/scratch/${userID}/DE_NWP/deode/${YYYY}/${MM}/${DD}/${HH}/flooding/1/${expID}
	targetPath=/perm/${USER}/deode_exps/${YYYY}${MM}${DD}${HH}/${expID}
	./deode_grib_copy.sh ${sourcePath} ${gribFilesId} ${targetPath}

  done

fi

##########
# get HRES
##########
if [[ ${getHRES} == "TRUE" ]] ; then

	DATE=${YYYY}${MM}${DD}
	ANTIME=${HH}
	targetPath=/perm/${USER}/deode_exps/${YYYY}${MM}${DD}${HH}/HRES

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
	targetPath=/perm/${USER}/deode_exps/${YYYY}${MM}${DD}${HH}/DT

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
     PARAM=228.128,49.128/165.128/166.128/167.128/228.128,
     TARGET=$myTarget
EOF

	mars mars_${myTarget}.inp

	echo "File retrieved: $myTarget"
	echo "Saved to: ${targetPath}"
	rm mars_${myTarget}.inp
done #FCSTEPS

fi  # getHRES
