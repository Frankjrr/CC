#!/bin/bash

# Variables (replace with your actual values)
USER_NAME="hassan.tariq"
PROFILE_NAME="cc-prod"
NEW_PROFILE_NAME="cc-prod-temp"
MFA_ARN="arn:aws:iam::750283682324:mfa/hassan.tariq"
TOKEN_CODE="710114"  # Change this to the actual MFA code

# Function to list AWS CLI profiles
list_profiles() {
    echo "Listing AWS CLI profiles..."
    aws configure list-profiles
    echo
}

# Function to list existing MFA devices for the user
list_mfa_devices() {
    echo "Listing existing MFA devices for user ${USER_NAME}..."
    aws iam list-mfa-devices --user-name "${USER_NAME}" --profile="${PROFILE_NAME}"
    echo
}

# Function to get a session token using MFA
get_session_token() {
    echo "Getting session token using MFA..."
    SESSION_TOKEN=$(aws sts get-session-token --duration-seconds 129600 --serial-number "${MFA_ARN}" --token-code "${TOKEN_CODE}" --profile "${PROFILE_NAME}")
    echo "Session token obtained."
    echo
}

# Function to configure a new profile with the session token
configure_new_profile() {
    echo "Configuring new profile ${NEW_PROFILE_NAME}..."

    AWS_ACCESS_KEY_ID=$(echo "${SESSION_TOKEN}" | jq -r '.Credentials.AccessKeyId')
    AWS_SECRET_ACCESS_KEY=$(echo "${SESSION_TOKEN}" | jq -r '.Credentials.SecretAccessKey')
    AWS_SESSION_TOKEN=$(echo "${SESSION_TOKEN}" | jq -r '.Credentials.SessionToken')

    aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}" --profile "${NEW_PROFILE_NAME}"
    aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}" --profile "${NEW_PROFILE_NAME}"
    aws configure set aws_session_token "${AWS_SESSION_TOKEN}" --profile "${NEW_PROFILE_NAME}"

    echo "New profile ${NEW_PROFILE_NAME} configured."
    echo
}

# Main script execution
list_profiles
list_mfa_devices
get_session_token
configure_new_profile

echo "Script execution completed."
