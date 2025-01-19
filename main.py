from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
import fake_useragent
import requests
import string
import random
import json
import os
import re

class TempMail:
    """A class to handle temporary email operations using mail.tm API."""
    
    def __init__(self):
        self.api_url = "https://api.mail.tm"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": fake_useragent.UserAgent().random
        })

    def create_account(self, email: str, password: str) -> int:
        """Create a new temporary email account."""
        payload = {"address": email, "password": password}
        try:
            response = self.session.post(
                f"{self.api_url}/accounts", 
                json=payload, 
                timeout=10
            )
            if response.status_code == 201:
                response_data = response.json()
                token_response = self.session.post(
                    f"{self.api_url}/token", 
                    json=payload, 
                    timeout=10
                )
                token = token_response.json().get("token")
                self.save_to_json({
                    response_data['address']: {
                        **response_data,
                        "token": token,
                        "password": password
                    }
                })
            return response.status_code
        except Exception as e:
            print(f"Error creating account: {e}")
            return 0

    def save_to_json(self, data: Dict[str, Any]) -> None:
        """Save account data to a JSON file."""
        filepath = 'account_data.json'
        existing_data = {}
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as json_file:
                existing_data = json.load(json_file)

        existing_data.update(data)
        
        with open(filepath, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

    def read_all_messages(self, token: str) -> Dict[str, Any]:
        """Read all messages for an account."""
        headers = {"Authorization": f"Bearer {token}"}
        messages_response = self.session.get(
            f"{self.api_url}/messages", 
            headers=headers
        )
        latest_message_id = messages_response.json()["hydra:member"][0]["id"]
        
        response = self.session.get(
            f"{self.api_url}/messages/{latest_message_id}", 
            headers=headers
        )
        return response.json()

def create_random_account() -> None:
    """Create a random temporary email account."""
    temp_mail = TempMail()
    email = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@tohru.org"
    password = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    status = temp_mail.create_account(email, password)
    print(f"Account creation status: {status}")

def main():
    """Example usage of the TempMail class."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_random_account) for _ in range(3)]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
