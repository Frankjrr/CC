import imaplib
import email
from datetime import datetime, timedelta
import re
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
spreadsheet = client.open('Database Statistics')  # Use your spreadsheet name
sheet = spreadsheet.sheet1  # Use the appropriate sheet

# Clear existing data in the sheet
sheet.clear()

# Write headers to the sheet
headers = ["DB Name", "Size in GB values"]
sheet.append_row(headers)

# Email setup
username = "hassan.tariq@cloudcardinc.com"
app_password = "fyjfbjdigeufhobe"
gmail_host = 'imap.gmail.com'

# Set connection
mail = imaplib.IMAP4_SSL(gmail_host)

# Login
try:
    mail.login(username, app_password)
except imaplib.IMAP4.error as e:
    print(f"Login failed: {e}")
    exit()

# Select folder
mail.select("Reports")

# Get today's date in the format required by IMAP (DD-Mon-YYYY)
today_date = datetime.now().strftime('%d-%b-%Y')

# Calculate yesterday's date
#yesterday_date = (datetime.now() - timedelta(1)).strftime('%d-%b-%Y')

# Search for emails from yesterday with specific subject
status, selected_mails = mail.search(None,
f'(ON "{today_date}" FROM "reports@cloudcardinc.com" SUBJECT "Database Storage Statistic of")')

if status != 'OK':
    print("Error searching emails:", status)
    exit()

# Debug output: Show raw data
print(f"Raw search results: {selected_mails[0]}")

# Total number of mails from specific user with specific subject
email_ids = selected_mails[0].split()
print(f"Total Messages from reports@cloudcardinc.com on {today_date} with subject 'Database Storage Statistic of':",
      len(email_ids))

if len(email_ids) == 0:
    print("No emails found.")
else:
    print(f"Number of emails fetched: {len(email_ids)}")

    # Initialize lists to hold extracted data
    db_names = []
    sizes_in_gb = []

    for num in email_ids:
        status, data = mail.fetch(num, '(RFC822)')
        if status != 'OK':
            print(f"Error fetching email {num}: {status}")
            continue

        email_message = email.message_from_bytes(data[0][1])
        print("\n===========================================")

        # Access data
        print("Subject:", email_message["subject"])
        print("To:", email_message["to"])
        print("From:", email_message["from"])
        print("Date:", email_message["date"])

        for part in email_message.walk():
            if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                message = part.get_payload(decode=True).decode()
                print("Message: \n", message)
                print("==========================================\n")

                # Extract required data using regular expressions
                db_stats = re.findall(
                    r'Below are the database storage statistics of (\S+) DB.*?Size in GB = (\d+\.\d+)', message,
                    re.DOTALL)

                if db_stats:
                    for db_name, size_in_gb in db_stats:
                        db_names.append(db_name)
                        sizes_in_gb.append(size_in_gb)
                else:
                    print("Required data not found in the email body.")
                break

    # Display all extracted data at the end
    print("\nFinal Extracted Data:")
    for db_name, size_in_gb in zip(db_names, sizes_in_gb):
        print("{:<30} {:<20}".format(db_name, size_in_gb))

        # Write data to Google Sheets
        row = [db_name, size_in_gb]
        sheet.append_row(row)

print("Data successfully written to Google Sheets.")
