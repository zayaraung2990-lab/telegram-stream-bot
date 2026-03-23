import os
from quart import Quart, Response, request
from telegram import Bot

app = Quart(__name__)

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

@app.route('/')
async def index():
    return "Server is running! Bot is active."

@app.route('/stream/<file_id>')
async def stream_video(file_id):
    try:
        file = await bot.get_file(file_id)
        # Telegram ရဲ့ direct link (file_path) ကို လှမ်းယူတာပါ
        direct_url = file.file_path
        return Response(direct_url, status=200)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
