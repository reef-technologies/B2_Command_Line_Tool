#!/bin/bash

# Load B2 credentials and configurations
source .env

# Variables
BUCKET_NAME="mici-bucket"
FILE_ID="4_z70b22389f0bf88e4877f0e12_f112c45fd5ce1bfce_d20240131_m154715_c005_v0501004_t0059_u01706716035791"
LOCAL_FILE_PATH="/home/michal/Downloads/83829173_58.pdf"
B2_FILE_NAME="b2_test_file.pdf" # Name for the file in B2
COPY_FILE_NAME="copied_${B2_FILE_NAME}"
DOWNLOAD_PATH="downloaded_${B2_FILE_NAME}"

# List buckets
echo "Listing all buckets"
./dist/b2 list-buckets

# Upload a file
echo "Uploading a file to B2"
./dist/b2 upload-file $BUCKET_NAME $LOCAL_FILE_PATH $B2_FILE_NAME

# List files in a bucket
echo "Listing files in the bucket"
./dist/b2 ls $BUCKET_NAME

# Copy a file by ID
echo "Copying file by ID"
# Copy a file by ID and parse the output to get the new file ID
COPIED_FILE_JSON=$(./dist/b2 copy-file-by-id $FILE_ID $BUCKET_NAME $COPY_FILE_NAME)
COPIED_FILE_ID=$(echo "$COPIED_FILE_JSON" | jq -r '.fileId')

# Delete the copied file version
echo "Deleting the copied file version"
# Retrieve the file ID of the copied file first, then delete. This part needs manual handling or scripting to parse output.
./dist/b2 delete-file-version $COPY_FILE_NAME $COPIED_FILE_ID



# Download a file by id
echo "Downloading a file with download-file-by-id"
./dist/b2 download-file-by-id $FILE_ID $DOWNLOAD_PATH

# Download a file
echo "Downloading a file with download-file"
./dist/b2 download-file b2id://$FILE_ID $DOWNLOAD_PATH

# Get file info
echo "Getting file information using file ID"
./dist/b2 file-info b2id://$FILE_ID




# Clean up: delete downloaded file
rm -f $DOWNLOAD_PATH

echo "Done with B2 CLI operations."
