#!/bin/bash

os_name=$(uname -s)
arch=$(uname -m)
echo "Operating System: $os_name, arch=$arch"

# Function to display a message and exit with an error code
exit_with_error() {
    echo "Error: $1"
    exit 1
}

# Function to download and extract the chromedriver
download_and_extract_chromedriver() {
    local download_url="$1"
    local destination_folder="$2"

    # Check if the destination folder already exists
    if [ ! -d "$destination_folder" ]; then
        mkdir -p "$destination_folder" || exit_with_error "Failed to create destination folder: $destination_folder"
    fi

    # Define the path to the ZIP file
    local zip_file="${destination_folder}/chromedriver.zip"

    # Use curl to download the file
    curl -o "$zip_file" "$download_url" || exit_with_error "Failed to download chromedriver from $download_url"

    # Unzip the downloaded file
    unzip -q "$zip_file" -d "$destination_folder" || exit_with_error "Failed to unzip chromedriver"

    # Move chromedriver file to resources folder
    mv "${destination_folder}/chromedriver-mac-arm64/chromedriver" "$destination_folder" || exit_with_error "Failed to move chromedriver"

    # Delete the chromedriver-mac-arm64 folder
    rm -r "${destination_folder}/chromedriver-mac-arm64" || exit_with_error "Failed to delete chromedriver-mac-arm64 folder"

    # Delete the ZIP file after unzipping
    rm "$zip_file" || exit_with_error "Failed to delete ZIP file"
}

if [ "$os_name" = "Darwin" ] && [ "$arch" = "arm64" ]; then
    echo "Building for Apple M1"
    ARCH="arm64"

    # Define the URL of the file to download for Apple M1
    download_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/mac-arm64/chromedriver-mac-arm64.zip"
else
    echo "Building for x86_64"
    ARCH="x86_64"

    # Define the URL of the file to download for x86_64
    download_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/mac-x64/chromedriver-mac-x64.zip"
fi

# Define the destination folder for the downloaded file (project_root/resources)
destination_folder="../resources"

# Download and extract chromedriver
download_and_extract_chromedriver "$download_url" "$destination_folder"
