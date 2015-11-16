#!/bin/bash

clear

# run for each fo these filenames
for filename in cfg0_1 cfg0_2 cfg0_3 cfg1 cfg2 cfg3 cfg4
do
	time bash run_one.sh $filename
done