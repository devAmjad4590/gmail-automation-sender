# Gmail Bulk Sender Automation 📧
A Python automation tool designed to send personalized bulk emails using your personal Gmail account via the official Google Gmail API. It separates code from content, allowing you to update your email subject and body without touching the code.

## 🚀 Features
Official Gmail API: Sends authentic emails that land in the "Primary" inbox (avoids Spam folders).

External Content Loading: Reads the Subject and Body from a simple text file (email_content.txt).

Bulk Processing: Reads recipients from a list (email_list.txt) and automatically removes duplicates.

Safety Mechanisms: Includes rate limiting (delays) between emails to respect Gmail's API limits.

Attachment Support: Capable of sending attachments (requires minor code uncommenting).

## 🛠️ Prerequisites
Before running the script, ensure you have:

Python 3.x installed.

A Google Cloud Project with the Gmail API enabled.

### 📦 Installation & Setup
1. Install Dependencies
Open your terminal or PowerShell in the project folder and run:

```
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
2. Google Cloud Configuration
Go to the Google Cloud Console.

Create a project and enable the Gmail API.

Go to APIs & Services > OAuth Consent Screen:

Select External.

Crucial: Add your own email address to the "Test Users" list.

Go to Credentials > Create Credentials > OAuth Client ID:

Application Type: Desktop App.

Download the JSON file, rename it to credentials.json, and place it in this project folder.

## 📂 File Structure
Your folder should look like this:

app.py (The main Python script)

credentials.json (Downloaded from Google Cloud)

email_list.txt (List of recipient emails)

email_content.txt (Subject and Body text)

token.json (Auto-generated after first login - do not delete unless resetting)

## 📝 How to Use
Step 1: Add Recipients
Open email_list.txt and paste your email addresses (one per line):


```
recruiter@company.com
admin@agency.com
hr@startup.com
```
Step 2: Write Your Email
Open email_content.txt.

Line 1: The Subject Line.

Line 2 onwards: The Email Body.

Example:

```
Inquiry: Urgent Attestation Appointment

Dear Team,

My name is Amgad and I am looking to book an appointment...
[Rest of message]
```
Step 3: Run the Script
Open PowerShell in the folder and run:

```
py app.py
```
First time run: A browser window will open. Log in with your Google account and click Allow.

Subsequent runs: It will use the saved token.json and start immediately.

## ⚠️ Troubleshooting
ModuleNotFoundError
You haven't installed the libraries. Run the pip install command in the Installation section.

invalid_grant or Bad Request
Your login token has expired or is invalid.

Fix: Delete the token.json file and run the script again to re-login.

Access Blocked: App has not completed the Google verification process
Fix: Click "Advanced" -> "Go to [App Name] (unsafe)".

Fix: Make sure your email is added to the Test Users in the Google Cloud OAuth Consent Screen.

## 🔒 Security Note
This script runs locally on your computer. Your credentials (credentials.json) and tokens (token.json) are stored only on your machine. Never share these files with others.
