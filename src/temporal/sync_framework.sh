#!/bin/bash
# Secure Sync Script for Project_Symbiosis
# Path: /home/lexirath90/Project_Symbiosis/sync_framework.sh

# Uses environment variable set by auth_cli.py
# NO DECRYPTION LOGIC OR PASSWORD REFERENCES HERE

# Sync Google Drive
if [[ "$1" == "--drive" ]]; then
    echo "Syncing Google Drive..."
    # Download modified files (credentials inherited from auth_cli.py)
    gdrive files list --query "modifiedTime > '2025-01-29T00:00:00'" --no-header | awk '{print $1}' | xargs -I {} gdrive download {} --path /home/lexirath90/Project_Symbiosis/

    # Sync to Android via Termux
    echo "Syncing to Android..."
    rsync -avz -e "ssh -i /home/lexirath90/Documents/secrets/termux_key" \
        /home/lexirath90/Project_Symbiosis/ \
        user@192.168.1.X:/sdcard/Project_Symbiosis/
fi

# Error handling
trap 'echo "Error: $? at $LINENO"; exit 1' ERR
