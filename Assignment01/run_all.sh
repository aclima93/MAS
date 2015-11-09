#!/bin/bash

clear

# delete the previous results
rm -r temp/*
rm -r outputs/*

# run for each fo these filenames
for filename in cfg0 cfg1 cfg2 cfg3 cfg4
do
	bash run_one.sh $filename
done