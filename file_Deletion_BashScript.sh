#!/bin/bash

# Path to the log file containing filenames
log_file="/home/SamuelRPI/Desktop/PavMonSystem/uploaded.log"

# Paths to the folders where files need to be deleted
target_folder_20MP="/home/SamuelRPI/Desktop/PavMonSystem/Captures_20MP_Local"
target_folder_108MP="/home/SamuelRPI/Desktop/PavMonSystem/Captures_108MP_Local"

# Read each line from the log file
while IFS= read -r line; do
  # Extract the filename starting with "Capture"
  if [[ $line =~ Capture.* ]]; then
    filename="$(basename "${BASH_REMATCH[0]}")"
    
    # Construct the full paths to the files
    file_path_20MP="$target_folder_20MP/$filename"
    file_path_108MP="$target_folder_108MP/$filename"
    
    # Check if the file exists in the first folder and delete it
    if [ -f "$file_path_20MP" ]; then
      rm "$file_path_20MP"
      echo "Deleted: $file_path_20MP"
    else
      echo "File not found in folder 1: $file_path_20MP"
    fi
    
    # Check if the file exists in the second folder and delete it
    if [ -f "$file_path_108MP" ]; then
      rm "$file_path_108MP"
      echo "Deleted: $file_path_108MP"
    else
      echo "File not found in folder 2: $file_path_108MP"
    fi
  fi
done < "$log_file"



