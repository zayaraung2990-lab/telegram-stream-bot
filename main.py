import os
import asyncio
from quart import Quart, Response
from telegram import Bot

app = Quart(__name__)

# Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
BASE_URL = "https://telegram-stream-bot-4i9y.onrender.com"

@app.route('/')
async def index():
    return "Server is Running! Send a video to your bot."

@app.route('/stream/<file_id>')
async def stream_video(file_id):
    try:
        file = await bot.get_file(file_id)
        direct_url = file.file_path
        return Response(direct_url, status=302, headers={'Location': direct_url})
    except Exception as e:
        return f"Error: {str(e)}", 500

async def bot_polling():
    offset = 0
    print("Bot is polling...")
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

@app.before_serving
async def startup():
    # Background မှာ bot polling ကို စလုပ်ခိုင်းတာပါ
    asyncio.create_task(bot_polling())

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
