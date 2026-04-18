import asyncio

def make_progress_hook(message, title):

    async def edit(text):
        try:
            await message.edit_caption(text, parse_mode="Markdown")
        except:
            pass

    def hook(d):
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "0%")
            speed = d.get("_speed_str", "")
            eta = d.get("_eta_str", "")

            try:
                p = int(percent.replace("%",""))
            except:
                p = 0

            bar = "█"*(p//10) + "░"*(10-p//10)

            text = (
                f"📥 *Downloading*\n\n"
                f"{bar}\n"
                f"{percent}\n\n"
                f"⚡ {speed} | ⏱ {eta}"
            )

            asyncio.create_task(edit(text))

        elif d["status"] == "finished":
            asyncio.create_task(edit("📤 *Uploading...*"))

    return hook
