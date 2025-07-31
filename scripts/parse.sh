#!/bin/bash
awk '
{
    # Extract subject, predicate, and object
    subject = $1
    predicate = $2
    object = $3
    for (i = 4; i <= NF; i++) {
        # If we find a language tag like "@mul", we stop adding to the object
        if ($i ~ /^@/) {
            break
        }
        object = object " " $i
    }

    # Remove angle brackets or quotes from subject, predicate, and object
    gsub(/[<>"]/,"",subject)
    gsub(/[<>"]/,"",predicate)
    gsub(/[<>"]|@[a-z]+ \.$/,"",object)

    # Convert subject from a URI to just the identifier digits
    sub(/.*\/Q/,"Q",subject)

    # Convert object from a URI to just the identifier digits
    sub(/.*\/Q/,"Q",object)
	sub(/ \./,"",object)

    # Print the subject identifier and object
#    print subject "\t" object
    print subject
}' P31.nt > P31-subject.qids
