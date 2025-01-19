# TEMP-MAIL-API

A Python library for creating and managing temporary email addresses using the mail.tm API. This project provides an easy way to create disposable email addresses programmatically.

## Features

- Create temporary email accounts
- Read messages from temporary email accounts
- Extract Roblox OTP codes and verification URLs
- Parallel account creation support
- JSON-based account data storage
- User-agent rotation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/TEMP-MAIL-API.git
cd TEMP-MAIL-API

# Install required packages
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from main import TempMail

# Create a new instance
temp_mail = TempMail()

# Create a new account
email = "example123@tohru.org"
password = "secretpassword"
status = temp_mail.create_account(email, password)

# Check if account was created successfully
if status == 201:
    print("Account created successfully!")
```

### Reading Messages

```python
# Read messages using account token
messages = temp_mail.read_all_messages(token)
```

### Creating Multiple Accounts

```python
from main import create_random_account
from concurrent.futures import ThreadPoolExecutor

# Create multiple accounts in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(create_random_account) for _ in range(3)]
```

## API Methods

### `create_account(email: str, password: str) -> int`
Creates a new temporary email account.
- Returns HTTP status code (201 for success)

### `read_all_messages(token: str) -> Dict[str, Any]`
Reads all messages for an account.
- Requires authentication token
- Returns JSON response with message data

### `get_roblox_otp(content: str) -> Optional[str]`
Extracts Roblox OTP code from email content.

### `get_roblox_url(content: str) -> Optional[str]`
Extracts Roblox verification URL from email content.

## Status Codes

- 201: Account created successfully
- 422: Email address already in use
- 429: Too many requests
- 0: Error occurred during account creation

## Data Storage

Account data is automatically saved to `account_data.json` in the following format:
```json
{
    "email@tohru.org": {
        "id": "account_id",
        "address": "email@tohru.org",
        "token": "jwt_token",
        "password": "account_password",
        "quota": 40000000,
        "used": 0,
        "isDisabled": false,
        "isDeleted": false,
        "createdAt": "timestamp",
        "updatedAt": "timestamp"
    }
}
```

## Requirements

- Python 3.6+
- requests
- fake-useragent

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

