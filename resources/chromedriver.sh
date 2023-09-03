#!/bin/bash

os_name=$(uname -s)
arch=$(uname -m)
echo "Operating System: $os_name, arch=$arch"

if [ "$os_name" = "Darwin" ] && [ "$arch" = "arm64" ]; then
    echo "Building for Apple M1"
    ARCH="arm64"

    # Define the URL of the file to download
    download_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/mac-arm64/chromedriver-mac-arm64.zip"

    # Define the destination folder for the downloaded file (project_root/resources)
    destination_folder="../resources"

    # Check if the destination folder already exists
    if [ ! -d "$destination_folder" ]; then
        mkdir -p "$destination_folder"  # Create the folder if it doesn't exist
    fi

    # Define the path to the ZIP file
    zip_file="${destination_folder}/chromedriver-mac-arm64.zip"

    # Check if the ZIP file already exists
    if [ -f "$zip_file" ]; then
        echo "Existing ZIP file found. Deleting it..."
        rm "$zip_file"  # Delete the existing ZIP file
    fi

    # Use curl to download the file
    curl -o "$zip_file" "$download_url"

    # Unzip the downloaded file
    unzip -q "$zip_file" -d "$destination_folder"
fi
