#!/bin/bash

# common filename to be used
filename="cfg0"

# delete the previous results
rm -r temp/*
rm -r "outputs/"$filename"_spp_output.dat"
rm -r "outputs/"$filename"_scpp_output.dat"
rm -r "outputs/"$filename"_aspp_output.dat"

# we are gonna need these emptied out
touch "outputs/"$filename"_spp_output.dat"
touch "outputs/"$filename"_scpp_output.dat"
touch "outputs/"$filename"_aspp_output.dat"

##
## All Shortest Paths
echo "Finding All Shortest Paths..."

while true
do

	# create an appropriate .dat file for our .mod file from the given .dat
	python python/aspp_input_generator.py "inputs/"$filename".dat" "outputs/"$filename"_aspp_output.dat" "temp/"$filename"_aspp_input.dat"

	# get the shortest path from source to target without using the already discovered solutions
	glpsol -m glpk/aspp.mod -d "temp/"$filename"_aspp_input.dat" > temp/output.tmp

	# if no more solutions to be found
	if [ $(python python/no_solution_found.py temp/output.tmp) = "True" ]; then
		break
    fi 

	# add the obtained shortest path to the list of shortest paths
	python python/aspp_output_file_appender.py temp/output.tmp "outputs/"$filename"_aspp_output.dat"		

done

echo "Done."
echo ""