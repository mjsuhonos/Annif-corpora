#!/bin/bash

echo ' ==> Destroying droplet...'

# Clean shutdown
doctl compute ssh docker-annif -v --ssh-command 'shutdown -h now'

# Wait to ensure disk writes are done
sleep 30

# Destroy droplet
doctl compute droplet delete docker-annif -f