import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import os
import time

# ---------------- CLI ---------------- #

parser = argparse.ArgumentParser(description="S3 Bucket Key Validator")

parser.add_argument("-i", "--input", required=True, help="XML file")
parser.add_argument("-u", "--url", required=True, help="Base URL (örn: https://content.site.com)")
parser.add_argument("-o", "--output", default="result", help="Output prefix")
parser.add_argument("-t", "--threads", type=int, default=10, help="Thread count")

args = parser.parse_args()

BASE_URL = args.url.rstrip("/")
INPUT_FILE = args.input
THREADS = args.threads
OUTPUT = args.output

# ---------------- HEADERS ---------------- #

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Connection": "close"
}

# ---------------- XML PARSE ---------------- #

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    xml_data = f.read()

root = ET.fromstring(xml_data)
ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}

keys = []

for content in root.findall("s3:Contents", ns):
    key = content.find("s3:Key", ns).text.strip()

    key = key.replace("//", "/")

    if not key.startswith("/"):
        key = "/" + key

    keys.append(key)

print(f"[+] {len(keys)} key bulundu\n")

# ---------------- STORAGE ---------------- #

ok200 = []
ok403 = []
ok404 = []
errors = []

# ---------------- REQUEST ---------------- #

def request_url(url):

    retry = 2

    for _ in range(retry):
        try:
            r = requests.get(
                url,
                headers=HEADERS,
                timeout=10,
                verify=False
            )

            return r.status_code

        except Exception as e:
            last_error = str(e)
            time.sleep(1)

    return f"ERROR | {last_error}"


def test_key(key):

    url = BASE_URL + key
    status = request_url(url)

    return status, url


# ---------------- THREAD EXECUTION ---------------- #

total = len(keys)
count = 0

with ThreadPoolExecutor(max_workers=THREADS) as executor:

    futures = [executor.submit(test_key, k) for k in keys]

    for future in as_completed(futures):

        status, url = future.result()
        count += 1

        print(f"[{count}/{total}] ", end="")

        if status == 200:
            print(f"[200] {url}")
            ok200.append(url)

        elif status == 403:
            print(f"[403] {url}")
            ok403.append(url)

        elif status == 404:
            print(f"[404] {url}")
            ok404.append(url)

        else:
            print(f"[!] {status} -> {url}")
            errors.append(f"{url} | {status}")

# ---------------- OUTPUT ---------------- #

os.makedirs("output", exist_ok=True)

def save(name, data):
    with open(f"output/{OUTPUT}_{name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(data))

save("200", ok200)
save("403", ok403)
save("404", ok404)
save("errors", errors)

print("\n[✓] Scan tamamlandı")
