#!/bin/bash

# common filename to be used
filename=$1

# delete the previous results
rm -r temp/*
rm -r "outputs/"$filename"_spp_output.dat"
rm -r "outputs/"$filename"_cycles_output.dat"

echo "Running for "$filename"..."

# get the vertices
for i in $(python python/vertices_counter.py "inputs/"$filename".dat")
do
	##
	## Shortest Paths from source i to target

	# create an appropriate .dat file for our .mod file from the given .dat
	python python/spp_input_generator.py "inputs/"$filename".dat" $i "temp/"$filename"_spp_input.dat"

	# get the shortest path from source i to target
	glpsol -m glpk/spp.mod -d "temp/"$filename"_spp_input.dat" > temp/output.tmp

	# add the obtained shortest path to the list of shortest paths
	python python/spp_output_file_appender.py temp/output.tmp "outputs/"$filename"_spp_output.dat"
done

##
## Shortest Cycles

# create an appropriate .dat file for our .mod file from the given .dat
python python/scpp_input_generator.py "inputs/"$filename".dat" "temp/"$filename"_scpp_input.dat"

# get the shortest cycle from source i to target i
glpsol -m glpk/scpp.mod -d "temp/"$filename"_scpp_input.dat" > temp/output.tmp

# add the obtained shortest path to the list of shortest paths
python python/scpp_output_file_appender.py temp/output.tmp "outputs/"$filename"_scpp_output.dat"

echo "Done."
echo ""