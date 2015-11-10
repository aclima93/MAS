#!/bin/bash

# common filename to be used
filename=$1

# delete the previous results
for dir_path in "outputs/" "temp/"
do
	cd $dir_path
	find . -type f -name $filename\* | xargs rm -r
	cd ..

done	

# we are gonna need these emptied out for the loops
touch "outputs/"$filename"_spp_output.dat"
touch "outputs/"$filename"_scpp_output.dat"
touch "outputs/"$filename"_aspp_output.dat"

echo "Running for "$filename""

##
## Shortest Paths from source i to target
echo "Finding Shortest Paths from source i to target..."

# get the vertices
for i in $(python python/vertices_counter.py "inputs/"$filename".dat")
do

	# create an appropriate .dat file for our .mod file from the given .dat
	python python/spp_input_generator.py "inputs/"$filename".dat" $i "temp/"$filename"_spp_input.dat"

	# get the shortest path from source i to target
	glpsol -m glpk/spp.mod -d "temp/"$filename"_spp_input.dat" > temp/output.tmp

	# add the obtained shortest path to the list of shortest paths
	python python/output_file_appender.py temp/output.tmp "outputs/"$filename"_spp_output.dat"
done


##
## Shortest Cycles
echo "Finding Shortest Cycles..."

rm -r temp/last_solution.tmp
touch temp/last_solution.tmp
while true
do

	# create an appropriate .dat file for our .mod file from the given .dat
	python python/scpp_input_generator.py "inputs/"$filename".dat" "outputs/"$filename"_scpp_output.dat" "temp/"$filename"_scpp_input.dat"

	# get the shortest cycle without using the already discovered solutions
	glpsol -m glpk/scpp.mod -d "temp/"$filename"_scpp_input.dat" > temp/output.tmp

	# if no more solutions to be found
	if [ $(python python/continue_searching.py temp/output.tmp temp/last_solution.tmp) = "False" ]; then
		break
	else 
	    cat temp/output.tmp > temp/last_solution.tmp
    fi 

	# add the obtained shortest cycle to the list of shortest cycles
	python python/output_file_appender.py temp/output.tmp "outputs/"$filename"_scpp_output.dat"		

done

##
## All Shortest Paths from Source to Target
echo "Finding All Shortest Paths..."

rm -r temp/last_solution.tmp
touch temp/last_solution.tmp
while true
do

	# create an appropriate .dat file for our .mod file from the given .dat
	python python/aspp_input_generator.py "inputs/"$filename".dat" "outputs/"$filename"_aspp_output.dat" "temp/"$filename"_aspp_input.dat"

	# get the shortest path from source to target without using the already discovered solutions
	glpsol -m glpk/aspp.mod -d "temp/"$filename"_aspp_input.dat" > temp/output.tmp

	# if no more solutions to be found
	if [ $(python python/continue_searching.py temp/output.tmp temp/last_solution.tmp) = "False" ]; then
		break
	else 
	    cat temp/output.tmp > temp/last_solution.tmp
    fi 

	# add the obtained shortest path to the list of shortest paths
	python python/output_file_appender.py temp/output.tmp "outputs/"$filename"_aspp_output.dat"		

done

##
## Combine Shortest Paths with Cycles
echo "Combining Paths and Cycles..."

# combine patsh and cycles and create files for knapsack coverage problem
python python/path_generation.py "inputs/"$filename".dat" "outputs/"$filename"_spp_output.dat" "outputs/"$filename"_scpp_output.dat" "outputs/"$filename"_aspp_output.dat" "temp/"$filename"_node_coverage_input.dat" "temp/"$filename"_edge_coverage_input.dat" "temp/"$filename"_edge_pair_coverage_input.dat"		

##
## Select paths with cycles for best coverage
echo "Selecting Paths..."

# knapsack for node coverage
glpsol -m glpk/kp.mod -d "temp/"$filename"_node_coverage_input.dat" > "outputs/"$filename"_node_coverage.dat"

# knapsack for edge coverage
glpsol -m glpk/kp.mod -d "temp/"$filename"_edge_coverage_input.dat" > "outputs/"$filename"_edge_coverage.dat"

# knapsack for edge-pair coverage
glpsol -m glpk/kp.mod -d "temp/"$filename"_edge_pair_coverage_input.dat" > "outputs/"$filename"_edge_pair_coverage.dat"

##
## Done

echo "Done."
echo ""
