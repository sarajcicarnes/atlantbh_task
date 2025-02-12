#!/usr/bin/env python3

import sys
import os
import subprocess

# checks if there are two arguments, if not display usage
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <logs_directory> <search_string>")
    sys.exit(1)

# first and second arg
logs_dir = sys.argv[1]
search_string = sys.argv[2]

# checks if the directory is valid/exists
if not os.path.isdir(logs_dir):
    print(f"Error: '{logs_dir}' is not a valid directory.")
    sys.exit(1)

data = []  # will store tuples of (filename, size_str, total_lines_int, search_count_int)

# goes through each item that is in logs_dir
for entry in os.listdir(logs_dir):
    file_path = os.path.join(logs_dir, entry)

    # checks if the file is a regular file, and not a dir or symlink
    if os.path.isfile(file_path):
        filename = entry  # equivalent to basename in bash

        # call du -sh to get size in human-readable format (like in bash)
        try:
            size_output = subprocess.check_output(["du", "-sh", file_path])
            size_str = size_output.decode().split()[0]  # example: "101M"
        except subprocess.CalledProcessError:
            size_str = "N/A"

        # call wc -l to get total lines
        try:
            wc_output = subprocess.check_output(["wc", "-l", file_path])
            total_lines_str = wc_output.decode().split()[0]  # e.g. "715760"
            total_lines_int = int(total_lines_str)
        except subprocess.CalledProcessError:
            total_lines_int = 0

        # call grep -c to get search_count (ex. Chrome/)
        try:
            grep_output = subprocess.check_output(["grep", "-c", search_string, file_path])
            search_count_str = grep_output.decode().strip()
            search_count_int = int(search_count_str)
        except subprocess.CalledProcessError:
            search_count_int = 0

        # storing data in a tuple
        data.append((filename, size_str, total_lines_int, search_count_int))

# sort so that file names with the highest search count appear first
data.sort(key=lambda x: x[3], reverse=True)

# print table header (similar to bash's printf usage)
print(f"{'FILE NAME':<25} {'SIZE':<15} {'TOTAL LINES':<15} {'SEARCH COUNT':<15}")
print("--------------------------------------------------------------------------------")

# output of the results
for (filename, size_str, total_lines_int, search_count_int) in data:
    print(f"{filename:<25} {size_str:<15} {total_lines_int:<15} {search_count_int:<15}") 
