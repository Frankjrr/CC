
# Scripts to opy user home directory upload to s3 and download on other instance

To automate the process for all the users, you can modify the scripts to handle multiple users in a loop. Below are the updated scripts.

## On the Source Instance
- Create the script to zip and upload home directories to S3:
```
#!/bin/bash

# Variables
USERS=("furqan.nadeem" "khuram.arif" "ahsan.wali" "hasnat.ali" "fahad.mahmood" "idrees.faiq" "muhammad.shehryar" "arham.nawaz" "umair.khan")
S3_BUCKET="audit-manager-service"

for USERNAME in "${USERS[@]}"; do
  HOME_DIR="/home/$USERNAME"
  ZIP_FILE="/tmp/${USERNAME}_home.zip"

  # Check if the user's home directory exists
  if [ ! -d "$HOME_DIR" ]; then
    echo "Home directory for $USERNAME does not exist. Skipping."
    continue
  fi

  # Compress the user's home directory
  echo "Compressing the home directory of $USERNAME..."
  zip -r $ZIP_FILE $HOME_DIR

  # Check if zip command was successful
  if [ $? -ne 0 ]; then
    echo "Failed to compress the home directory of $USERNAME. Skipping."
    continue
  fi

  # Upload the zip file to S3
  echo "Uploading $ZIP_FILE to S3 bucket $S3_BUCKET..."
  aws s3 cp $ZIP_FILE s3://$S3_BUCKET/${USERNAME}_home.zip

  # Check if upload was successful
  if [ $? -ne 0 ]; then
    echo "Failed to upload the zip file for $USERNAME to S3. Skipping."
    continue
  fi

  echo "User's home directory for $USERNAME has been compressed and uploaded to S3 successfully."
done

```
2. Make the script executable:
```
chmod +x sync_all_users_home_to_s3.sh
```
3. Run the script:
```
./sync_all_users_home_to_s3.sh
```
## On the Destination Instance
1. Create the script to download and extract home directories from S3:
```
#!/bin/bash

# Variables
USERS=("furqan.nadeem" "khuram.arif" "ahsan.wali" "hasnat.ali" "fahad.mahmood" "idrees.faiq" "muhammad.shehryar" "arham.nawaz" "umair.khan")
S3_BUCKET="audit-manager-service"

for USERNAME in "${USERS[@]}"; do
  HOME_DIR="/home/$USERNAME"
  ZIP_FILE="/tmp/${USERNAME}_home.zip"

  # Ensure the user exists on the destination instance
  if ! id -u $USERNAME >/dev/null 2>&1; then
    echo "User $USERNAME does not exist. Creating user..."
    sudo useradd -m -s /bin/bash $USERNAME
  fi

  # Create home directory if it does not exist
  if [ ! -d "$HOME_DIR" ]; then
    echo "Creating home directory for $USERNAME..."
    sudo mkdir -p $HOME_DIR
    sudo chown $USERNAME:$USERNAME $HOME_DIR
  fi

  # Download the zip file from S3
  echo "Downloading $ZIP_FILE from S3 bucket $S3_BUCKET..."
  aws s3 cp s3://$S3_BUCKET/${USERNAME}_home.zip $ZIP_FILE

  # Check if download was successful
  if [ $? -ne 0 ]; then
    echo "Failed to download the zip file for $USERNAME from S3. Skipping."
    continue
  fi

  # Extract the zip file to the user's home directory
  echo "Extracting $ZIP_FILE to $HOME_DIR..."
  sudo unzip -o $ZIP_FILE -d /

  # Check if unzip command was successful
  if [ $? -ne 0 ]; then
    echo "Failed to extract the zip file for $USERNAME. Skipping."
    continue
  fi

  # Set the correct ownership for the user's home directory
  echo "Setting ownership for $HOME_DIR..."
  sudo chown -R $USERNAME:$USERNAME $HOME_DIR

  echo "User's home directory for $USERNAME has been downloaded and unzipped successfully."
done
```
2. Make the script executable:
```
chmod +x restore_all_users_home_from_s3.sh
```
3. Run the script:
```
./restore_all_users_home_from_s3.sh
```
Additional Notes

- Ensure AWS CLI is Configured: The AWS CLI must be configured with appropriate credentials and region settings on both the source and destination instances. Use aws configure if needed.
- Permissions: The scripts require sudo privileges to create users and manage file permissions.
- Error Handling: Both scripts include basic error handling to skip users if any step fails.
By running these scripts, you can automate the process of compressing, uploading, downloading, and extracting home directories for multiple users between two instances via an S3 bucket.

