#!/bin/bash

# common filename to be used
filename="cfg0"


##
## All Shortest Paths
echo "Generating Paths..."


# combine patsh and cycles and create files for knapsack coverage problem
python python/path_generation.py "inputs/"$filename".dat" "outputs/"$filename"_spp_output.dat" "outputs/"$filename"_scpp_output.dat" "outputs/"$filename"_aspp_output.dat" "temp/"$filename"_node_coverage_input.dat" "temp/"$filename"_edge_coverage_input.dat" "temp/"$filename"_edge_pair_coverage_input.dat"		

# knapsack for node coverage
glpsol -m glpk/kp.mod -d "temp/"$filename"_node_coverage_input.dat" > "outputs/"$filename"_node_coverage.dat"

echo "Done."
echo ""