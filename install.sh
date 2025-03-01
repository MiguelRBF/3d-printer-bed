#!/bin/bash

# Check if pip3 is already installed
if command -v pip3 &>/dev/null; then
    echo "pip3 is already installed."
else
    # Update package list and install pip3
    echo "pip3 not found. Installing pip3..."
    sudo apt update
    sudo apt install -y python3-pip

    # Verify installation
    if command -v pip3 &>/dev/null; then
        echo "pip3 was successfully installed."
    else
        echo "Failed to install pip3."
        exit 1
    fi
fi

# Function to check and install Python packages if not installed
install_package() {
    PACKAGE=$1
    if pip3 show "$PACKAGE" &>/dev/null; then
        echo "$PACKAGE is already installed."
    else
        echo "$PACKAGE not found. Installing $PACKAGE..."
        pip3 install "$PACKAGE"

        # Verify installation
        if pip3 show "$PACKAGE" &>/dev/null; then
            echo "$PACKAGE was successfully installed."
        else
            echo "Failed to install $PACKAGE."
        fi
    fi
}

# Install the required packages
install_package "matplotlib"
install_package "numpy"
install_package "pandas"
install_package "scipy"

