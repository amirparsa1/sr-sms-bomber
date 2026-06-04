import discord
from discord.ext import commands
import config
import sys

intents = discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=intents, help_command=None)
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

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id != config.ALLOWED_CHANNEL_ID:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("❌》کامند پیدا نشد! `.help` رو بزن.", delete_after=5)
        elif isinstance(error, commands.CheckFailure):
            return
        else:
            print(f"[ERROR] {error}")

bot = Bot()

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="ℹ️》HELP",
        description="**💣》SR-ROOT-BOMBER v2.0**",
        color=config.INFO_COLOR
    )
    embed.add_field(name="💣》`.bomb <sms/call> <09xx> <count>`", value="شروع بمباران", inline=False)
    embed.add_field(name="📊》`.status`", value="وضعیت سیستم", inline=False)
    embed.add_field(name="🔄》`.reload`", value="ریست API (ادمین)", inline=False)
    embed.add_field(name="ℹ️》`.help`", value="این راهنما", inline=False)
    embed.set_footer(text="💣》SR-ROOT-BOMBER | SR ROOT TEAM")
    await ctx.reply(embed=embed)

if __name__ == "__main__":
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[!] Token not set! Edit config.py")
        sys.exit(1)
    bot.run(config.BOT_TOKEN)