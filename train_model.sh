#!/bin/bash
../darknet detector train voc.data yolov3-voc-walker.cfg backup/yolov3-voc-walker.backup|tee train.log
