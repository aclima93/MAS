__authors__ = 'aclima, ilpetronilho, pjaneiro'

import sys

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 2:

        input_filename = sys.argv[1]

        input_file = open(input_filename, 'r')
        lines = input_file.readlines()
        input_file.close()

        print("PROBLEM HAS NO PRIMAL FEASIBLE SOLUTION\n" in lines)

    else:
        print("no_solution_found expects arguments: <input file>")

