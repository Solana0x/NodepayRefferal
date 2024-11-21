import asyncio
import time
import random
import csv
import string
from typing import Optional, Tuple, Dict
import requests
from colorama import Fore, Style, init
from datetime import datetime
from twocaptcha import TwoCaptcha

init(autoreset=True)
def log_step(message: str, type: str = "info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "info": Fore.LIGHTBLUE_EX,
        "success": Fore.GREEN,
        "error": Fore.LIGHTRED_EX,
        "warning": Fore.YELLOW
    }
    emojis = {
        "info": "ℹ️",          # Information emoji
        "success": "✅",       # Success check mark
        "error": "❌",         # Error cross mark
        "warning": "⚠️"        # Warning symbol
    }
    color = colors.get(type, Fore.WHITE)
    emoji = emojis.get(type, "•")
    print(f"{Fore.LIGHTWHITE_EX}[{timestamp}] {color}{emoji} {message}{Style.RESET_ALL}")

class CaptchaConfig:
    WEBSITE_KEY = '0x4AAAAAAAx1CyDNL8zOEPe7'
    WEBSITE_URL = 'https://app.nodepay.ai/login'
class Service2Captcha:
    def __init__(self, api_key):
        self.solver = TwoCaptcha(api_key)
    
    async def get_captcha_token_async(self):
        result = await asyncio.to_thread(
            lambda: self.solver.turnstile(
                sitekey=CaptchaConfig.WEBSITE_KEY,
                url=CaptchaConfig.WEBSITE_URL
            )
        )
        return result['code']
class ProxyManager:
    def __init__(self, proxy_list: list):
        self.proxies = proxy_list
        self.current_index = -1
        self.total_proxies = len(proxy_list) if proxy_list else 0
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        if not self.proxies:
            return None
        self.current_index = (self.current_index + 1) % self.total_proxies
        proxy = self.proxies[self.current_index]
        return {"http": proxy, "https": proxy}

class ApiEndpoints:
    BASE_URL = "https://api.nodepay.ai/api"
    @classmethod
    def get_url(cls, endpoint: str) -> str:
        return f"{cls.BASE_URL}/{endpoint}"
    class Auth:
        REGISTER = "auth/register"
        LOGIN = "auth/login"
        ACTIVATE = "auth/active-account"
class LoginError(Exception):
    pass
class ReferralClient:
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        self.proxy_manager = proxy_manager
        self.current_proxy = None
        self.credentials_list = []
        self.current_index = -1
    def _load_credentials(self) -> bool:
        try:
            if not self.credentials_list:
                with open('reg.txt', 'r') as f_reg:
                    self.credentials_list = [line.strip().split(",") for line in f_reg if line.strip()]
            if len(self.credentials_list) == 0:
                log_step("Credential file (reg.txt) is empty.", "error")
                return False
            self.current_index = (self.current_index + 1) % len(self.credentials_list)
            self.email, self.password, self.username = self.credentials_list[self.current_index]
            return True
        except FileNotFoundError:
            log_step("Credential file (reg.txt) not found.", "error")
            return False
    def _update_proxy(self):
        if self.proxy_manager:
            self.current_proxy = self.proxy_manager.get_next_proxy()
            if self.current_proxy:
                proxy_addr = self.current_proxy['http']
                log_step(f"Using proxy: {proxy_addr}", "info")
    def _get_headers(self, auth_token: Optional[str] = None) -> Dict[str, str]:
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://app.nodepay.ai',
            'priority': 'u=1, i',
            'referer': 'https://app.nodepay.ai/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        if auth_token:
            headers['Authorization'] = f'Bearer {auth_token}'
            headers['origin'] = 'chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm'
        return headers 
    async def _make_request(self, method: str, endpoint: str, json_data: dict, auth_token: Optional[str] = None) -> dict:
        self._update_proxy()
        headers = self._get_headers(auth_token)
        url = ApiEndpoints.get_url(endpoint)

        try:
            response = await asyncio.to_thread(
                lambda: requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_data,
                    proxies=self.current_proxy,
                    timeout=30
                )
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            log_step(f"Request failed: {str(e)}", "error")
            return {"success": False, "msg": str(e)}

    async def login(self, captcha_service) -> str:
        try:
            log_step("Getting captcha token for login...", "info")
            captcha_token = await captcha_service.get_captcha_token_async()
            log_step("Captcha token obtained", "success")

            json_data = {
                'user': self.email,
                'password': self.password,
                'remember_me': True,
                'recaptcha_token': captcha_token
            }

            log_step("Attempting login...", "info")
            response = await self._make_request(
                method='POST',
                endpoint=ApiEndpoints.Auth.LOGIN,
                json_data=json_data
            )

            if not response.get("success"):
                msg = response.get("msg", "Unknown login error")
                log_step(f"Login failed: {msg}", "error")
                raise LoginError(msg)

            access_token = response['data']['token']
            log_step("Login successful", "success")
            return access_token

        except Exception as e:
            log_step(f"Login error: {str(e)}", "error")
            raise

    async def activate_account(self, access_token: str):
        try:
            log_step("Attempting account activation...", "info")
            response = await self._make_request(
                method='POST',
                endpoint=ApiEndpoints.Auth.ACTIVATE,
                json_data={},
                auth_token=access_token
            )

            if response.get("success"):
                log_step(f"Account activation successful: {response.get('msg', 'Success')}", "success")
            else:
                log_step(f"Account activation failed: {response.get('msg', 'Unknown error')}", "error")

            return response

        except Exception as e:
            log_step(f"Activation error: {str(e)}", "error")
            raise
        
    async def process_referral(self, ref_code: str, captcha_service, referral_number: int) -> Optional[Dict]:
        try:
            if not self._load_credentials():
                return None          
            log_step(f" Loaded credentials for: {self.email}", "info")
            log_step(" Getting captcha token...", "info")
            captcha_token = await captcha_service.get_captcha_token_async()
            log_step("Captcha token obtained", "success")        
            register_data = {
                'email': self.email,
                'password': self.password,
                'username': self.username,
                'referral_code': ref_code,
                'recaptcha_token': captcha_token
            }
            log_step(" Registering account...", "info")
            register_response = await self._make_request('POST', ApiEndpoints.Auth.REGISTER, register_data)
            if register_response.get("success"):
                log_step(f"Registration successful: {register_response.get('msg', 'Success')}", "success")   
                access_token = await self.login(captcha_service)   
                activation_response = await self.activate_account(access_token)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('accounts.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([referral_number, self.email, self.password, self.username, access_token, timestamp])
                return {
                    "username": self.username,
                    "email": self.email,
                    "password": self.password,
                    "referral_code": ref_code,
                    "token": access_token,
                    "activation_status": activation_response.get('success', False),
                    "activation_message": activation_response.get('msg', 'Unknown')
                }
            else:
                log_step(f"Registration failed: {register_response.get('msg', 'Unknown error')}", "error")
                return None

        except Exception as e:
            log_step(f"Error processing referral: {str(e)}", "error")
            return None
async def main():
    referral_codes = ["mjIpmj2MWwKKyjz", "FFbRTqtmtKos6Dr", "28Z4fXIg2KkGGAn", "AM1A6dUEocMlSOH", "sMW33yLLziigDOR"] #enter your refferal code of the nodepay here !
    api_key = "2captcha API KEY" #enter your 2cpatcha API key
    with open('reg.txt', 'r') as f_reg:
        credentials_list = [line.strip() for line in f_reg if line.strip()]
    num_referrals = len(credentials_list)
    use_proxies = True
    proxy_manager = None
    
    if use_proxies:
        try:
            with open('proxies.txt', 'r') as f:
                proxy_list = [line.strip() for line in f if line.strip()]
            proxy_manager = ProxyManager(proxy_list)
            log_step(f"Loaded {len(proxy_list)} proxies", "success")
        except FileNotFoundError:
            log_step("proxies.txt not found. Running without proxies.", "warning")

    captcha_service = Service2Captcha(api_key)
    log_step(" Captcha service initialized", "success")

    # Create CSV file and write headers if it doesn't exist
    with open('accounts.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["S.NO", "EMAIL", "PASS", "USERNAME", "ACCESS_TOKEN", "TIMESTAMP"])
    client = ReferralClient(proxy_manager)
    successful_referrals = []
    log_step(" Starting referral process...", "info")
    for i in range(num_referrals):
        ref_code = random.choice(referral_codes)
        batch_size = min(1, num_referrals - i)
        tasks = [
            client.process_referral(ref_code, captcha_service, referral_number=i + j + 1)
            for j in range(batch_size)
        ]

        results = await asyncio.gather(*tasks)
        for result in results:
            if result:
                log_step("Account details:", "success")
                print(f"{Fore.LIGHTCYAN_EX}Username: {Fore.WHITE}{result['username']}")
                print(f"{Fore.LIGHTCYAN_EX}Email: {Fore.WHITE}{result['email']}")
                print(f"{Fore.LIGHTCYAN_EX}Password: {Fore.WHITE}{result['password']}")
                print(f"{Fore.LIGHTCYAN_EX}Referred to: {Fore.WHITE}{result['referral_code']}")
                print(f"{Fore.LIGHTCYAN_EX}Token: {Fore.WHITE}{result['token']}")
                successful_referrals.append(result)
                with open('accounts.txt', 'a') as f:
                    f.write(f"Email: {result['email']}\n")
                    f.write(f"Password: {result['password']}\n")
                    f.write(f"Username: {result['username']}\n")
                    f.write(f"Referred to: {result['referral_code']}\n")
                    f.write(f"Token: {result['token']}\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("-" * 50 + "\n")
        if i + batch_size < num_referrals:
            delay = random.uniform(2, 5)
            log_step(f" Waiting {delay:.2f} seconds before next batch...", "info")
            await asyncio.sleep(delay)
    print(f"\n{Fore.LIGHTCYAN_EX}{'='*45}")
    log_step("Summary:", "info")
    log_step(f"Total attempted: {num_referrals}", "info")
    log_step(f"Successful: {len(successful_referrals)}", "success")
    print(f"{Fore.LIGHTCYAN_EX}{'='*45}\n")
if __name__ == "__main__":
    asyncio.run(main())
