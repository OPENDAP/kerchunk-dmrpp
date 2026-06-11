#!/usr/bin/env python3

# Psudeo code
# read in json file to a dictionary
# make a xml variable
# start parsing json vars into dmrpp fields
# write xml var to a file
# /!\ profit /!\

from pathlib import Path
import json

verbose = False

def generate_output_file_name(input_file):
    """
    Generates output file name from input file
    :param input_file:
    :return:
    """
    basename = Path(input_file).name
    output_file = 'output_files/' + basename.split('.')[0] + '.dmrpp'

    if verbose: print(output_file)

    return output_file


def conversion_driver(input_file, output_file):
    """
    Daily driver for the conversion progress, all fcts are called from within this fct
    :param input_file:
    :param output_file:
    :param verbose:
    :return:
    """
    if verbose: print("Begin reading json data into memory ...")
    json_data = read_json(input_file)
    if verbose: print("Json data loaded into memory, beginning conversion ...")


def read_json(input_file):
    """
    Reads json data from input file
    :param input_file:
    :return:
    """
    with open(input_file, 'r') as json_file:
        json_data = json.load(json_file)

    if verbose: print(json_data)

    return json_data


def main():
    """
    Main fucntion
    :return:
    """
    import argparse
    parser = argparse.ArgumentParser(description="Generate a dmr++ file using a provided Kerchunk/Zarr json file")

    parser.add_argument("-i", "--input", required=True, help="Kerchunk/Zarr json file")
    parser.add_argument("-o", "--output", help="Output dmr++ file")

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output", default=False)

    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    if args.input is None:
        print("No input file provided, Exiting ...")
        return
    else:
        input_file = args.input

    if args.output is None:
        print("No output file provided, generating output file name based on input file ...")
        output_file = generate_output_file_name(input_file)
    else:
        output_file = 'output_files/' + args.output

    conversion_driver(input_file, output_file)



if __name__ == "__main__":
    main()