# SM CORPORATE 🍁 SMS Bomber

A Python-based SMS Bomber tool designed to send OTP requests to various APIs. This tool is intended for **educational and testing purposes only** with explicit consent. Misuse may violate laws and API terms of service.

## Features
- Supports multiple APIs (e.g., Ostad, Chaldal, Daraz, etc.).
- Random User-Agent rotation to mimic legitimate traffic.
- Adjustable message count (1–100).
- Random delays to avoid rate limits.
- Runs in Termux on Android without proxies.

## Prerequisites
- **Termux**: Install from [F-Droid](https://f-droid.org/en/packages/com.termux/) or [GitHub](https://github.com/termux/termux-app).
- **Python**: Installed in Termux.
- **Git**: Installed in Termux.
- Internet connection.

## Setup Instructions for Termux

1. **Update Termux and Install Dependencies**:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
