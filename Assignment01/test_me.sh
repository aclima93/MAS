#!/bin/bash

# common filename to be used
filename="cfg0"

# delete the previous results
rm -r temp/*
rm -r "outputs/"$filename"_spp_output.dat"
rm -r "outputs/"$filename"_cycles_output.dat"

echo "Running for "$filename"..."

# get the vertices
#for i in $(python python/vertices_counter.py "inputs/"$filename".dat")
for i in 1
do

	##
	## Shortest Cycles

	# create an appropriate .dat file for our .mod file from the given .dat
	python python/spp_input_generator.py "inputs/"$filename".dat" $i $i "temp/"$filename"_cycles_"$i"_input.dat"

	# get the shortest cycle from source i to target i
	glpsol -m glpk/scpp.mod -d "temp/"$filename"_cycles_"$i"_input.dat" > temp/output.tmp

	# add the obtained shortest path to the list of shortest paths
	python python/output_file_appender.py temp/output.tmp "outputs/"$filename"_cycles_output.dat"
done

echo "Done."
echo ""