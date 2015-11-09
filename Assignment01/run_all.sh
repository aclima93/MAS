#!/bin/bash

clear

# run for each fo these filenames
for filename in cfg0 cfg1 cfg2 cfg3 cfg4
do
	time bash run_one.sh $filename
done