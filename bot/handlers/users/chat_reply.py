from loader import dp, bot
from aiogram import types, F
import re
from api import send_reply_to_django
from data.config import BOT_TOKEN

@dp.message(F.reply_to_message)
async def handle_telegram_reply(message: types.Message):
    original_text = message.reply_to_message.text or message.reply_to_message.caption
    if not original_text:
        return
        
    if "#CS_" not in original_text:
        return
        
    # Extract session ID from original text
    match = re.search(r"#CS_(\d+)", original_text)
    if not match:
        return
        
    session_id = match.group(1)
    reply_text = message.text
    
    if not reply_text:
        return # Ignore non-text replies
        
    # Send it to Django
    result = await send_reply_to_django(session_id, reply_text, BOT_TOKEN)
    
    if result and result.get('success'):
        await message.reply("✅ Xabaringiz saytga yuborildi.")
    else:
        await message.reply("❌ Xabarni saytga yuborishda xatolik yuz berdi.")
