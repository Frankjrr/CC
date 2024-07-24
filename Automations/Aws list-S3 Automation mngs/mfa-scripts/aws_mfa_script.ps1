# Variables (replace with your actual values)
$USER_NAME = "hassan.tariq"
$PROFILE_NAME = "cc-prod"
$NEW_PROFILE_NAME = "cc-prod-temp"
$MFA_ARN = "arn:aws:iam::750283682324:mfa/hassan.tariq"
$TOKEN_CODE = "493513"  # Change this to the actual MFA code

# Function to list AWS CLI profiles
function List-Profiles {
    Write-Host "Listing AWS CLI profiles..."
    aws configure list-profiles
    Write-Host
}

# Function to list existing MFA devices for the user
function List-MFA-Devices {
    Write-Host "Listing existing MFA devices for user $USER_NAME..."
    aws iam list-mfa-devices --user-name $USER_NAME --profile $PROFILE_NAME
    Write-Host
}

# Function to get a session token using MFA
function Get-Session-Token {
    Write-Host "Getting session token using MFA..."
    $SESSION_TOKEN_JSON = aws sts get-session-token --duration-seconds 129600 --serial-number $MFA_ARN --token-code $TOKEN_CODE --profile $PROFILE_NAME
    if ($SESSION_TOKEN_JSON -ne $null) {
        $SESSION_TOKEN = $SESSION_TOKEN_JSON | ConvertFrom-Json
        Write-Host "Session token obtained."
        return $SESSION_TOKEN
    } else {
        Write-Host "Failed to obtain session token."
        exit 1
    }
}

# Function to configure a new profile with the session token
function Configure-New-Profile {
    param (
        [Parameter(Mandatory=$true)]
        [PSCustomObject]$SessionToken
    )

    Write-Host "Configuring new profile $NEW_PROFILE_NAME..."

    $AWS_ACCESS_KEY_ID = $SessionToken.Credentials.AccessKeyId
    $AWS_SECRET_ACCESS_KEY = $SessionToken.Credentials.SecretAccessKey
    $AWS_SESSION_TOKEN = $SessionToken.Credentials.SessionToken

    if ($AWS_ACCESS_KEY_ID -and $AWS_SECRET_ACCESS_KEY -and $AWS_SESSION_TOKEN) {
        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID --profile $NEW_PROFILE_NAME
        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY --profile $NEW_PROFILE_NAME
        aws configure set aws_session_token $AWS_SESSION_TOKEN --profile $NEW_PROFILE_NAME

        Write-Host "New profile $NEW_PROFILE_NAME configured."
        Write-Host
    } else {
        Write-Host "Failed to configure new profile due to missing token values."
        exit 1
    }
}

# Main script execution
List-Profiles
List-MFA-Devices
$SessionToken = Get-Session-Token
Configure-New-Profile -SessionToken $SessionToken

Write-Host "Script execution completed."
