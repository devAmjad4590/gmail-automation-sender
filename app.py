import os
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailInternSender:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                try:
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"⚠️  Local server failed: {e}")
                    print("🔄 Trying manual authentication...")
                    creds = flow.run_console()
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("✅ Successfully authenticated with Gmail!")

    def create_message(self, to_email, subject, body_text, attachment_paths=None):
        """Create email message"""
        message = MIMEMultipart()
        message['to'] = to_email
        message['subject'] = subject
        
        # Add body
        message.attach(MIMEText(body_text, 'plain'))
        
        # Add attachments if provided
        if attachment_paths:
            for attachment_path in attachment_paths:
                if os.path.exists(attachment_path):
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(attachment_path)}'
                    )
                    message.attach(part)
                    print(f"📎 Attached: {os.path.basename(attachment_path)}")
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw_message}

    def send_email(self, to_email, subject, body_text, attachment_paths=None):
        """Send email via Gmail API"""
        try:
            message = self.create_message(to_email, subject, body_text, attachment_paths)
            sent_message = self.service.users().messages().send(
                userId='me', 
                body=message
            ).execute()
            
            print(f"✅ Email sent to {to_email} (Message ID: {sent_message['id']})")
            return True
            
        except HttpError as error:
            print(f"❌ Failed to send email to {to_email}: {error}")
            return False

    def send_bulk_applications(self, email_list, subject, body_template, attachment_paths=None, delay=2):
        """Send bulk emails"""
        successful_sends = 0
        failed_sends = 0
        
        print(f"📧 Starting to send {len(email_list)} emails...")
        print(f"⏱️  Delay between emails: {delay} seconds")
        print("-" * 50)
        
        for i, email in enumerate(email_list, 1):
            print(f"[{i}/{len(email_list)}] Sending to: {email}")
            
            success = self.send_email(email, subject, body_template, attachment_paths)
            
            if success:
                successful_sends += 1
            else:
                failed_sends += 1
            
            if i < len(email_list):
                time.sleep(delay)
        
        print("-" * 50)
        print(f"📊 Summary:")
        print(f"   ✅ Successful: {successful_sends}")
        print(f"   ❌ Failed: {failed_sends}")
        print(f"   📧 Total: {len(email_list)}")

def load_email_list(file_path):
    """Load email addresses from file"""
    try:
        with open(file_path, 'r') as f:
            emails = [line.strip().lower() for line in f if line.strip() and '@' in line]
        
        unique_emails = []
        seen = set()
        for email in emails:
            if email not in seen:
                unique_emails.append(email)
                seen.add(email)
        
        print(f"📋 Loaded {len(unique_emails)} unique emails from {file_path}")
        return unique_emails
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []

def load_email_content(file_path):
    """Load subject and body from a text file. First line is Subject, rest is Body."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            if not lines:
                print(f"❌ Content file is empty: {file_path}")
                return None, None
            
            # The first line is the Subject
            subject = lines[0].strip()
            
            # Everything else is the Body (join lines to keep formatting)
            body = "".join(lines[1:]).strip()
            
            print(f"📋 Loaded content from {file_path}")
            return subject, body
            
    except FileNotFoundError:
        print(f"❌ Content file not found: {file_path}")
        return None, None

def main():
    # Configuration
    EMAIL_LIST_FILE = "email_list.txt"
    CONTENT_FILE = "email_content.txt"
    ATTACHMENT_FILES = [] 
    
    # Initialize Gmail sender
    try:
        gmail_sender = GmailInternSender()
        
        # 1. Load Email List
        email_list = load_email_list(EMAIL_LIST_FILE)
        if not email_list:
            print("❌ No valid emails found.")
            return

        # 2. Load Subject and Body from file
        subject, body = load_email_content(CONTENT_FILE)
        if not subject or not body:
            print("❌ Failed to load email content.")
            return
        
        # Show preview
        print(f"\n📧 Will send to {len(email_list)} unique emails.")
        print("-" * 30)
        print(f"Subject: {subject}")
        print(f"Body Preview: {body[:100]}...") # Show first 100 chars
        print("-" * 30)
        
        # Confirm before sending
        confirm = input(f"\nProceed with sending? (yes/no): ").lower().strip()
        
        if confirm in ['yes', 'y']:
            gmail_sender.send_bulk_applications(
                email_list=email_list,
                subject=subject,
                body_template=body,
                attachment_paths=[], 
                delay=3
            )
        else:
            print("❌ Operation cancelled.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
