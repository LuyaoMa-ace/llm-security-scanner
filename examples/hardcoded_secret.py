# examples/hardcoded_secret.py
# WARNING: This file contains INTENTIONAL security vulnerabilities for testing purposes.
# All credentials below are fake, for demonstration only.

import requests

# Hardcoded credentials — never commit secrets to source code!
API_KEY      = "sk-proj-abc123XYZsupersecretkey9999"
DB_PASSWORD  = "admin1234"
DB_USER      = "root"
AWS_SECRET   = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_ACCESS   = "AKIAIOSFODNN7EXAMPLE"
GITHUB_TOKEN = "ghp_16C7e42F292c6912E7710c838347Ae651246"
SECRET_KEY   = "django-insecure-abc123xyz"

def call_api(endpoint):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    return requests.get(endpoint, headers=headers)

def connect_database():
    # Credentials hardcoded directly in connection string
    conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@db.internal.company.com/production"
    return conn_str

def upload_to_s3(file_path):
    import boto3
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS,
        aws_secret_access_key=AWS_SECRET,
        region_name="us-east-1"
    )
    s3 = session.client('s3')
    return s3

if __name__ == "__main__":
    print(call_api("https://api.example.com/data"))
