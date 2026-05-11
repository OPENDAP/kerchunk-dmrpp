#!/usr/bin/env python3

"""
Simple script to take a geotiff file and convert it to a json file

Output of this script is a json document that has been generated from the supplied geotiff file

Authors
    Samuel Lloyd - 5/11/26
"""

import ujson
from kerchunk.tiff import tiff_to_zarr
from pathlib import Path

verbose = False

def generate_output_file_name(input_file):
    """
    Function to generate an output file name if the input filename is provided but the output filename was not.
    :param input_file:
    :return: name of the output_file.
    """
    basename = Path(input_file).name
    output_file = 'output_files/' + basename.split('.')[0] + '.json'

    if verbose: print(output_file)

    return output_file


def convert_to_json(input_file, output_file):
    """
    Converts the geotiff file to a json file.
    :param input_file: geotiff file to be converted.
    :param output_file: json file of the converted geotiff
    :return:
    """
    refs = tiff_to_zarr(input_file)

    with open(output_file, "wb") as f:
        f.write(ujson.dumps(refs).encode())

    if verbose: print(f"Successfully created {output_file}")


def main():
    """
    main function to handle the commandline args
    :return:
    """
    import argparse
    parser = argparse.ArgumentParser(description="Generate a json file with KerChunk using a provided geotiff file")

    parser.add_argument("-i", "--input_file", help="Input geotiff filepath")
    parser.add_argument("-o", "--output_file", help="Output json filename")

    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true", default=False)

    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    if args.input_file is None:
        print("No input file provided, Exiting ...")
        return
    else:
        input_file = args.input_file

    if args.output_file is None:
        print("No output file provided, generating output file name based on input file ...")
        output_file = generate_output_file_name(input_file)
    else:
        output_file = 'output_files/' + args.output_file

    convert_to_json(input_file, output_file)


if __name__ == "__main__":
    main()
