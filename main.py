import discord
from discord.ext import commands
import config
import sys
import time
import asyncio
from datetime import datetime
from os import path
from Plugins.my_handler import Handler
from Plugins.api_list import handler as api_handler

intents = discord.Intents.default()
intents.message_content = True

handler_obj = Handler()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=intents, help_command=None)
        self.start_time = None
        self.total_bombs = 0

    async def setup_hook(self):
        print("[✓] Bot Ready!")

    async def on_ready(self):
        self.start_time = discord.utils.utcnow()
        print(f"[✓] {self.user.name} Online!")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="💣》SR-ROOT-BOMBER"))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id != config.ALLOWED_CHANNEL_ID:
            return
        await self.process_commands(message)

bot = Bot()

# ── .help ──
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="ℹ️》HELP", description="**💣》SR-ROOT-BOMBER v2.0**", color=config.INFO_COLOR)
    embed.add_field(name="💣》`.bomb <sms/call> <09xx> <count>`", value="شروع بمباران", inline=False)
    embed.add_field(name="📊》`.status`", value="وضعیت سیستم", inline=False)
    embed.add_field(name="🔄》`.reload`", value="ریست API (ادمین)", inline=False)
    embed.set_footer(text="💣》SR-ROOT-BOMBER | SR ROOT TEAM")
    await ctx.reply(embed=embed)

# ── .bomb ──
@bot.command(name="bomb", aliases=["b"])
async def bomb_cmd(ctx, bomb_type=None, phone=None, count=10):
    if not bomb_type or not phone:
        embed = discord.Embed(title="❌》USAGE", description="`.bomb <sms/call> <09xxxxxxxxx> <count>`\nمثال: `.bomb sms 09123456789 20`", color=config.ERROR_COLOR)
        await ctx.reply(embed=embed)
        return

    bomb_type = bomb_type.lower()
    if bomb_type not in ["sms", "call"]:
        await ctx.reply("❌》نوع: `sms` یا `call`")
        return

    phone = phone.strip()
    if not (phone.isnumeric() and phone.startswith("09") and len(phone) == 11):
        await ctx.reply("❌》شماره باید ۱۱ رقم باشه و با ۰۹ شروع بشه! مثال: `09123456789`")
        return

    count = min(int(count), config.MAX_SPAM_COUNT)
    api_count = handler_obj.sms_api_count if bomb_type == "sms" else handler_obj.call_api_count

    embed_start = discord.Embed(title="🔥》ATTACK STARTED", description=f"**🎯:** `{phone}` | **💣:** `{bomb_type.upper()}` | **📊:** `{count}`", color=config.EMBED_COLOR)
    embed_start.set_footer(text="💣》SR-ROOT-BOMBER")
    await ctx.reply(embed=embed_start)

    func = handler_obj.send_sms if bomb_type == "sms" else handler_obj.send_call

    for i in range(count):
        try:
            func(phone)
        except:
            pass
        await asyncio.sleep(0.3)

    embed_done = discord.Embed(title="✅》DONE!", description=f"**🎯:** `{phone}` | **💣:** `{bomb_type.upper()}` | **📊:** `{count}`", color=config.SUCCESS_COLOR)
    embed_done.set_footer(text="💣》SR-ROOT-BOMBER")
    await ctx.reply(embed=embed_done)

# ── .status ──
@bot.command(name="status", aliases=["st"])
async def status_cmd(ctx):
    sms = handler_obj.sms_api_count
    call = handler_obj.call_api_count
    proxy = "🟢 ON" if path.exists("./proxies.txt") else "🔴 OFF"
    embed = discord.Embed(title="📊》STATUS", color=config.INFO_COLOR)
    embed.add_field(name="🔌》APIs", value=f"SMS: `{sms}` | Call: `{call}`", inline=False)
    embed.add_field(name="📡》Proxy", value=proxy, inline=True)
    embed.set_footer(text="💣》SR-ROOT-BOMBER")
    await ctx.reply(embed=embed)

# ── .reload ──
@bot.command(name="reload", aliases=["rl"])
async def reload_cmd(ctx):
    import importlib
    importlib.reload(api_handler)
    global handler_obj
    handler_obj = Handler()
    embed = discord.Embed(title="✅》RELOADED!", description=f"SMS: `{handler_obj.sms_api_count}` | Call: `{handler_obj.call_api_count}`", color=config.SUCCESS_COLOR)
    embed.set_footer(text="💣》SR-ROOT-BOMBER")
    await ctx.reply(embed=embed)

# ── Error Handler ──
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("❌》کامند پیدا نشد! `.help` رو بزن.", delete_after=5)

# ── Run ──
if __name__ == "__main__":
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[!] Token not set!")
        sys.exit(1)
    bot.run(config.BOT_TOKEN)