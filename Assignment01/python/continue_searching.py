__authors__ = 'aclima, ilpetronilho, pjaneiro'

import sys

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 3:

        input_filename = sys.argv[1]
        previous_solutions_filename = sys.argv[2]

        input_file = open(input_filename, 'r')
        input_lines = input_file.readlines()
        input_file.close()

        previous_solutions_file = open(previous_solutions_filename, 'r')
        previous_solutions_lines = previous_solutions_file.readlines()
        previous_solutions_file.close()

        if "PROBLEM HAS NO PRIMAL FEASIBLE SOLUTION\n" in input_lines:
            print("False")
        elif input_lines == previous_solutions_lines:
            print("False")
        else:
            print("True")

    else:
        print("continue_searching expects arguments: <input file> <previous solutions file>")

