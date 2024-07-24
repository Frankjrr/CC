from flask import Flask, render_template, request, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
import os
import re

app = Flask(__name__)

# Initialize Boto3 session
session = boto3.Session(profile_name='cc-prod-temp')
s3 = session.client('s3')


def extract_date_from_filename(filename):
    """Extract the date from the filename in the format DYYMMDD."""
    match = re.search(r'D(\d{6})', filename)
    if match:
        date_str = match.group(1)
        try:
            year = '20' + date_str[:2]
            month = date_str[2:4]
            day = date_str[4:6]
            date_obj = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
            return date_obj
        except ValueError:
            return None
    return None


def download_files_by_date(bucket_name, prefix, target_date):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' not in response:
            return f"No files found in {bucket_name}/{prefix}"

        folder_name = prefix.strip('/').split('/')[-1]
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        downloaded_files = []
        for obj in response['Contents']:
            file_name = os.path.basename(obj['Key'])
            file_date = extract_date_from_filename(file_name)
            if file_date and file_date == target_date:
                file_path = os.path.join(folder_name, file_name)
                s3.download_file(bucket_name, obj['Key'], file_path)
                downloaded_files.append(file_name)

        return downloaded_files if downloaded_files else "No files matched the target date."
    except NoCredentialsError:
        return "Credentials not available."
    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/')
def index():
    buckets = s3.list_buckets().get('Buckets', [])
    return render_template('index.html', buckets=buckets)


@app.route('/bucket/<bucket_name>')
def list_prefixes(bucket_name):
    prefixes = []
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    if 'CommonPrefixes' in response:
        prefixes = [prefix['Prefix'] for prefix in response['CommonPrefixes']]
    return render_template('bucket.html', bucket_name=bucket_name, prefixes=prefixes)


@app.route('/prefix', methods=['POST'])
def select_prefix():
    bucket_name = request.form['bucket']
    prefix = request.form['prefix']
    return redirect(url_for('list_subprefixes', bucket_name=bucket_name, prefix=prefix))


@app.route('/prefix/<bucket_name>/<path:prefix>')
def list_subprefixes(bucket_name, prefix):
    prefixes = []
    files = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
    if 'CommonPrefixes' in response:
        prefixes = [prefix['Prefix'] for prefix in response['CommonPrefixes']]
    if 'Contents' in response:
        files = [obj['Key'] for obj in response['Contents'] if obj['Key'] != prefix]
    return render_template('subprefix.html', bucket_name=bucket_name, prefix=prefix, prefixes=prefixes, files=files)


@app.route('/download/<bucket_name>/<path:prefix>', methods=['GET', 'POST'])
def download(bucket_name, prefix):
    if request.method == 'POST':
        date_str = request.form['date']
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        result = download_files_by_date(bucket_name, prefix, target_date)
        return render_template('result.html', result=result)

    return render_template('download.html', bucket_name=bucket_name, prefix=prefix)


if __name__ == '__main__':
    app.run(debug=True)
