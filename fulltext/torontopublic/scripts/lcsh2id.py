# for a in *.tsv ; do python3 ../lcshtoid.py $a ../shids/$a; done

import sys
import csv

# Function to read a CSV file and return a dictionary mapping text to shID
def read_csv(file_path):
    mapping = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for line_number, row in enumerate(reader, start=1):
            if len(row) != 2:
                #print(f"Error: {file_path} line {line_number}: {row}")
                continue  # Skip this row and move to the next one
            text, shID = row
            mapping[text] = shID
    return mapping

# Function to process subjects according to the rules
def process_subject(subject, dictionaries, trailing=None):
    if trailing is None:
        trailing = []

    # Trim leading and trailing spaces and dot (.) characters
    subject = subject.strip().strip('.')

    # Look up the subject in the dictionaries
    for d in dictionaries:
        if subject in d:
            shID = d[subject]
            matches = [shID]  # Add the shID to a list of matches
            print(f"Matched: {subject} -> {matches}")
            if trailing:
                # Concatenate the 'trailing' list using the "--" sequence and send it recursively
                matches.extend(process_subject('--'.join(trailing), dictionaries, []))
            return matches
        else: print(f"No match: {subject}")

    # If there's no match, split the string at the last "--" sequence into parts B and C
    if '--' in subject:
        parts = subject.rsplit('--', 1)
        part_b, part_c = parts[0], parts[1]
        # Add part C to an ordered list 'trailing'
        trailing.insert(0, part_c)
        # Send part B recursively into this function
        return process_subject(part_b, dictionaries, trailing)
    else:
        # If there's no "--" left, and no match was found, return an empty list
        return []

# Process a given TSV file and output another TSV file with shIDs
def process_tsv(input_tsv, output_tsv):
    with open(input_tsv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_tsv, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            ID, title = row[:2]
            subjects = row[2:]
            shIDs = set()  # Use a set to store unique shIDs

            for subject in subjects:
                shID_list = process_subject(subject, [subjects_dict, names_dict])
                for shID in shID_list:
                    shIDs.add(shID)  # Add to set to ensure uniqueness

            if shIDs:
                writer.writerow([ID, title] + list(shIDs))

# Check if arguments are provided and call main
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} inputfile.tsv outputfile.tsv")
        sys.exit(1)

    # Assign the arguments to variables for clarity
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    
    # Read the CSV files into dictionaries
    subjects_dict = read_csv('subjects.csv')
    names_dict = read_csv('names.csv')

    process_tsv(inputfile, outputfile)