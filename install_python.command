#!/bin/bash

# Check if python3 is installed at /usr/bin/python3
if ! [ -x "/usr/bin/python3" ]; then
    echo "Python3 is not found at /usr/bin/python3. Attempting to install..."

    # Check if Homebrew is installed
    if ! command -v brew &>/dev/null; then
        echo "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    # Install python3 using Homebrew
    brew install python3

    # Create a symbolic link to /usr/bin/python3 (might not be necessary, but ensures it's available at that path)
    sudo ln -s -f /usr/local/bin/python3 /usr/bin/python3

    echo "Python3 installed successfully."
else
    echo "Python3 found at /usr/bin/python3."
fi