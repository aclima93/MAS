#!/bin/bash

clear

# substitute cfg1 for $1 and generalize the generix script?
python dat_file_generator.py inputs/cfg1.dat inputs/cfg1_spp_input.dat
glpsol -m spp.mod -d inputs/cfg1_spp_input.dat > output.tmp
python output_file_appender.py output.tmp outputs/cfg1_spp_output.dat
