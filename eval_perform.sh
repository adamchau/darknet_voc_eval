#!/bin/bash
source activate test_py2
python reval_voc.py --voc_dir ../data/walker_detec --year 2007 --image_set test --class ../data/voc.names .|tee ./perform_logs/perform_`date +%F_%H-%M`.log
