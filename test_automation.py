#!/usr/bin/env python3
"""
Test script to verify the automation setup works correctly
"""

import os
import json
import sys

def test_dependencies():
    """Test if all required dependencies are available"""
    print("🔍 Testing dependencies...")
    
    try:
        import requests
        import google.auth
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_config_files():
    """Test if configuration files exist"""
    print("🔍 Testing configuration files...")
    
    required_files = [
        "config/geoapify_config.json",
        "config/service_account.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing config files: {missing_files}")
        return False
    else:
        print("✅ All config files exist")
        return True

def test_geoapify_api():
    """Test Geoapify API connection"""
    print("🔍 Testing Geoapify API...")
    
    try:
        with open("config/geoapify_config.json", "r") as f:
            config = json.load(f)
        
        api_key = config.get("geoapify_api_key")
        if not api_key:
            print("❌ Geoapify API key not found in config")
            return False
        
        import requests
        url = f"https://api.geoapify.com/v1/geocode/search?text=Bangalore&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Geoapify API is working")
            return True
        else:
            print(f"❌ Geoapify API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Geoapify API test failed: {e}")
        return False

def test_google_sheets():
    """Test Google Sheets connection"""
    print("🔍 Testing Google Sheets connection...")
    
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials.from_service_account_file(
            "config/service_account.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        
        service = build("sheets", "v4", credentials=creds)
        
        # Test reading from the sheet
        spreadsheet_id = "1m5Fehqq_cVAb7jitVw1IMo1l_R8XGG0XiQK-gFpKX8I"
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1:A1"
        ).execute()
        
        print("✅ Google Sheets connection is working")
        return True
    except Exception as e:
        print(f"❌ Google Sheets test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting automation tests...\n")
    
    tests = [
        test_dependencies,
        test_config_files,
        test_geoapify_api,
        test_google_sheets
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your automation is ready to run.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())