#! /bin/bash

for a in *.txt; do
  timestamp=$(date +"%y%m%d%H%M%S") # Generates a 12-digit timestamp
  content=$(<"$a") # Reads the content of the file
  hash=$(echo "$a" | shasum | sed "s/\ *\-//g" | tr -d '\n')
  echo -n $hash
  echo -n ",\""
  echo -n "$content" | tr -d '\n' | sed "s/\"/\"\"/g" 
  echo "\",$timestamp" # Prints the timestamp
done