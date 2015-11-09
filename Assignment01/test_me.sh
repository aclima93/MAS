#!/bin/bash

# common filename to be used
filename="cfg0"

touch temp/last_solution.tmp

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
	if [ $(python python/continue_searching.py temp/output.tmp temp/last_solution.tmp) = "False" ]; then
		break
    fi 

    cat temp/output.tmp > temp/last_solution.tmp

	# add the obtained shortest path to the list of shortest paths
	python python/aspp_output_file_appender.py temp/output.tmp "outputs/"$filename"_aspp_output.dat"		

done

echo "Done."
echo ""