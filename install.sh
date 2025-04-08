#!/bin/bash

echo "Script started."

# Place default config file in /etc/sysupgrader/config.json if it doesn't exist
if [ ! -f /etc/sysupgrader/config.json ]; then
    echo "Creating default config file..."
    mkdir -p /etc/sysupgrader
    cp config.json /etc/sysupgrader/config.json
fi

echo "Installing sysupgrader to /usr/bin/sut..."

# Install sysupgrader to /usr/bin
cp upgrade.py /usr/bin/sut

echo "Setting permissions..."

# Chmod sysupgrader
chmod +x /usr/bin/sut

echo "Done."
