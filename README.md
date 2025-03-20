# deode_compare_exps
Some scripts to prepare data from DEODE exps and compare against DT/HRES.

- prepare data using run_getdata_deode_case.sh: configure and run ('sbatch run_getdata_deode_case.sh') to extract a) desidered variables from DEODE grib files (by means of grib_copy implemented in deode_grib_copy.sh) b) retrieved HRES and/or DT from MARS (MARS requested is configurable in run_getdata_deode_case.sh)

- after data has been prepared, plot using compare_deode_HRES_DT_case.py: configure and run compare_deode_HRES_DT_case.py (plot functions are implemented in compare_deode_case_utils.py). Variables that can be compared: 'accPrep' (selecting accumulated time) & 'windSpeed' (10m wind speed). More to add...
