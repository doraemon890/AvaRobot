import os
import aiohttp
import aiofiles
import re
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import whois

from Ava import BOT_NAME, BOT_USERNAME
from Ava import Jarvis as app

# MongoDB URL Pattern
mongo_url_pattern = re.compile(r'mongodb(?:\+srv)?:\/\/[^\s]+')

# MongoDB Checker Command
@app.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please enter your MongoDB URL after the command. Example: /mongochk your_mongodb_url")
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            # Attempt to connect to the MongoDB instance
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()  # Will cause an exception if connection fails
            await message.reply("MongoDB URL is valid and connection successful ✅")
        except Exception as e:
            await message.reply(f"Failed to connect to MongoDB: {e}")
    else:
        await message.reply("Invalid MongoDB URL format 💔")


# Remove Background Feature
API_KEY = "23nfCEipDijgVv6SH14oktJe"

def check_filename(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid

async def remove_bg(input_file_name):
    headers = {"X-API-Key": API_KEY}
    files = {"image_file": open(input_file_name, "rb").read()}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.remove.bg/v1.0/removebg", headers=headers, data=files
        ) as response:
            content_type = response.headers.get("content-type")
            if "image" not in content_type:
                return False, (await response.json())

            name = check_filename("alpha.png")
            file = await aiofiles.open(name, "wb")
            await file.write(await response.read())
            await file.close()
            return True, name

@app.on_message(filters.command("rmbg"))
async def rmbg(bot, message):
    rmbg_message = await message.reply("Processing...") 
    replied = message.reply_to_message
    if not replied or not replied.photo:
        return await rmbg_message.edit("Reply to a photo to remove its background")

    photo = await bot.download_media(replied)
    success, result = await remove_bg(photo)
    os.remove(photo)
    if not success:
        error = result["errors"][0]
        details = error.get("detail", "")
        return await rmbg_message.edit(f"ERROR ~ {error['title']},\n{details}")

    await message.reply_photo(photo=result, caption="Here is your image without background")
    await message.reply_document(document=result)
    await rmbg_message.delete()
    os.remove(result)


# Domain Checker Feature
def get_domain_hosting_info(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        return domain_info
    except whois.parser.PywhoisError as e:
        print(f"Error: {e}")
        return None

@app.on_message(filters.command("domain"))
async def get_domain_info(client, message):
    if len(message.command) > 1:
        domain_name = message.text.split("/domain ", 1)[1]
        domain_info = get_domain_hosting_info(domain_name)

        if domain_info:
            response = (
                f"Domain Name: {domain_info.domain_name}\n"
                f"Registrar: {domain_info.registrar}\n"
                f"Creation Date: {domain_info.creation_date}\n"
                f"Expiration Date: {domain_info.expiration_date}"
                # Add more details as needed
            )
        else:
            response = "Failed to retrieve domain hosting information."

        await message.reply(response)
    else:
        await message.reply("Please provide a site link or name after the /domain command.")


# PyPI Info Checker Feature
def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(api_url)
        pypi_info = response.json()
        return pypi_info
    except Exception as e:
        print(f"Error fetching PyPI information: {e}")
        return None

@app.on_message(filters.command("pypi"))
async def pypi_info_command(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a package name after the /pypi command.")
        return

    package_name = message.command[1]
    pypi_info = get_pypi_info(package_name)

    if pypi_info:
        info_message = f"Package Name ➪ {pypi_info['info']['name']}\n\n" \
                       f"Latest Version ➪ {pypi_info['info']['version']}\n\n" \
                       f"Description ➪ {pypi_info['info']['summary']}\n\n" \
                       f"Project URL ➪ {pypi_info['info']['project_urls']['Homepage']}"
        await message.reply(info_message)
    else:
        await message.reply("Failed to fetch information from PyPI.")


# GPS Location Feature
@app.on_message(filters.command(["gps"]))
async def gps(bot, message):
    if len(message.command) < 2:
        return await message.reply_text("Example:\n\n/gps [latitude, longitude]")
    
    coordinates = message.text.split(' ')[1].split(',')
    try:
        geolocator = Nominatim(user_agent="legend-jarvis")
        location = geolocator.reverse(coordinates, addressdetails=True, zoom=18)
        address = location.raw['address']

        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        latitude = location.latitude
        longitude = location.longitude

        url = [[InlineKeyboardButton("Open with: 🌏 Google Maps", url=f"https://www.google.com/maps/search/{latitude},{longitude}")]]
        await message.reply_venue(latitude, longitude, city, f"{state}, {country}", reply_markup=InlineKeyboardMarkup(url))
    except Exception as e:
        await message.reply_text(f"I can't find that location \nDue to: {e}")


# Distance Calculator Feature
@app.on_message(filters.command(["distance"]))
async def distance(bot, message):
    if len(message.command) < 2:
        return await message.reply_text("Example:\n\n/distance [latitude, longitude],[latitude, longitude]")

    try:
        points = message.text.split(" ")[1].split(',')
        x = points[0:2]
        y = points[2:4]
        dist = great_circle(x, y).miles

        await message.reply_text(f"Total distance between {x[0]},{x[1]} and {y[0]},{y[1]} is {dist} miles")
    except Exception as e:
        await message.reply_text(f"I can't calculate that distance \nDue to: {e}")

