#!/bin/bash

# Create droplet
./annif-create.sh

# Train backends
time ./annif-train.sh

# Evaluate backends
time ./annif-eval.sh

# Destroy droplet
./annif-destroy.sh

# Notify with sound / popup
echo ' ==> Annif workload complete! <== ' | alerter -sound default

#
#
# docker run -u root:root -v /mnt/annif_data:/annif-projects -p 5000:5000 quay.io/natlibfi/annif annif run -h 0.0.0.0 -p 5000
# docker exec -it -u root:root annif_bash_1 bash
#
#