# main.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import BOT_TOKENS, OWNER_ID, PRIVATE_CHANNEL_ID
from utils import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKENS[0])
dp = Dispatcher(bot)

LAST_EPISODE_MSG_ID = None

# /start
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📥 Get Episode", callback_data="get_ep"))
    await msg.answer("👋 Welcome! Click below to receive the latest episode.", reply_markup=kb)

# Help
@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("👑 Owner", callback_data="help_owner"),
        InlineKeyboardButton("🛠 Admin", callback_data="help_admin"),
        InlineKeyboardButton("🙋‍♂️ User", callback_data="help_user")
    )
    await msg.answer("ℹ️ Choose your role to get help:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("help_"))
async def help_section(cb: types.CallbackQuery):
    role = cb.data.split("_")[1]
    if role == "owner":
        if cb.from_user.id != OWNER_ID:
            await cb.message.edit_text("❌ Only the owner can access this help.")
            return
        await cb.message.edit_text("""
👑 Owner Help:
/addadmin <user_id>
/removeadmin <user_id>
/addchannel <channel_id>
/removechannel <channel_id>
        """)
    elif role == "admin":
        if cb.from_user.id not in get_admins():
            await cb.message.edit_text("❌ Only admins can access this help.")
            return
        await cb.message.edit_text("""
🛠 Admin Help:
Just send a video (episode) with caption. Bot will auto-post to private channel and update it for users.
        """)
    else:
        await cb.message.edit_text("""
🙋‍♂️ User Help:
Click "📥 Get Episode". You must join all required channels first to receive the file.
        """)

# Owner Commands
@dp.message_handler(lambda msg: msg.from_user.id == OWNER_ID and msg.text.startswith("/addadmin"))
async def add_admin_cmd(msg: types.Message):
    try:
        uid = int(msg.text.split()[1])
        add_admin(uid)
        await msg.reply(f"✅ Admin {uid} added.")
    except:
        await msg.reply("❌ Usage: /addadmin <user_id>")

@dp.message_handler(lambda msg: msg.from_user.id == OWNER_ID and msg.text.startswith("/removeadmin"))
async def remove_admin_cmd(msg: types.Message):
    try:
        uid = int(msg.text.split()[1])
        remove_admin(uid)
        await msg.reply(f"✅ Admin {uid} removed.")
    except:
        await msg.reply("❌ Usage: /removeadmin <user_id>")

@dp.message_handler(lambda msg: msg.from_user.id == OWNER_ID and msg.text.startswith("/addchannel"))
async def add_channel_cmd(msg: types.Message):
    try:
        cid = msg.text.split()[1]
        add_channel(cid)
        await msg.reply(f"✅ Channel {cid} added.")
    except:
        await msg.reply("❌ Usage: /addchannel <channel_id>")

@dp.message_handler(lambda msg: msg.from_user.id == OWNER_ID and msg.text.startswith("/removechannel"))
async def remove_channel_cmd(msg: types.Message):
    try:
        cid = msg.text.split()[1]
        remove_channel(cid)
        await msg.reply(f"✅ Channel {cid} removed.")
    except:
        await msg.reply("❌ Usage: /removechannel <channel_id>")

# Admin Upload
@dp.message_handler(lambda msg: msg.from_user.id in get_admins() and msg.video)
async def receive_episode(msg: types.Message):
    global LAST_EPISODE_MSG_ID
    sent = await bot.copy_message(
        chat_id=PRIVATE_CHANNEL_ID,
        from_chat_id=msg.chat.id,
        message_id=msg.message_id
    )
    LAST_EPISODE_MSG_ID = sent.message_id
    await msg.reply("✅ Episode posted and ID updated.")

# Force Join Check
async def has_joined_required(user_id):
    for ch in get_channels():
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ("left", "kicked"):
                return False
        except:
            return False
    return True

# Get Episode Callback
@dp.callback_query_handler(lambda c: c.data == "get_ep")
async def get_episode_cb(cb: types.CallbackQuery):
    uid = cb.from_user.id
    if not await has_joined_required(uid):
        msg = "❌ You must join all required channels:\n\n"
        for ch in get_channels():
            channel_id = ch.replace("-100", "")
            msg += f"👉 https://t.me/c/{channel_id}/\n"
        msg += "\nThen click /start again."
        await bot.send_message(uid, msg)
        return
    if not LAST_EPISODE_MSG_ID:
        await cb.message.answer("⚠️ No episode uploaded yet. Please try again later.")
        return
    await bot.send_message(uid, "✅ Here is your episode:")
    await bot.copy_message(
        chat_id=uid,
        from_chat_id=PRIVATE_CHANNEL_ID,
        message_id=LAST_EPISODE_MSG_ID
    )

# Start bot
if __name__ == "__main__":
    print("🤖 Bot is running...")
    executor.start_polling(dp, skip_updates=True)
