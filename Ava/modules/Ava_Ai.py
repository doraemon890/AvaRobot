import requests
import aiofiles
import aiohttp
import asyncio
import os
import uuid
import base64
import mimetypes
import shutil
from re import findall
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode, MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
from bing_image_downloader import downloader
import httpx
import config
from Ava import DEEP_API, Jarvis as app
from MukeshAPI import api
from lexica.constants import languageModels
from httpx import AsyncClient

# Ava as an Ai Assistant
@app.on_message(filters.command(["va"], prefixes=["A"]))
async def chat_gpt(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        name = message.from_user.first_name if message.from_user else "User"
        
        if len(message.command) < 2:
            await message.reply_text(f"Hello {name}, How can I help you today?")
        else:
            query = message.text.split(' ', 1)[1]
            response = api.gemini(query)["results"]
            await message.reply_text(f"{response}", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# Upscale feature
async def load_image(image_path: str, url: str) -> str:
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(image_path, mode="wb") as file:
                    await file.write(await response.read())
                return image_path
            return None

@app.on_message(filters.command("upscale", prefixes="/"))
async def upscale_image(client, message):
    chat_id = message.chat.id
    replied_message = message.reply_to_message
    
    if not DEEP_API:
        return await message.reply_text("I can't upscale without a DEEP API key!")
    
    if not replied_message or not replied_message.photo:
        return await message.reply_text("Please reply to an image.")
    
    aux_message = await message.reply_text("Upscaling, please wait...")
    image_path = await replied_message.download()
    
    response = requests.post(
        "https://api.deepai.org/api/torch-srgan",
        files={'image': open(image_path, 'rb')},
        headers={'api-key': DEEP_API}
    ).json()
    
    image_url = response.get("output_url")
    if not image_url:
        return await aux_message.edit("Failed to upscale image, please try again.")
    
    downloaded_image = await load_image(image_path, image_url)
    if not downloaded_image:
        return await aux_message.edit("Failed to download upscaled image, please try again.")
    
    await aux_message.delete()
    await message.reply_document(document=downloaded_image)

@app.on_message(filters.command("getdraw", prefixes="/"))
async def draw_image(client, message):
    chat_id = message.chat.id
    user_id = message.sender_chat.id if message.sender_chat else message.from_user.id
    replied_message = message.reply_to_message
    
    if not DEEP_API:
        return await message.reply_text("I can't generate images without a DEEP API key!")
    
    if replied_message and replied_message.text:
        query = replied_message.text
    elif len(message.text.split()) > 1:
        query = message.text.split(None, 1)[1]
    else:
        return await message.reply_text("Please provide text or reply to a text message.")
    
    aux_message = await message.reply_text("Generating image, please wait...")
    image_path = f"cache/{user_id}_{chat_id}_{message.id}.png"
    
    response = requests.post(
        "https://api.deepai.org/api/text2img",
        data={'text': query, 'grid_size': '1', 'image_generator_version': 'hd'},
        headers={'api-key': DEEP_API}
    ).json()
    
    image_url = response.get("output_url")
    if not image_url:
        return await aux_message.edit("Failed to generate image, please try again.")
    
    downloaded_image = await load_image(image_path, image_url)
    if not downloaded_image:
        return await aux_message.edit("Failed to download generated image, please try again.")
    
    await aux_message.delete()
    await message.reply_photo(photo=downloaded_image, caption=query)

# Image searching
@app.on_message(filters.command(["img", "image"], prefixes=["/", "!"]))
async def google_img_search(client: Client, message: Message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("Provide an image query to search!")

    lim = findall(r"lim=\d+", query)
    try:
        lim = int(lim[0].replace("lim=", ""))
        query = query.replace(f"lim={lim}", "")
    except IndexError:
        lim = 5  # Default limit to 5 images

    download_dir = "downloads"

    try:
        downloader.download(query, limit=lim, output_dir=download_dir, adult_filter_off=True, force_replace=False, timeout=60)
        images_dir = os.path.join(download_dir, query)
        if not os.listdir(images_dir):
            raise Exception("No images were downloaded.")
        lst = [os.path.join(images_dir, img) for img in os.listdir(images_dir)][:lim]  # Ensure we only take the number of images specified by lim
    except Exception as e:
        return await message.reply(f"Error in downloading images: {e}")

    msg = await message.reply("`Ava Scraping images...`")

    count = 0
    for img in lst:
        count += 1
        await msg.edit(f"`Ava Scrapped images {count}`")

    try:
        await app.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=img) for img in lst],
            reply_to_message_id=message.id
        )
        shutil.rmtree(images_dir)
        await msg.delete()
    except Exception as e:
        await msg.delete()
        return await message.reply(f"Error in sending images: {e}")
