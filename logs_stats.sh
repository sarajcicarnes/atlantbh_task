#!/usr/bin/env bash

# checks if there are two arguments, if not display usage
if [ $# -ne 2 ]; then
  echo "Usage: $0 <logs_directory> <search_string>"
  exit 1
fi

# first and second arg
LOGS_DIR="$1"
SEARCH_STRING="$2"

# checks if the directory is valid/exists
if [ ! -d "$LOGS_DIR" ]; then
  echo "Error: '$LOGS_DIR' is not a valid directory."
  exit 1
fi


DATA=""
for file in "$LOGS_DIR"/*; do # goes through each item that is in LOGS_DIR
  if [ -f "$file" ]; then # checks if the file is a regular file, and not a dir or symlink
    filename=$(basename "$file")
    size=$(du -sh "$file" | cut -f1) # human readable file size
    total_lines=$(wc -l < "$file") # total lines in the file
    search_count=$(grep -c "$SEARCH_STRING" "$file") # count of search argument (ex. Chrome/)
    
    DATA+="$filename|$size|$total_lines|$search_count\n" # appending to existing value in DATA
  fi
done

SORTED=$(echo -e "$DATA" | sort -t '|' -k4,4nr) # sorting so that file names with the highest search count appear first

printf "%-25s %-15s %-15s %-15s\n" "FILE NAME" "SIZE" "TOTAL LINES" "SEARCH COUNT" # a table like header, for easier readibility
echo "--------------------------------------------------------------------------------"

# output of the results
while IFS='|' read -r filename size total_lines search_count; do 
  printf "%-25s %-15s %-15s %-15s\n" "$filename" "$size" "$total_lines" "$search_count"
done <<< "$SORTED"
