from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_ui(bot_username):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 Video", callback_data="video"),
            InlineKeyboardButton("🎵 MP3", callback_data="mp3")
        ],
        [
            InlineKeyboardButton(
                "➕ Add to Group",
                url=f"https://t.me/{bot_username}?startgroup=true"
            )
        ]
    ])

def quality_ui(url):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("360p", callback_data=f"q360|{url}"),
            InlineKeyboardButton("720p", callback_data=f"q720|{url}")
        ],
        [
            InlineKeyboardButton("1080p", callback_data=f"q1080|{url}")
        ],
        [
            InlineKeyboardButton("🚀 Best", callback_data=f"qbest|{url}")
        ],
        [
            InlineKeyboardButton("🎵 MP3", callback_data=f"mp3|{url}")
        ]
    ])
