#!/bin/bash

# g-4vcpu-16gb : $120
# c-8 (8/16gb) : $160
# m-4vcpu-32gb : $180
# g-8vcpu-32gb : $240
echo 'Creating droplet...'

doctl compute droplet create \
	docker-host \
	--image docker-18-04 \
	--region nyc1 \
	--size g-8vcpu-32gb \
	--wait \
	--volumes e181b0d1-4c33-11ea-ac31-0a58ac144605 \
	--ssh-keys $(doctl compute ssh-key list --format ID --no-header | sed 's/$/,/' | tr -d '\n' | sed 's/,$//')

# Wait for SSH to run commands
sleep 30

# TODO: move this to an init script on the server directly

# mount block storage
doctl compute ssh docker-host --ssh-command 'mkdir -p /mnt/annif_data'
doctl compute ssh docker-host --ssh-command 'mount -o discard,defaults,noatime /dev/disk/by-id/scsi-0DO_Volume_annif-data /mnt/annif_data'
doctl compute ssh docker-host --ssh-command "echo '/dev/disk/by-id/scsi-0DO_Volume_annif-data /mnt/annif_data ext4 defaults,nofail,discard 0 0' | sudo tee -a /etc/fstab"

# clone Annif & run docker
doctl compute ssh docker-host --ssh-command 'git clone https://github.com/NatLibFi/Annif.git'
doctl compute ssh docker-host --ssh-command 'ANNIF_PROJECTS=/mnt/annif_data MY_UID=$(id -u) MY_GID=$(id -g) docker-compose -f Annif/docker-compose.yml up -d'

# Update Corpora from git
#
# Clone if the folder doesn't exist, otherwise pull
doctl compute ssh docker-host --ssh-command 'cd /mnt/annif_data/; [ -d /mnt/annif_data/Annif-corpora ] && git -C Annif-corpora pull ||  git clone https://github.com/mjsuhonos/Annif-corpora.git'

# Post-process corpora
# eg. unzip compressed files eg. LCSH.ttl
#
# TODO: use makefiles