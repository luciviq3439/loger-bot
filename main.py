import discord
from discord.ext import commands
import time
from datetime import timedelta
from aiohttp import web
import asyncio

TOKEN = "MTQ5MDA3MDU3NzU0Nzk2ODYwOQ.G_fK2C.gozJkDisCCmSGy31Dzav-r5BV8Vy7PsyNod0cc"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_messages = {}

SPAM_LIMIT = 5
SPAM_TIME = 5

EXEMPT_ROLE_IDS = [1345114361798201417, 1345114368420872212, 1457311005515321528, 1440834857474457730]

# -------------------- BOT EVENTS --------------------
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="Developing By Luciviq3439"
        )
    )
    print(f"Bot aktif: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Rol ID kontrolü
    if any(role.id in EXEMPT_ROLE_IDS for role in message.author.roles):
        return

    user_id = message.author.id
    now = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(now)
    user_messages[user_id] = [
        t for t in user_messages[user_id] if now - t < SPAM_TIME
    ]

    if len(user_messages[user_id]) > SPAM_LIMIT:
        try:
            await message.author.timeout(
                timedelta(minutes=5),
                reason="Spammed Stupid"
            )
            await message.channel.send(
               f"{message.author.mention} has been **muted for 5 minutes** for spamming."
            )
        except:
            print("Timeout Error")
        user_messages[user_id] = []

    await bot.process_commands(message)

# -------------------- HTTP SERVER (UptimeRobot için) --------------------
async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.add_routes([web.get("/", handle)])

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)  # Render port
    await site.start()

# -------------------- MAIN --------------------
async def main():
    # HTTP server başlat
    await start_web()
    # Bot başlat
    await bot.start(TOKEN)

# Windows uyumluluğu
if __name__ == "__main__":
    asyncio.run(main())
