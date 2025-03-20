import json
import requests
from signing import generate_rsa_key_pair, sign_data, verify_response
import uuid
import pprint
import hashlib
import base64

class BunqClient:
    def __init__(self, api_key, service_name, base_url="https://public-api.sandbox.bunq.com/v1"):
        self.service_name = service_name
        self.api_key = api_key
        self.private_key_pem, self.public_key_pem = generate_rsa_key_pair()
        self.device_token = None
        self.server_public_key = None
        self.device_server_id = None
        self.session_token = None
        self.user_id = None
        self.base_url = base_url

        # Try to load device token from file
        self.load_device_token()

    def save_device_token(self):
        """Save the device token to a file."""
        with open('device_token.json', 'w') as file:
            json.dump({"device_token": self.device_token}, file)

    def load_device_token(self):
        """Load the device token from a file if it exists."""
        try:
            with open('device_token.json', 'r') as file:
                data = json.load(file)
                self.device_token = data.get("device_token")
                print(f"bunq - Loaded device token from file [KEEP THIS SAFE!]")
        except FileNotFoundError:
            print("bunq - No device token found, need to create a new one.")

    def create_installation(self):
        if self.device_token is not None:
            print("bunq - Device token already created.")
            return

        url = f"{self.base_url}/installation"
        payload = json.dumps({"client_public_key": self.public_key_pem})

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.service_name,
            'X-Bunq-Language': 'en_US',
            'X-Bunq-Region': 'nl_NL',
            'X-Bunq-Geolocation': '0 0 0 0 000',
        }

        response = requests.post(url, headers=headers, data=payload)
        data = response.json()

        self.device_token = next(item["Token"]["token"] for item in data["Response"] if "Token" in item)
        self.server_public_key = next(item["ServerPublicKey"]["server_public_key"] for item in data["Response"] if "ServerPublicKey" in item)
        self.save_device_token()  # Save the token for future use

    def create_device_server(self):
        if not self.device_token:
            print("bunq - Device token is required to create device server.")
            return

        url = f"{self.base_url}/device-server"
        payload = json.dumps({
            "description": self.service_name,
            "secret": self.api_key,
            "permitted_ips": ["*"]
        })
        signed_payload_signature = sign_data(payload, self.private_key_pem)

        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': self.service_name,
            'X-Bunq-Language': 'en_US',
            'X-Bunq-Region': 'nl_NL',
            'X-Bunq-Geolocation': '0 0 0 0 000',
            'X-Bunq-Client-Authentication': self.device_token,
            'X-Bunq-Client-Signature': signed_payload_signature
        }

        response = requests.post(url, headers=headers, data=payload)
        self.device_server_id = response.text

    def create_session(self):
        if not self.device_token:
            print("bunq - Device token is required to create session.")
            return

        url = f"{self.base_url}/session-server"
        payload_dict = {"secret": self.api_key}
        payload_json = json.dumps(payload_dict, separators=(',', ':'))
        signed_payload_signature = sign_data(payload_json, self.private_key_pem)
        
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': self.service_name,
            'X-Bunq-Language': 'en_US',
            'X-Bunq-Region': 'nl_NL',
            'X-Bunq-Geolocation': '0 0 0 0 000',
            'X-Bunq-Client-Authentication': self.device_token,
            'X-Bunq-Client-Signature': signed_payload_signature
        }

        response = requests.post(url, headers=headers, data=payload_json)
        data = response.json()
        print(data)
        # Extract and save session token
        self.session_token = next(item["Token"]["token"] for item in data["Response"] if "Token" in item)
        self.user_id = next(item["UserPerson"]["id"] for item in data["Response"] if "UserPerson" in item)

        print(f"bunq - Session Token: {self.session_token}")
        print(f"bunq - User ID: {self.user_id}")
        

    def request(self, endpoint: str, method: str = "GET", data: dict = None):
        url = f"{self.base_url}/user/{self.user_id}/{endpoint}"
        print(f"[DEBUG] bunq - Requesting: {method} {url}")

        # Default headers
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': self.service_name,
            'X-Bunq-Language': 'en_US',
            'X-Bunq-Region': 'nl_NL',
            'X-Bunq-Geolocation': '0 0 0 0 000',
            'X-Bunq-Client-Authentication': self.session_token,
            'X-Bunq-Client-Request-Id': str(uuid.uuid4())  # Should be unique for each request
        }

        payload = None
            
        if data and method == "POST":
            # Ensure consistent JSON formatting by using separators
            payload = json.dumps(data, separators=(',', ':'))
            signed_payload_signature = sign_data(payload, self.private_key_pem)
            headers["X-Bunq-Client-Signature"] = signed_payload_signature

            print(f"[DEBUG] Request Payload: {payload}")
            print(f"[DEBUG] Signed Payload Signature: {signed_payload_signature}")

        try:
            response = requests.request(method, url, headers=headers, data=payload)
            print(f"[DEBUG] Response Status Code: {response.status_code}")

            if response.status_code == 401:
                print("[WARNING] Unauthorized (401) - Refreshing session...")
                self.refresh_session()
                response = requests.request(method, url, headers=headers, data=payload)
                print(f"[DEBUG] Retried Response Status Code: {response.status_code}")

            if response.status_code == 200:
                response_body = response.text
                server_signature = response.headers.get('X-Bunq-Server-Signature')
                
                if server_signature and self.server_public_key:
                    # Verify the response signature
                    if not verify_response(response_body, server_signature, self.server_public_key):
                        raise Exception("Response signature verification failed")
                    print("[DEBUG] Response signature verified successfully")
                
                return response.json()

            print(f"[ERROR] Request failed: {response.status_code} - {response.text}")
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request error: {e}")
            raise
    


    def create_payment(self, amount: str, recipient_iban: str, currency: str, from_monetary_account_id: str, description: str):
        url = f"{self.base_url}/user/{self.user_id}/monetary-account/{from_monetary_account_id}/payment"

        payload = json.dumps({
            "amount": {
                "value": str(amount),
                "currency": str(currency)
            },
            "counterparty_alias": {
                "type": "EMAIL",
                "value": "sugardaddy@bunq.com",
                "name": "Sugar Daddy"
            },
            "description": str(description)
        }, separators=(',', ':'))  # Ensure consistent JSON formatting
        
        signature = sign_data(payload, self.private_key_pem)
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': self.service_name,
            'X-Bunq-Language': 'en_US',
            'X-Bunq-Region': 'nl_NL',
            'X-Bunq-Client-Request-Id': str(uuid.uuid4()),
            'X-Bunq-Geolocation': '0 0 0 0 000',
            'X-Bunq-Client-Authentication': self.session_token,
            'X-Bunq-Client-Signature': signature
        }

        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            response_body = response.text
            server_signature = response.headers.get('X-Bunq-Server-Signature')
            
            if server_signature and self.server_public_key:
                # Verify the response signature
                if not verify_response(response_body, server_signature, self.server_public_key):
                    raise Exception("Response signature verification failed")
                print("[DEBUG] Response signature verified successfully")
        
        return response.json()

                