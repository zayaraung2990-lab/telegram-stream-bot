import os
import asyncio
from quart import Quart, Response
from telegram import Bot

app = Quart(__name__)

# Environment Variables ကနေယူမယ်
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
# Render ကပေးတဲ့ သင့်ရဲ့ URL ကို ဒီမှာထည့်ပါ
BASE_URL = "https://telegram-stream-bot-4i9y.onrender.com"

@app.route('/')
async def index():
    return "Server is Running! Send a video to your bot."

@app.route('/stream/<file_id>')
async def stream_video(file_id):
    try:
        file = await bot.get_file(file_id)
        # Telegram ရဲ့ File path ကို လှမ်းယူတာပါ
        direct_url = file.file_path
        # အဲ့ဒီ URL ဆီကို Redirect လုပ်ပေးလိုက်မယ်
        return Response(direct_url, status=302, headers={'Location': direct_url})
    except Exception as e:
        return f"Error: {str(e)}", 500

async def main():
    # ဒီအပိုင်းက Bot ဆီစာရောက်ရင် အလုပ်လုပ်မယ့် logic ပါ (Poll လုပ်တာ)
    offset = 0
    print("Bot is polling for messages...")
    while True:
        try:
            updates = await bot.get_updates(offset=offset, timeout=10)
            for update in updates:
                if update.message and update.message.video:
                    file_id = update.message.video.file_id
                    stream_link = f"{BASE_URL}/stream/{file_id}"
                    await update.message.reply_text(f"🎬 Your Direct Link:\n\n{stream_link}")
                offset = update.update_id + 1
        except Exception as e:
            print(f"Polling Error: {e}")
        await asyncio.sleep(1)

if __name__ == "__main__":
    import uvicorn
    # Bot polling ကို background မှာ run မယ်
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
