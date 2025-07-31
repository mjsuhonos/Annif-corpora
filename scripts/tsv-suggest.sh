#! /bin/bash
# Read the TSV file line by line, extract the last column, and run the command
while IFS=$'\t' read -r line; do
    content=$(echo "$line" | awk -F'\t' '{print $NF}')
    id=$(echo "$line" | cut -f1)

    result=$(echo "$content" | poetry run annif suggest -l 5 u1-http-ensemble-en)
    echo -e "${id}\t$result" >> output_file.tsv

done < /Users/mjsuhonos/annif.nosync/evie-articles-enriched-20250520\ -\ evie-articles-enriched-20250520.tsv 
