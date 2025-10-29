# for a in *.tsv ; do python3 ../id2qid.py $a ../id2qid.sorted.tsv ../qids/$a; done

import sys
import csv
import multiprocessing

# Function to process a single line
def process_line(line, key_value_pairs):
    elements = line.strip().split('\t')
    if len(elements) > 2:
        # Filter and map subjects that are in the key_value_pairs dictionary
        filtered_elements = [el.replace('-781', '') if '-781' in el else el for el in elements[2:]]
        #print(f"Elements: {filtered_elements}")
        filtered_subjects = [key_value_pairs.get(subject) for subject in filtered_elements if subject in key_value_pairs]
        #print(f"Subjects: {filtered_subjects}")
        if not filtered_subjects:  # Check if there are no matching subjects
            return None  # Return None to indicate no matches
        elements[2:] = filtered_subjects
    return '\t'.join(elements)

# Worker function for parallel processing
def workerx(input_queue, output_queue, key_value_pairs):
    while True:
        line = input_queue.get()
        if line is None:
            break
        processed_line = process_line(line, key_value_pairs)
        output_queue.put(processed_line)

def main(inputfile, dictfile, outputfile):
    # Create a dictionary to hold the key-value pairs from dictfile
    key_value_pairs = {}

    # Read key-value pairs into a dictionary from dictfile
    with open(dictfile, 'r') as f2:
        reader = csv.reader(f2, delimiter='\t')
        key_value_pairs = {row[0]: row[1] for row in reader if len(row) >= 2}

    # Set up multiprocessing
    num_workers = multiprocessing.cpu_count()
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # Start worker processes
    workers = []
    for _ in range(num_workers):
        worker_process = multiprocessing.Process(target=workerx, args=(input_queue, output_queue, key_value_pairs))
        worker_process.start()
        workers.append(worker_process)

    # Read the inputfile and put lines into the input queue
    with open(inputfile, 'r') as f1:
        for line in f1:
            input_queue.put(line)

    # Signal the workers to stop when done
    for _ in range(num_workers):
        input_queue.put(None)

    # Collect the processed lines and write them to the output file
    with open(outputfile, 'w') as tmpfile:
        while any(worker.is_alive() for worker in workers):
            while not output_queue.empty():
                processed_line = output_queue.get()
                if processed_line is not None:  # Check if the line has matches
                    tmpfile.write(processed_line + '\n')

    # Wait for all workers to finish
    for worker in workers:
        worker.join()

# Check if arguments are provided and call main
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} inputfile.tsv dictfile.tsv outputfile.tsv")
        sys.exit(1)

    # Assign the arguments to variables for clarity
    inputfile = sys.argv[1]
    dictfile = sys.argv[2]
    outputfile = sys.argv[3]

    main(inputfile, dictfile, outputfile)