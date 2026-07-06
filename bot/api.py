import aiohttp
from environs import Env
env = Env()
env.read_env()
URL =env.str('URL')
import asyncio


async def get_user(telegram_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{URL}/user/", data={'telegram_id': telegram_id}) as response:
                if response.status == 204:
                    return "Not found"
                data = await response.json()
                return data
        except:
            return {}

async def create_user(telegram_id: str, language='uz', name: str = None):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{URL}/botuser/", data={'telegram_id': telegram_id, 'name': name, 'language': language}) as response:
                if response.status == 201:
                    data = await response.json()
                    return data
                else:
                    error_message = await response.text()
                    print(f"Failed to create user: {response.status} - {error_message}")
                    return "User creation failed"
        except Exception as e:
            print(f"Exception occurred: {e}")
            return "Error"

async def get_all_users():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{URL}/botuser/") as response:
                data = await response.json()
                return data
        except:
            return []

async def users_count():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{URL}/botuser") as response:
                # data = await response.json()
                if response.status == 200:
                    data = await response.json()
                    count = len(data)
                    return count
        except:
            return 0

async def change_user_language(telegram_id, language):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/lang/", data={'telegram_id': telegram_id, 'language': language}) as response:
                if response.status == 204:
                    return 'Not Found'
                else:
                    return await response.json()
        except:
            return None

async def add_channel(channel_id: str, channel_name: str = None, channel_members_count: str = None):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/channels/", data={'channel_id': channel_id, 'channel_name': channel_name, 'channel_members_count': channel_members_count}) as response:
                if response.status == 201:
                    return 'ok'
                else:
                    return 'bad'
        except:
            return None

async def get_all_channels():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=f"{URL}/channels/") as response:
                return await response.json()
        except:
            return []

async def get_channel(channel_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/channel/", data={'channel_id': channel_id}) as response:
                if response.status == 206:
                    return await response.json()
                else:
                    return {}
        except:
            return {}

async def delete_channel(channel_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/delete_channel/", data={'channel_id': channel_id}) as response:
                if response.status == 200:
                    return 'Ok'
                else:
                    return "Bad"
        except:
            return "Bad"

async def send_reply_to_django(session_id, message_text, bot_token):
    # Determine Django base url by removing /api from the URL variable
    base_url = URL.replace('/api', '')
    endpoint = f"{base_url}/chat/reply-from-telegram/"
    
    headers = {
        'Authorization': f'Bearer {bot_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'session_id': session_id,
        'message': message_text
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(endpoint, headers=headers, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    err_txt = await response.text()
                    print(f"Failed to send reply to Django: {response.status} - {err_txt}")
                    return None
        except Exception as e:
            print(f"Exception during django reply post: {e}")
            return None

