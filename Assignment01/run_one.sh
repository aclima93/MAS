#!/bin/bash

# common filename to be used
filename=$1

# delete the previous results
rm -r "outputs/"$filename"_spp_output.dat"

echo "Running for "$filename"..."

# get the vertices
for i in $(python vertices_counter.py inputs/cfg1.dat)
do
	# create an appropriate .dat file for our .mod file from the given .dat
	python dat_file_generator.py "inputs/"$filename".dat" $i "inputs/"$filename"_spp_input.dat"

	# get the shortest path from source i to target
	glpsol -m spp.mod -d "inputs/"$filename"_spp_input.dat" > output.tmp

	# add the obtained shortest path to the list of shortest paths
	python output_file_appender.py output.tmp "outputs/"$filename"_spp_output.dat"
done

echo "Done."
echo ""