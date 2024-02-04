#!/bin/bash

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "jq could not be found, please install jq to parse JSON outputs."
    exit 1
fi

# Load B2 credentials and configurations
if [ -f ".env" ]; then
    source .env
else
    echo ".env file not found, please ensure it exists with the necessary configurations."
    exit 1
fi

# Load B2 credentials and configurations
source .env

# Variables
BUCKET_NAME="mici-bucket"
FILE_ID="4_z70b22389f0bf88e4877f0e12_f112c45fd5ce1bfce_d20240131_m154715_c005_v0501004_t0059_u01706716035791"
LOCAL_FILE_PATH="/home/michal/Downloads/83829173_58.pdf"
B2_FILE_NAME="b2_test_file.pdf" # Name for the file in B2
COPY_FILE_NAME="copied_${B2_FILE_NAME}"
DOWNLOAD_PATH="downloaded_${B2_FILE_NAME}"
FOLDER_NAME="sample_folder"
EMPTY_FOLDER="/home/michal/dev/B2/empty"
KEY_NAME="myKey"
KEY_TO_DELETE="keyIdToDelete"

LOCAL_DIR_PATH="/home/michal/Downloads"  # Local directory to sync
B2_DIR_PATH="b2://$BUCKET_NAME/"  # B2 bucket path where the local directory will be synced


# Create and store the output from creating a key
echo
echo ">>>>>>> Creating a new application key"
echo "./dist/b2 create-key $KEY_NAME listBuckets"
KEY_OUTPUT=$(./dist/b2 create-key $KEY_NAME listBuckets)
echo "Key Output: $KEY_OUTPUT"

# Extract the key ID
read -r KEY_ID APPLICATION_KEY <<< "$KEY_OUTPUT"
echo "Key ID: $KEY_ID"
echo "Application Key: $APPLICATION_KEY"

# List buckets
echo
echo ">>>>>>> Listing all buckets"
echo "./dist/b2 list-buckets"
./dist/b2 list-buckets

# Upload a file
echo
echo ">>>>>>> Uploading a file to B2"
echo "./dist/b2 upload-file --noProgress $BUCKET_NAME $LOCAL_FILE_PATH $B2_FILE_NAME"
./dist/b2 upload-file --noProgress $BUCKET_NAME $LOCAL_FILE_PATH $B2_FILE_NAME

# List files in a bucket
echo
echo ">>>>>>> Listing files in the bucket"
echo "./dist/b2 ls $BUCKET_NAME"
./dist/b2 ls $BUCKET_NAME

# Copy a file by ID
echo
echo ">>>>>>> Copying file by ID"
echo "./dist/b2 copy-file-by-id $FILE_ID $BUCKET_NAME $COPY_FILE_NAME"
COPIED_FILE_JSON=$(./dist/b2 copy-file-by-id $FILE_ID $BUCKET_NAME $COPY_FILE_NAME)
echo $COPIED_FILE_JSON | jq '.'
COPIED_FILE_ID=$(echo "$COPIED_FILE_JSON" | jq -r '.fileId')

# Delete the copied file version
echo
echo ">>>>>>> Deleting the copied file version"
echo "./dist/b2 delete-file-version $COPY_FILE_NAME $COPIED_FILE_ID"
./dist/b2 delete-file-version $COPY_FILE_NAME $COPIED_FILE_ID

# Download a file by id
echo
echo ">>>>>>> Downloading a file with download-file-by-id"
echo "./dist/b2 download-file-by-id --noProgress $FILE_ID $DOWNLOAD_PATH"
./dist/b2 download-file-by-id --noProgress $FILE_ID $DOWNLOAD_PATH

# Download a file
echo
echo ">>>>>>> Downloading a file with download-file"
echo "./dist/b2 download-file --noProgress b2id://$FILE_ID $DOWNLOAD_PATH"
./dist/b2 download-file --noProgress b2id://$FILE_ID $DOWNLOAD_PATH

# Get file info
echo
echo ">>>>>>> Getting file information using file ID"
echo "./dist/b2 file-info b2id://$FILE_ID"
./dist/b2 file-info b2id://$FILE_ID

# Get file info by name
echo
echo ">>>>>>> Getting file information using file name"
echo "./dist/b2 file-info b2://$BUCKET_NAME/$B2_FILE_NAME"
./dist/b2 file-info b2://$BUCKET_NAME/$B2_FILE_NAME

# Remove a file or a directory
echo
echo ">>>>>>> Removing a file/directory"
echo "./dist/b2 rm --dryRun --queueSize 5 --noProgress --failFast --threads 2 --versions -r --withWildcard $BUCKET_NAME $FOLDER_NAME"
./dist/b2 rm --dryRun --queueSize 5 --noProgress --failFast --threads 2 --versions -r --withWildcard $BUCKET_NAME $FOLDER_NAME

# Get file URL
echo
echo ">>>>>>> Getting file URL"
echo "./dist/b2 get-url b2id://$FILE_ID"
./dist/b2 get-url b2id://$FILE_ID

# Update bucket settings
echo
echo ">>>>>>> Updating bucket settings"
echo "./dist/b2 update-bucket --fileLockEnabled --defaultServerSideEncryption \"SSE-B2\" --defaultServerSideEncryptionAlgorithm \"AES256\" $BUCKET_NAME allPrivate"
./dist/b2 update-bucket --fileLockEnabled --defaultServerSideEncryption "SSE-B2" --defaultServerSideEncryptionAlgorithm "AES256" $BUCKET_NAME allPrivate

# Hide a file in a bucket
echo
echo ">>>>>>> Hiding a file in the bucket"
echo "./dist/b2 hide-file $BUCKET_NAME $B2_FILE_NAME"
./dist/b2 hide-file $BUCKET_NAME $B2_FILE_NAME

# Create a new bucket
echo
echo ">>>>>>> Creating a new bucket"
echo "./dist/b2 create-bucket \"$BUCKET_NAME-new\" allPublic"
./dist/b2 create-bucket "$BUCKET_NAME-new" allPublic

# Delete a bucket
echo
echo ">>>>>>> Deleting a bucket"
echo "./dist/b2 delete-bucket \"$BUCKET_NAME-new\""
./dist/b2 delete-bucket "$BUCKET_NAME-new"

# Delete an application key
echo
echo ">>>>>>> Deleting an application key"
echo "./dist/b2 delete-key $KEY_TO_DELETE"
./dist/b2 delete-key $KEY_TO_DELETE

# Get account info
echo
echo ">>>>>>> Getting account information"
echo "./dist/b2 get-account-info"
./dist/b2 get-account-info

# List files with options
echo
echo ">>>>>>> Listing files with options"
echo "./dist/b2 ls --long --json --replication --versions -r $BUCKET_NAME"
./dist/b2 ls --long --json --replication --versions -r $BUCKET_NAME

# Sync command
echo
echo ">>>>>>> Synchronizing local directory with B2 bucket"
echo "./dist/b2 sync --noProgress $LOCAL_DIR_PATH $B2_DIR_PATH"
./dist/b2 sync --noProgress $LOCAL_DIR_PATH $B2_DIR_PATH

# Clean up: delete downloaded file
echo "rm -f $DOWNLOAD_PATH"
rm -f $DOWNLOAD_PATH

# At the end of the script, delete the key using the stored KEY_ID
echo
echo ">>>>>>> Deleting the application key"
echo "./dist/b2 delete-key $KEY_ID"
./dist/b2 delete-key $KEY_ID
echo "Application key with ID $KEY_ID has been deleted."

# Sync empty folder, to clean up the bucket
echo
echo ">>>>>>> Synchronizing empty folder with B2 bucket"
echo "./dist/b2 sync --noProgress --allowEmptySource --delete $EMPTY_FOLDER $B2_DIR_PATH"
./dist/b2 sync --noProgress --allowEmptySource --delete $EMPTY_FOLDER $B2_DIR_PATH

echo
echo ">>>>>>> Done with B2 CLI operations."

## TODO: Add more operations to test the B2 CLI
# echo "Listing all application keys:"
# ./dist/b2 list-keys

# echo "Listing all versions of a file:"
# ./dist/b2 ls --versions "$BUCKET_NAME" "$B2_FILE_NAME"


# echo "Starting a large file upload (simulated):"
# You would need to simulate or actually start a large file upload here

# echo "Listing parts of the large file upload:"
#./dist/b2 list-parts "$LARGE_FILE_ID"

#echo "Canceling the large file upload:"
#./dist/b2 cancel-large-file "$LARGE_FILE_ID"

#echo "Setting up replication:"
# Use replication-setup with appropriate parameters here

#echo "Checking replication status:"
./dist/b2 replication-status "$SOURCE_BUCKET_NAME"

#echo "Updating bucket with lifecycle rules:"
# This requires a JSON string for lifecycle rules
#./dist/b2 update-bucket --lifecycleRules '[{"fileNamePrefix":"","daysFromUploadingToHiding":30,"daysFromHidingToDeleting":365}]' "$BUCKET_NAME" allPrivate

#echo "Updating file legal hold:"
./dist/b2 update-file-legal-hold "$B2_FILE_NAME" "$FILE_ID" on

#echo "Updating file retention settings:"
#./dist/b2 update-file-retention --retainUntil "2024-01-01" "$B2_FILE_NAME" "$FILE_ID" compliance
