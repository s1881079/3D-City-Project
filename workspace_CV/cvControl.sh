#!/bin/bash
# a general control for the pipeline

VENVACT=/home/s1881079/scratch/venv/bin/activate
CVWORKDIR=/home/s1881079/A_materials/dissertation/workspace_CV
MTCHWORKDIR=/home/s1881079/A_materials/dissertation/workspace_building

# =============================working on cv part 
cd $CVWORKDIR

# download images and store metaCSV(possibly writing results into memory)
python3 prepro_gsv.py

# change to vertual environment with google enginine installed
source $VENVACT

# object recognition process and storing metadata(writing to cam_pt)
python objrec_gsv.py

deactivate

#==============================working on matching part
cd $MTCHWORKDIR

#start matching process
python3 mtch_dbs.py
