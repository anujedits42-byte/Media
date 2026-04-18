def make_progress_hook(message):
    async def update(text):
        try:
            await message.edit_text(text)
        except:
            pass

    def hook(d):
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "0%")
            speed = d.get("_speed_str", "")
            eta = d.get("_eta_str", "")

            import asyncio
            asyncio.create_task(
                update(f"📥 Downloading...\n\n{percent} | {speed} | ETA {eta}")
            )

    return hook
