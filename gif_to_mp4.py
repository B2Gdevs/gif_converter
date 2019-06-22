"""
This script converts git to mp4.

Author: Benjamin Garrard
Date: 6/22/2019
"""
import moviepy.editor as mp
import argparse
import sys
import os


def get_args(cli_args):
	"""
	Get commandline arguments and parse them.

	Parameters
	----------
	cli_args: str
		String of arguments gathered from sys.argv[1:]
	
	Returns
	-------
	argparse.Namespace
		The namespace housing the processed command line
		arguments.
	"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_file", help="The gif file to convert.")
    parser.add_argument("-o", "--output_file", help="The name of output file.")

    args = parser.parse_args(cli_args)
    return args

	
def main():
	"""Script entry point."""
    args = sys.argv[1:]
    args = get_args(args)
    output_file_name = None

    if not args.input_file:
        print("File not given.  Exiting program")
        sys.exit()
    
    if not os.path.isfile(args.input_file):
        print("Path {} does not exist. Exit program.")
        sys.exit()

    if args.output_file:
        output_file_name = os.path.basename(args.output_file)

    clip = mp.VideoFileClip(args.input_file)
    clip.write_videofile(output_file_name)


if __name__ == "__main__": 
    main()