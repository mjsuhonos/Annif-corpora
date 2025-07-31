#! /bin/bash

csv_file="/Users/mjsuhonos/docker-aut/SQL/LCSH/subjects.clean.csv"
csv_file2="/Users/mjsuhonos/docker-aut/SQL/LCSH/names.clean.csv"

for a in *.tsv; do
  hash=$(echo "$a" | sed 's/\.tsv$/.txt/') # fix naming to match .txt from abstracts
  hash=$(echo "$hash" | shasum | awk '{print $1}' | tr -d '\n' )

  # Read each line in the file
  while IFS= read -r line; do
	echo -n $hash

	id=''
	score="1"
    # if the line contains 'id.loc.gov' then extract the string in the URL between the last "/" and trailing ">"
    if [[ "$line" =~ id\.loc\.gov ]]; then
	  id=$(echo "$line" | awk -F '/' '{print $NF}' | sed 's/>.*$//')
	  score="1.0"
    else
      # if the line contains "--" then extract the string between the tab "\t" and the last "--" as $id
      if [[ "$line" =~ "--" ]]; then
        id=$(echo "$line" | awk -F '\t' '{print $2}' | sed 's/--.*$//')
	  else
		# otherwise extract the string after the tab "\t" as $id
		id=$(echo "$line" | awk -F '\t' '{print $2}')
      fi
    fi

	if [[ "$score" = "1" ]]; then #if score is 1, we have text;
		# try to convert it to an LCSH ID
		converted=$(awk -F, -v value="$id" '$1 == value {print $2}' "$csv_file")

		if [[ "$converted" != "" ]]; then # we have a match
			id=$(echo "$converted" | sed -n '1p')
		else
			# try to convert it to an LCNAF ID
			converted=$(awk -F, -v value="$id" '$1 == value {print $2}' "$csv_file2")
			if [[ "$converted" != "" ]]; then # we have a match
				id=$(echo "$converted" | sed -n '1p')
			fi
		fi
	fi

    echo -n ",\"$id\",$score"

    timestamp=$(date +"%y%m%d%H%M%S") # Generates a 12-digit timestamp
    echo ",$timestamp" # Prints the timestamp with leading comma
  done < "$a"
done
