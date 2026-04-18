from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def format_size(size):
    if not size:
        return ""
    for unit in ['B','KB','MB','GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024


def format_duration(seconds):
    if not seconds:
        return "0:00"
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if h:
        return f"{h}:{m:02}:{s:02}"
    return f"{m}:{s:02}"


# 🎯 SMART RECOMMEND
def get_recommended(formats):
    if not formats:
        return None

    # prefer 720p
    for f in formats:
        if f["quality"] == "720p":
            return f

    return formats[-1]


# 🎬 MAIN MENU
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


# 🔥 GOD QUALITY UI
def quality_ui(info, formats, url):
    buttons = []
    row = []

    formats = sorted(formats, key=lambda x: int(x["quality"].replace("p","")))

    recommended = get_recommended(formats)

    for f in formats:
        size = format_size(f.get("filesize"))

        label = f"{f['quality']} ({size})" if size else f["quality"]

        # ⭐ Recommended highlight
        if recommended and f["format_id"] == recommended["format_id"]:
            label = f"⭐ {label}"

        row.append(
            InlineKeyboardButton(
                label,
                callback_data=f"{f['format_id']}|{url}"
            )
        )

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    # 🚀 BEST BUTTON
    if formats:
        best = formats[-1]
        size = format_size(best.get("filesize"))

        buttons.append([
            InlineKeyboardButton(
                f"🚀 Best Quality ({best['quality']} {size})",
                callback_data=f"{best['format_id']}|{url}"
            )
        ])

    # 🎵 MP3
    buttons.append([
        InlineKeyboardButton("🎵 Extract MP3", callback_data=f"mp3|{url}")
    ])

    return InlineKeyboardMarkup(buttons)


# 🎬 GOD CAPTION
def build_caption(info):
    title = info.get("title", "Video")
    duration = format_duration(info.get("duration"))
    uploader = info.get("uploader", "Unknown")

    caption = (
        f"🎬 *{title}*\n\n"
        f"👤 {uploader}\n"
        f"⏱ {duration}\n\n"
        f"⚡ Choose quality below 👇"
    )

    return caption
