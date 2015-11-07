#!/bin/bash

# common filename to be used
filename="cfg0"

# delete the previous results
rm -r temp/*
rm -r "outputs/"$filename"_spp_output.dat"
rm -r "outputs/"$filename"_scpp_output.dat"

# we are gonna need these emptied out
touch "outputs/"$filename"_spp_output.dat"
touch "outputs/"$filename"_scpp_output.dat"

echo "Running for "$filename"..."

##
## Shortest Cycles
echo "Finding Cycles"

while true
do

	# create an appropriate .dat file for our .mod file from the given .dat
	python python/scpp_input_generator.py "inputs/"$filename".dat" "outputs/"$filename"_scpp_output.dat" "temp/"$filename"_scpp_input.dat"

	# get the shortest cycle from source i to target i
	glpsol -m glpk/scpp.mod -d "temp/"$filename"_scpp_input.dat" > temp/output.tmp

	# if no more solutions to be found
	if [ $(python python/no_solution_found.py temp/output.tmp) ]; then
		break
    fi 

	# add the obtained shortest path to the list of shortest paths
	python python/scpp_output_file_appender.py temp/output.tmp "outputs/"$filename"_scpp_output.dat"		

done

echo "Done."
echo ""