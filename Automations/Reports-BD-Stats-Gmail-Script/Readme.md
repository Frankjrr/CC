# Database Statistics Email Fetcher

This script fetches emails from a specified Gmail account, extracts database storage statistics, and writes the data to a Google Sheet. The script is configured to fetch emails from the "Reports" folder with a specific subject line, extract relevant data, and append it to the Google Sheet with a date field.

## Prerequisites

1. **Python 3.x**: Ensure you have Python 3.x installed on your machine.
2. **Gmail Account**: A Gmail account with an app password generated.
3. **Google Cloud Service Account**: A service account with access to Google Sheets API.
4. **Google Sheets and Drive API Enabled**: Ensure that the Google Sheets and Drive API is enabled for your project.
5. **Provide Editor access of googlesheet to service account**:

"db-713@i-incentive-430219-i2.iam.gserviceaccount.com",
open sheet => share add this above line from the credentials.json file

## Step-by-Step Guide to Obtain and Use Google Sheets Credentials

## 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on "Select a Project" at the top, then "New Project".
3. Enter a project name and click "Create".

## 2. Enable Google Sheets and Drive API

1. In the Google Cloud Console, go to "APIs & Services" > "Library".
2. Search for "Google Sheets and Googlr Drive API" and click on it.
3. Click "Enable" to enable the API for your project.

## 3. Create Service Account Credentials

1. Go to "APIs & Services" > "Credentials".
2. Click "Create Credentials" and select "Service account".
3. Enter a service account name and description, then click "Create".
4. In the next step, you can skip assigning roles (just click "Continue"), then click "Done".

## 4. Create a Service Account Key

1. Find your newly created service account in the "Service Accounts" list.
2. Click on the "Actions" (three vertical dots) for the service account and select "Manage keys".
3. Click "Add Key" and select "Create new key".
4. Choose "JSON" as the key type and click "Create".
5. A JSON file will be downloaded; this is your `credentials.json` file. Save it securely.

## 5. Share the Google Sheet with the Service Account

1. Open your Google Sheet.
2. Click "Share" and enter the "Client Email" from your `credentials.json` file (e.g., `your-service-account@your-project-id.iam.gserviceaccount.com`).
3. Give the service account edit access.

## 6. Using the Credentials in Your Script

1. Save the downloaded `credentials.json` file in the same directory as your Python script.
2. Your script will use this file to authenticate and interact with Google Sheets.

## Setup

### 1. Install Required Python Packages

```sh
pip install imaplib
pip install email
pip install datetime
pip install re
pip install gspread
pip install google-auth
```
## 2. Create `credentials.json`

Create a `credentials.json` file from your Google Cloud service account and place it in the same directory as the script. This file should contain your service account credentials.

## 3. Configure Your Gmail Account

- Enable IMAP in your Gmail settings.
- Generate an app password if you have 2-Step Verification enabled on your account.

## Script Details

### Email Setup

- **Username**: Your Gmail address.
- **App Password**: The app password generated for your Gmail account.
- **IMAP Host**: 'imap.gmail.com' for Gmail IMAP access.

### Google Sheets Setup

- **Service Account File**: The path to your `credentials.json` file.
- **Spreadsheet Name**: The name of your Google Sheets spreadsheet.
- **Sheet Name**: The name of the sheet within your spreadsheet.

### Script Workflow

1. **Connect to Gmail**: Establish a connection to the Gmail IMAP server and log in using your credentials.
2. **Select Folder**: Select the "Reports" folder to search for emails.
3. **Search Emails**: Search for emails from "reports@gmail.com" with a specific subject containing "Database Storage Statistic of".
4. **Extract Data**: Extract database name and size in GB from the email body using regular expressions.
5. **Append to Google Sheets**: Append the extracted data to the Google Sheet with the current date.

### Column Headers

- **DB Name**: The name of the database extracted from the email body.
- **Size in GB values**: The size of the database in GB extracted from the email body.
- **Date**: The date when the data is appended to the sheet.

## Usage

### Running the Script

1. Ensure you have all the prerequisites installed and configured.
2. Place the `credentials.json` file in the same directory as the script.
3. Run the script using Python:

    ```sh
    python main.py
    ```

### Example Output

```plaintext
Raw search results: b'1 2 3'
Total Messages from reports@cloudcardinc.com on 24-Jul-2024 with subject 'Database Storage Statistic of': 3
Number of emails fetched: 3

===========================================
Subject: Database Storage Statistic of "cbkc-prod-db" - [CBKC - Production]
To: devops@gmail.com
From: reports@gmail.com
Date: Mon, 24 Jul 2024 11:00:07 +0000
Message: 
Hi Team, 

Below are the database storage statistics of cbkc-prod-db DB on CBKC - Production environment.

Size in MB = 551649
Size in GB = 538.7197265625000000
Allocated Storage in GB = 1000
Max Allocated Storage in GB = 2000
DB Class = db.r6i.4xlarge

Thanks,
Database Monitoring Job

Desclaimer: This is an automated generated email, please do not reply and connect DBA in-case of any query.

===========================================

Final Extracted Data:
cbkc-prod-db                   538.7197265625000000     

Data successfully written to Google Sheets.
```

### Notes:

- Replace `"hassan.tariq@gmail.com"` and `"fyjfbjdigeufhobe"` with your actual Gmail address and app password.
- Update the `"Database Statistics"` and `sheet1` with your actual spreadsheet and sheet names.

