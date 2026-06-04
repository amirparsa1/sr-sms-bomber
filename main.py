import discord
from discord.ext import commands
import config
import sys

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
        print(f"[✓] {self.user.name} Online!")
        print(f"[✓] Servers: {len(self.guilds)}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="💣》SR-ROOT-BOMBER"))

bot = Bot()

if __name__ == "__main__":
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[!] Token not set! Edit config.py")
        sys.exit(1)
    bot.run(config.BOT_TOKEN)