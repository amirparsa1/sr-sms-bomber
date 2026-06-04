import discord
from discord.ext import commands
import config
from os import path, system
import sys
import asyncio

# نصب خودکار
def install_reqs():
    if path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            for line in f:
                lib = line.strip().split(">=")[0].split("==")[0]
                if lib:
                    try:
                        __import__(lib.replace("-", "_"))
                    except ImportError:
                        system(f"pip install {lib}")

install_reqs()

intents = discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.start_time = None
        self.total_bombs = 0

    async def setup_hook(self):
        await self.load_extension("cogs.bomber")
        print("[✓] Cogs Loaded!")

    async def on_ready(self):
        self.start_time = discord.utils.utcnow()
        print(f"""
╔══════════════════════════════════╗
║                                  ║
║    💣》SR-ROOT-BOMBER             ║
║    Powered by SR ROOT            ║
║                                  ║
║  👑 {self.user.name:<26} ║
║  📡 {len(self.guilds)} Servers{'':<20} ║
║  ⚡ Online & Ready               ║
║                                  ║
╚══════════════════════════════════╝
        """)

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="💣》SR-ROOT-BOMBER"
            ),
            status=discord.Status.online
        )

        self.loop.create_task(self.rotate_status())

    async def rotate_status(self):
        statuses = [
            discord.Activity(type=discord.ActivityType.watching, name="💣》SR-ROOT-BOMBER"),
            discord.Activity(type=discord.ActivityType.playing, name="🔥》SR-ROOT-SMS"),
            discord.Activity(type=discord.ActivityType.listening, name="⚡》/bomb"),
            discord.Activity(type=discord.ActivityType.watching, name=f"💀》{self.total_bombs} bombs"),
        ]
        while not self.is_closed():
            for s in statuses:
                await self.change_presence(activity=s)
                await asyncio.sleep(8)

bot = Bot()

if __name__ == "__main__":
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[!] Token not set! Edit config.py")
        sys.exit(1)
    bot.run(config.BOT_TOKEN)