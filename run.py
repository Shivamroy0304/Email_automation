#!/usr/bin/env python3
"""
Simple runner for the email notification system.
Run this script to check for important emails and get notifications.
"""

import main

if __name__ == "__main__":
    print("🔍 Starting email notification system...")
    print("📧 Authenticating with Gmail...")
    
    try:
        service = main.gmail_authenticate()
        print("Gmail authentication successful!")
        
        print(" Checking for unread emails...")
        main.get_unread_emails(service)
        
        print(" Email check complete!")
        
    except Exception as e:
        print(f" Error: {e}")
        print("Please check your credentials and internet connection.")