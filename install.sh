#!/bin/bash

config_folder="/etc/sysupgrader"
config_file="/etc/sysupgrader/config.json"
installation_path="/usr/bin/sut"

echo "Script started."

# Place default config file in /etc/sysupgrader/config.json if it doesn't exist
if [ ! -f $config_file ]; then
    echo "Creating default config file..."
    mkdir -p "$config_folder"
    cp config.json "$config_file"
fi

echo "Installing sysupgrader to $installation_path..."

# Install sysupgrader to /usr/bin
cp upgrade.py "$installation_path"

echo "Setting permissions..."

# Chmod
chmod +x "$installation_path"
chmod +x postinst.py

# Post installation
echo "Running post install..."
python3 postinst.py

echo "Done."

echo "Maybe you would like to edit config file on $config_file."
echo "Warning: Only users with root access should edit config file. THIS SCRIPT IS POTTENTIALLY DANGEROUS."