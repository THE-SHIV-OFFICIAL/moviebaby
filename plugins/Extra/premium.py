from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- ⚙️ CONFIGURATION ---
UPDATE_CHANNEL = "betabot_hub"    # Do not add '@'
SUPPORT_GROUP = "movie_req_premium" # Do not add '@'

# --- 🔍 VERIFICATION CHECKER ---
async def is_user_verified(client, user_id):
    """Checks if the user is a member of both the update and support chats."""
    try:
        # Check Update Channel
        await client.get_chat_member(UPDATE_CHANNEL, user_id)
        # Check Support Group
        await client.get_chat_member(SUPPORT_GROUP, user_id)
        return True
    except UserNotParticipant:
        # Triggers if they haven't joined one or both
        return False
    except Exception as e:
        print(f"Force Sub Error: {e}")
        return False

# --- 🎬 MOVIE REQUEST INTERCEPTOR ---
# Note: Adjust the filters below based on how your bot normally receives movie requests 
# (e.g., if it uses deep linking like /start movie_id, change the filter to filters.command("start"))

@Client.on_message(filters.private & filters.incoming)
async def handle_movie_request(client, message):
    user_id = message.from_user.id
    
    # 1. Check if the user is verified
    verified = await is_user_verified(client, user_id)
    
    # 2. If NOT verified, show the poster and buttons
    if not verified:
        
        # Grab the deep link parameter if they clicked a specific movie link
        # so they don't lose the movie when they click "Try Again"
        start_param = message.text.split()[1] if len(message.text.split()) > 1 else "start"
        
        btn = [
            [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATE_CHANNEL}")],
            [InlineKeyboardButton("💬 ᴊᴏɪɴ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url=f"https://t.me/{SUPPORT_GROUP}")],
            [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ / ᴠᴇʀɪꜰʏ", url=f"https://t.me/{client.me.username}?start={start_param}")]
        ]
        
        await message.reply_photo(
            photo="https://graph.org/file/55a5392f88ec5a4bd3379.jpg",
            caption=(
                f"<b>ʜᴇʟʟᴏ {message.from_user.mention} 👋</b>\n\n"
                "<b>🔐 ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ꜰᴏʀ ꜰʀᴇᴇ!</b>\n\n"
                "<i>ᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟꜱ ᴜꜱɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ, ᴛʜᴇɴ ᴄʟɪᴄᴋ 'ᴛʀʏ ᴀɢᴀɪɴ' ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ꜰɪʟᴇ.</i>"
            ),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return # Important: This stops the code here so they don't get the movie

    # 3. If they ARE verified, the code continues to here!
    # 👇 PASTE YOUR MOVIE SENDING/DATABASE LOGIC BELOW THIS LINE 👇
    
    await message.reply_text("✅ <b>ʏᴏᴜ ᴀʀᴇ ᴠᴇʀɪꜰɪᴇᴅ!</b>\n\n<i>(Your bot's regular movie-sending code goes here)</i>")
