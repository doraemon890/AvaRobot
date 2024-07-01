from pyrogram import Client, filters
import requests
import random
import os
from Ava import Jarvis as app

# IP Checker Feature
IPINFO_TOKEN = '434e1cea389a93'
IPQUALITYSCORE_API_KEY = '952ztTq41AxoXam43pStVjVNcEjo1ntQ'

@app.on_message(filters.command(["ip"]))
async def ip_info_and_score(client, message):
    if len(message.command) != 2:
        await message.reply_text("Please provide an IP address after the command. Example: /ip 8.8.8.8")
        return

    ip_address = message.command[1]
    ip_info = get_ip_info(ip_address)
    ip_score, score_description, emoji = get_ip_score(ip_address, IPQUALITYSCORE_API_KEY)

    if ip_info is not None and ip_score is not None:
        response_message = (
            f"{ip_info}\n\n"
            f"**IP Score** ➪ {ip_score} {emoji} ({score_description})"
        )
        await message.reply_text(response_message)
    else:
        await message.reply_text("Unable to fetch information for the provided IP address.")

def get_ip_info(ip_address):
    api_url = f"https://ipinfo.io/{ip_address}?token={IPINFO_TOKEN}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        info = (
            f"🌐 **IP** ➪ {data.get('ip', 'N/A')}\n"
            f"🏙️ **City** ➪ {data.get('city', 'N/A')}\n"
            f"📍 **Region** ➪ {data.get('region', 'N/A')}\n"
            f"🌍 **Country** ➪ {data.get('country', 'N/A')}\n"
            f"📌 **Location** ➪ {data.get('loc', 'N/A')}\n"
            f"🏢 **Organization** ➪ {data.get('org', 'N/A')}\n"
            f"📮 **Postal Code** ➪ {data.get('postal', 'N/A')}\n"
            f"⏰ **Timezone** ➪ {data.get('timezone', 'N/A')}"
        )
        return info
    except requests.RequestException as e:
        print(f"Error fetching IP information: {e}")
    return None

def get_ip_score(ip_address, api_key):
    api_url = f"https://ipqualityscore.com/api/json/ip/{api_key}/{ip_address}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        fraud_score = data.get('fraud_score', 'N/A')
        if fraud_score != 'N/A':
            fraud_score = int(fraud_score)
            if fraud_score <= 20:
                score_description = 'Good'
                emoji = '✅'
            elif fraud_score <= 60:
                score_description = 'Moderate'
                emoji = '⚠️'
            else:
                score_description = 'Bad'
                emoji = '❌'
            return fraud_score, score_description, emoji
    except requests.RequestException as e:
        print(f"Error fetching IP score: {e}")
    return None, None, None

@app.on_message(filters.command(["genip"]))
async def generate_ip_handler(client, message):
    if len(message.command) != 2 or not message.command[1].isdigit():
        await message.reply_text("Please provide a valid number of IPs to generate. Example: /genip 1000")
        return
    
    number_of_ips = int(message.command[1])
    status_message = await message.reply_text(f"Generating {number_of_ips} IP addresses...")

    generated_ips = generate_ip_addresses(number_of_ips)
    
    await status_message.delete()

    if number_of_ips <= 20:
        ip_list_message = "\n".join(generated_ips)
        try:
            await message.reply_text(f"Generated {number_of_ips} IP addresses:\n{ip_list_message}")
        except Exception as e:
            print(f"Error sending message: {e}")
    else:
        file_path = save_ips(generated_ips)
        try:
            await message.reply_document(file_path)
        except Exception as e:
            print(f"Error sending document: {e}")
        os.remove(file_path)

def generate_ip_addresses(n):
    return [".".join(map(str, (random.randint(0, 255) for _ in range(4)))) for _ in range(n)]

def save_ips(ip_list):
    file_path = 'generated_ips.txt'
    with open(file_path, 'w') as f:
        for ip in ip_list:
            f.write(f"{ip}\n")
    return file_path

@app.on_message(filters.command(["chkip"]))
async def check_ips_handler(client, message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to a message containing IP addresses or a document to check.")
        return
    
    if message.reply_to_message.document:
        file_path = await message.reply_to_message.download()
        ip_list = extract_ips_from_file(file_path)
        os.remove(file_path)
    else:
        ip_text = message.reply_to_message.text
        ip_list = extract_ips(ip_text)

    if not ip_list:
        await message.reply_text("No valid IP addresses found.")
        return
    
    status_message = await message.reply_text(f"Checking {len(ip_list)} IP addresses...")

    checked_ips = check_ips(ip_list)
    
    await status_message.delete()
    
    file_path = save_checked_ips(checked_ips)
    await message.reply_document(file_path)
    os.remove(file_path)

def extract_ips(text):
    return [ip.strip() for ip in text.split() if is_valid_ip(ip.strip())]

def extract_ips_from_file(file_path):
    with open(file_path, 'r') as f:
        return [ip for line in f for ip in extract_ips(line)]

def is_valid_ip(ip):
    parts = ip.split(".")
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

def check_ips(ip_list):
    checked_ips = []
    for ip in ip_list:
        ip_info = get_ip_info(ip)
        ip_score, score_description, emoji = get_ip_score(ip, IPQUALITYSCORE_API_KEY)
        checked_ips.append(f"{ip}: {ip_info} - Score: {ip_score} {emoji} ({score_description})")
    return checked_ips

def save_checked_ips(checked_ips):
    file_path = 'checked_ips.txt'
    with open(file_path, 'w') as f:
        for ip in checked_ips:
            f.write(f"{ip}\n")
    return file_path
