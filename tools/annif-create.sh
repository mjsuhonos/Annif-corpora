#!/bin/bash

# g-4vcpu-16gb : $120
# m-4vcpu-32gb : $180

# c-8 (8/16gb) : $160
# g-8vcpu-32gb : $240

echo ' ==> Creating droplet...'

# TODO: parameterize
#
doctl compute droplet create \
	docker-annif \
	--image docker-18-04 \
	--region nyc1 \
	--size c-8 \
	--wait \
	--volumes e181b0d1-4c33-11ea-ac31-0a58ac144605 \
	--ssh-keys $(doctl compute ssh-key list --format ID --no-header | sed 's/$/,/' | tr -d '\n' | sed 's/,$//')

# Wait for SSH to run commands
sleep 30

# TODO: move this to an init script on the server directly

# remove rate limiting on SSH
doctl compute ssh docker-annif -v --ssh-command  'ufw allow ssh'

echo ' ==> Mounting block storage...'

# mount block storage
doctl compute ssh docker-annif -v --ssh-command 'mkdir -p /mnt/annif_data; mount -o discard,defaults,noatime /dev/disk/by-id/scsi-0DO_Volume_annif-data /mnt/annif_data'
doctl compute ssh docker-annif -v --ssh-command "echo '/dev/disk/by-id/scsi-0DO_Volume_annif-data /mnt/annif_data ext4 defaults,nofail,discard 0 0' | sudo tee -a /etc/fstab"

# Pull Annif-Corpora from git
#
# Clone if the folder doesn't exist, otherwise pull
doctl compute ssh docker-annif -v --ssh-command 'cd /mnt/annif_data/; [ -d /mnt/annif_data/Annif-corpora ] && git -C Annif-corpora pull ||  git clone https://github.com/mjsuhonos/Annif-corpora.git'

echo ' ==> Starting Docker...'

# Run Docker
doctl compute ssh docker-annif -v --ssh-command 'ANNIF_PROJECTS=/mnt/annif_data MY_UID=$(id -u) MY_GID=$(id -g) docker-compose -f /mnt/annif_data/Annif-corpora/tools/docker-compose.yml up -d'
