#!/bin/bash

module load ecmwf-toolbox

# Wrapper for running SICE pipeline
if [ $# -eq 3 ]; then
  sourcePath=$1
  gribFilesId=$2
  targetPath=$3  
else
   echo "ERROR: incorrect number of command line arguments!"  
   echo "Expected <sourcePath> <gribFilesId> <targetPath>>"
   exit 1
fi


if [[ ! -e $targetPath ]]; then
    mkdir -p $targetPath
fi

echo "*******************************************************"
echo "inputs to performe grib_copy"
echo "sourcePath is: $sourcePath"
echo "gribFilesId is: $gribFilesId"
echo "targetPath is: $targetPath"
echo "*******************************************************"

cd $sourcePath

for GRIB_IN in `ls ${gribFilesId}*` ; do

	echo "Input grib file: ${sourcePath}/${GRIB_IN}"
		
	# extract winds
        GRIB_OUT="surface_"${GRIB_IN}
	grib_copy -w shortName=tirf/tsnowp/tgrp/tp/unknown/10u/10v/10efg/10nfg/2t $GRIB_IN ${targetPath}/${GRIB_OUT}

	echo "--> grib_copy file:  ${targetPath}/${GRIB_OUT} "

done

