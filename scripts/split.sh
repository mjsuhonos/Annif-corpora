#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 inputfile"
  exit 1
fi

inputfile="$1"

TOTAL_LINES=$(wc -l < "$inputfile")

# Define the split sizes for train, validation, and test (e.g., 70%, 15%, 15%)
TRAIN_SPLIT=$(echo "$TOTAL_LINES*70/100" | bc)
VAL_SPLIT=$(echo "$TOTAL_LINES*15/100" | bc)
TEST_SPLIT=$(echo "$TOTAL_LINES*15/100" | bc)

echo "Train set: $TRAIN_SPLIT lines."
echo "Validation set: $VAL_SPLIT lines."
echo "Test set: $(($TOTAL_LINES - $TRAIN_SPLIT - $VAL_SPLIT)) lines."

# Create subfolders for train, eval, and test
mkdir -p train eval test

# Initialize line counter
current_line=0

# Process each line of the input file
while IFS=$'\t' read -r col1 col2; do
  # Increment the current line counter
  ((current_line++))

  # Determine the output folder based on the current line number
  if [ $current_line -le $TRAIN_SPLIT ]; then
    output_folder="train"
  elif [ $current_line -le $(($TRAIN_SPLIT + $VAL_SPLIT)) ]; then
    output_folder="eval"
  else
    output_folder="test"
  fi

  # Create the .txt file with the second column as content
  echo "$col2" > "$output_folder/${col1}.txt"
  
  # Create the .tsv file with the URN content
  echo "<http://www.wikidata.org/entity/${col1}>" > "$output_folder/${col1}.tsv"

done < "$inputfile"
