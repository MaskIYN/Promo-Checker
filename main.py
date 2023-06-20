import ctypes
import os
import queue
import random
import threading
import time
from datetime import datetime
import tls_client
from colorama import Fore, Style, init


os.system('cls' if os.name == 'nt' else 'clear')
ctypes.windll.kernel32.SetConsoleTitleW("Promo Checker Made by Switch#4377")


class Console:
    @staticmethod
    def valid(code, days_left, expires_at, typee):
        init()
        current_date = datetime.now().strftime('%H:%M:%S')
        print(Fore.WHITE + current_date + Style.RESET_ALL + Fore.GREEN + f" [VALID] " + Fore.RESET +
              Fore.LIGHTBLACK_EX + "Code : " + Fore.RESET + f"{code[:10]}...." + Fore.LIGHTBLACK_EX +
              " Days left : " + Fore.RESET + str(days_left) + Fore.LIGHTBLACK_EX + " Expires at :" +
              Fore.RESET + str(expires_at) + Fore.LIGHTBLACK_EX + " Type :" + Fore.RESET + str(typee) + Style.RESET_ALL)

    @staticmethod
    def invalid(code, reason=None):
        init()
        current_date = datetime.now().strftime('%H:%M:%S')
        print(Fore.WHITE + current_date + Style.RESET_ALL + Fore.RED + f" [INVALID] " + Fore.RESET +
              Fore.LIGHTBLACK_EX + "Code : " + Fore.RESET + f"{code[:10]}...." + " Reason : " +
              str(reason) + Style.RESET_ALL)

    @staticmethod
    def error(code):
        init()
        current_date = datetime.now().strftime('%H:%M:%S')
        print(Fore.WHITE + current_date + Style.RESET_ALL + Fore.RED + f" [ERROR] " + Fore.RESET +
              Fore.LIGHTBLACK_EX + "Code : " + Fore.RESET + f"{code[:10]}...." + Style.RESET_ALL)

    @staticmethod
    def rate_limit(code, time):
        init()
        current_date = datetime.now().strftime('%H:%M:%S')
        print(Fore.WHITE + current_date + Style.RESET_ALL + Fore.RED + f" [RATE LIMIT] " + Fore.RESET +
              Fore.LIGHTBLACK_EX + "Code : " + Fore.RESET + f"{code[:10]}...." + " Time : " +
              str(time) + Style.RESET_ALL)

    @staticmethod
    def info(info):
        init()
        current_date = datetime.now().strftime('%H:%M:%S')
        print(Fore.WHITE + current_date + Style.RESET_ALL + Fore.YELLOW + f" [INFO] " + Fore.RESET +
              Fore.LIGHTBLACK_EX + "Info : " + Fore.RESET + f"{info}" + Style.RESET_ALL)


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date_str = date_obj.strftime('%d/%m/%Y')
    return formatted_date_str


def date_diff(date2_str):
    date1 = datetime.now()
    date2 = datetime.strptime(date2_str, '%d/%m/%Y')
    delta = date2 - date1
    return delta.days


useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

init()

with open("input/codes.txt", "r") as f:
    codes = f.read().splitlines()

unique_codes = list(set(codes))
duplicates = len(codes) - len(unique_codes)

with open("input/codes.txt", "w") as f:
    for code in unique_codes:
        f.write(code + "\n")

Console.info(f"{duplicates} duplicates removed")
time.sleep(1)

if not os.path.exists('output'):
    os.mkdir('output')


def get_random_line():
    with open('data/tokens.txt', 'r') as f:
        lines = f.readlines()
        return random.choice(lines)


def center_text(text: str, space: int = None):
    if not space:
        space = (os.get_terminal_size().columns - len(text.splitlines()[int(len(text.splitlines()) / 2)])) / 2
    return "\n".join((' ' * int(space)) + var for var in text.splitlines())


total = len(open('input/codes.txt').readlines())
valid = 0
invalid = 0


def remove_line(arg: str):
    with open('input/codes.txt', "r") as f:
        lines = f.readlines()
    with open('input/codes.txt', "w") as f:
        for line in lines:
            if line.strip("\n") != arg:
                f.write(line)


def title():
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Promo Checker | Total Loaded: {str(total)} | Valid:{str(valid)} | Invalid: {str(invalid)}")


class Checker:
    def __init__(self, code):
        global valid
        global invalid
        self.token = get_random_line()
        self.ja3 = '771,4866-4867-4865-159-61-52393-158-49162-49195-103-60-156-57-52394-47-49200-49172-49187-49171-107-51-49199-53-52392-49192-49191-157-49188-49196-49161-255,0-11-10-35-16-22-23-13-43-45-51-21,29-23-30-25-24,0-1-2'
        self.client = tls_client.Session(
            client_identifier="chrome_109",
            ja3_string=self.ja3,
            h2_settings={
                "HEADER_TABLE_SIZE": 65536,
                "MAX_CONCURRENT_STREAMS": 1000,
                "INITIAL_WINDOW_SIZE": 6291456,
                "MAX_HEADER_LIST_SIZE": 262144
            },
            h2_settings_order=["HEADER_TABLE_SIZE", "MAX_CONCURRENT_STREAMS", "INITIAL_WINDOW_SIZE",
                               "MAX_HEADER_LIST_SIZE"],
            supported_signature_algorithms=["ECDSAWithP256AndSHA256", "PSSWithSHA256", "PKCS1WithSHA256",
                                            "ECDSAWithP384AndSHA384", "PSSWithSHA384", "PKCS1WithSHA384",
                                            "PSSWithSHA512", "PKCS1WithSHA512", ],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
            connection_flow=15663105,
            header_order=["accept", "user-agent", "accept-encoding", "accept-language"]
        )
        self.useragent = useragent
        self.code = code.strip('\n').replace('https://discord.com/billing/promotions/', '').replace(
            'https://promos.discord.gg/', '').replace('/', '').replace('\n', '')
        self.url = f"https://discord.com/api/v9/entitlements/gift-codes/{self.code}?with_application=false&with_subscription_plan=true"
        self.path = self.url.replace('https://discordapp.com', '').strip('\n')
        self.cookie_str = self.client.get("https://discord.com/").cookies
        try:
            dcf = str(self.cookie_str).split('__dcfduid=')[1].split(' ')[0]
            sdc = str(self.cookies_str).split('__sdcfduid=')[1].split(' ')[0]
            self.cookies = f'__dcfduid={dcf}; __sdcfduid={sdc}'
        except:
            self.cookies = None
            if self.cookies is None:
                self.headers = {
                    'authority': 'discordapp.com',
                    "authorization": self.token.strip('\n'),
                    'method': 'GET',
                    'path': self.path,
                    'scheme': 'https',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.8',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Brave";v="108"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': useragent,
                }
            else:
                self.headers = {
                    'authority': 'discordapp.com',
                    'method': 'GET',
                    'path': self.path,
                    'scheme': 'https',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.8',
                    'cache-control': 'max-age=0',
                    'cookie': self.cookies,
                    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Brave";v="108"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': useragent,
                }

        r = self.client.get(self.url, headers=self.headers)
        if r.status_code == 200:
            try:
                ree = r.text
                re = r.json()
            except:
                print(r.text)
            if '3 months of Nitro' in ree:
                self.type = '3 Months'
            else:
                self.type = '1 Months'
            expiry = re["expires_at"][:10]
            redeemed = re["uses"]

            if redeemed == 0:
                days_left = date_diff(format_date(expiry))
                valid += 1
                title()
                Console.valid(self.code, days_left=days_left, expires_at=expiry, typee=self.type)
                remove_line(self.code)
                open("output/valid.txt", 'a').write("https://discord.com/billing/promotions/" + self.code + '\n')
            else:
                invalid += 1
                remove_line(self.code)
                title()
                Console.invalid(self.code, reason="Already Redeemed")
        elif r.status_code == 429:
            nig = r.json()
            sax = int(nig['retry_after'])
            Console.rate_limit(code=self.code, time=str(sax))
            time.sleep(sax)
            Checker(self.code)
        else:
            invalid += 1
            title()
            Console.invalid(code=self.code, reason="Incorrect code")
            remove_line(self.code)


os.system("cls")
title()


def worker():
    while True:
        try:
            code = codes_queue.get(block=False)
        except queue.Empty:
            break
        checker = Checker(code)
        codes_queue.task_done()


codes_queue = queue.Queue()

with open('input/codes.txt') as f:
    for code in f:
        codes_queue.put(code.strip())

workers = []

for _ in range(20):
    t = threading.Thread(target=worker)
    t.start()
    workers.append(t)

for t in workers:
    t.join()

Console.info(f"Valid: {valid} | Invalid: {invalid}")
Console.info("Enter any Key to exit")
input('                                     ')
