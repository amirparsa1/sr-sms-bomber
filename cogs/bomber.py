import discord
from discord.ext import commands
import config
import asyncio
import time
from datetime import datetime
from os import path
from Plugins.my_handler import Handler
from Plugins.api_list import handler as api_handler


class Bomber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}
        self.handler = Handler()

    # ── ADMIN CHECK ──
    def is_admin():
        async def predicate(ctx):
            role = ctx.guild.get_role(config.ADMIN_ROLE_ID)
            if ctx.author.guild_permissions.administrator:
                return True
            if role and role in ctx.author.roles:
                return True
            embed = discord.Embed(
                title="🔒》ACCESS DENIED",
                description=f"⛔ نیاز به رول: <@&{config.ADMIN_ROLE_ID}>",
                color=config.ERROR_COLOR
            )
            embed.set_footer(text="💣》SR-ROOT-BOMBER")
            await ctx.respond(embed=embed, ephemeral=True)
            return False
        return commands.check(predicate)

    # ── USER CHECK ──
    def has_user_role():
        async def predicate(ctx):
            admin_role = ctx.guild.get_role(config.ADMIN_ROLE_ID)
            user_role = ctx.guild.get_role(config.USER_ROLE_ID)
            if ctx.author.guild_permissions.administrator:
                return True
            if admin_role and admin_role in ctx.author.roles:
                return True
            if user_role and user_role in ctx.author.roles:
                return True
            embed = discord.Embed(
                title="🔒》ACCESS DENIED",
                description=f"⛔ نیاز به رول: <@&{config.USER_ROLE_ID}>",
                color=config.ERROR_COLOR
            )
            embed.set_footer(text="💣》SR-ROOT-BOMBER")
            await ctx.respond(embed=embed, ephemeral=True)
            return False
        return commands.check(predicate)

    # ── CHANNEL CHECK ──
    def allowed_channel():
        async def predicate(ctx):
            if ctx.channel.id == config.ALLOWED_CHANNEL_ID:
                return True
            embed = discord.Embed(
                title="⛔》WRONG CHANNEL",
                description=f"⚠️ فقط: <#{config.ALLOWED_CHANNEL_ID}>",
                color=config.WARNING_COLOR
            )
            embed.set_footer(text="💣》SR-ROOT-BOMBER")
            await ctx.respond(embed=embed, ephemeral=True)
            return False
        return commands.check(predicate)

    # ── COOLDOWN CHECK ──
    def cooldown():
        async def predicate(ctx):
            uid = ctx.author.id
            now = time.time()
            if uid in ctx.cog.cooldowns:
                last = ctx.cog.cooldowns[uid]
                rem = config.COOLDOWN_SECONDS - (now - last)
                if rem > 0:
                    embed = discord.Embed(
                        title="⏰》COOLDOWN",
                        description=f"🔥 **{rem:.1f}s** صبر کن!",
                        color=config.WARNING_COLOR
                    )
                    await ctx.respond(embed=embed, ephemeral=True)
                    return False
            ctx.cog.cooldowns[uid] = now
            return True
        return commands.check(predicate)

    # ── PROXY CHECK ──
    def proxy_state():
        return path.exists("./proxies.txt")

    # ── /bomb ──
    @discord.slash_command(name="bomb", description="💣》شروع بمباران")
    @has_user_role()
    @allowed_channel()
    @cooldown()
    async def bomb(
        self,
        ctx: discord.ApplicationContext,
        bomb_type: discord.Option(str, "نوع", choices=[
            discord.OptionChoice(name="📱》SMS", value="sms"),
            discord.OptionChoice(name="📞》CALL", value="call"),
        ]),
        phone_number: discord.Option(str, "شماره (09123456789)"),
        spam_count: discord.Option(int, "تعداد", min_value=1, max_value=config.MAX_SPAM_COUNT, default=10),
    ):
        phone_number = phone_number.strip()
        if not (phone_number.isnumeric() and phone_number.startswith("09") and len(phone_number) == 11):
            embed = discord.Embed(title="❌》INVALID", description="فرمت: `09123456789`", color=config.ERROR_COLOR)
            await ctx.respond(embed=embed, ephemeral=True)
            return

        api_count = self.handler.sms_api_count if bomb_type == "sms" else self.handler.call_api_count
        if api_count == 0:
            embed = discord.Embed(title="⚠️》NO API", description=f"API برای {bomb_type.upper()} نیست!", color=config.WARNING_COLOR)
            await ctx.respond(embed=embed, ephemeral=True)
            return

        embed_start = discord.Embed(
            title="🔥》ATTACK STARTED",
            description=f"**🎯:** `{phone_number}` | **💣:** `{bomb_type.upper()}` | **📊:** `{spam_count}`",
            color=config.EMBED_COLOR
        )
        embed_start.set_footer(text="💣》SR-ROOT-BOMBER")
        await ctx.respond(embed=embed_start)

        embed_prog = discord.Embed(title=f"💣》BOMBING {bomb_type.upper()}...", color=config.EMBED_COLOR)
        embed_prog.add_field(name="📊》Progress", value=f"`0/{spam_count}`", inline=True)
        embed_prog.add_field(name="✅》Success", value="`0`", inline=True)
        embed_prog.add_field(name="❌》Failed", value="`0`", inline=True)
        embed_prog.set_footer(text="💣》SR-ROOT-BOMBER")
        msg = await ctx.channel.send(embed=embed_prog)

        success = failed = 0
        st = time.time()
        func = self.handler.send_sms if bomb_type == "sms" else self.handler.send_call

        for i in range(spam_count):
            try:
                func(phone_number)
                success += 1
            except:
                failed += 1
            if (i + 1) % 5 == 0 or i == spam_count - 1:
                embed_prog.clear_fields()
                embed_prog.add_field(name="📊》Progress", value=f"`{i+1}/{spam_count}`", inline=True)
                embed_prog.add_field(name="✅》Success", value=f"`{success}`", inline=True)
                embed_prog.add_field(name="❌》Failed", value=f"`{failed}`", inline=True)
                embed_prog.set_footer(text="💣》SR-ROOT-BOMBER")
                try:
                    await msg.edit(embed=embed_prog)
                except:
                    pass
            await asyncio.sleep(0.3)

        tt = time.time() - st
        self.bot.total_bombs += 1
        rate = (success / spam_count) * 100 if spam_count else 0
        if rate >= 80:
            c, e = config.SUCCESS_COLOR, "✅"
        elif rate >= 50:
            c, e = config.WARNING_COLOR, "⚠️"
        else:
            c, e = config.ERROR_COLOR, "❌"

        embed_final = discord.Embed(
            title=f"{e}》ATTACK FINISHED",
            description=f"**🎯:** `{phone_number}` | **💣:** `{bomb_type.upper()}`",
            color=c
        )
        embed_final.add_field(name="📊》Total", value=f"`{spam_count}`", inline=True)
        embed_final.add_field(name="✅》Success", value=f"`{success}`", inline=True)
        embed_final.add_field(name="❌》Failed", value=f"`{failed}`", inline=True)
        embed_final.add_field(name="📈》Rate", value=f"`{rate:.1f}%`", inline=True)
        embed_final.add_field(name="⏱️》Time", value=f"`{tt:.1f}s`", inline=True)
        embed_final.set_footer(text="💣》SR-ROOT-BOMBER")
        await msg.edit(embed=embed_final)

    # ── /status ──
    @discord.slash_command(name="status", description="📊》وضعیت سیستم")
    @has_user_role()
    @allowed_channel()
    async def status(self, ctx: discord.ApplicationContext):
        sms = self.handler.sms_api_count
        call = self.handler.call_api_count
        proxy = "🟢 ON" if self.proxy_state() else "🔴 OFF"
        uptime = str(datetime.utcnow() - self.bot.start_time).split('.')[0] if self.bot.start_time else "N/A"

        embed = discord.Embed(title="📊》STATUS", color=config.INFO_COLOR)
        embed.add_field(name="🔌》APIs", value=f"SMS: `{sms}` | Call: `{call}`", inline=False)
        embed.add_field(name="📡》Proxy", value=proxy, inline=True)
        embed.add_field(name="💣》Bombs", value=f"`{self.bot.total_bombs}`", inline=True)
        embed.add_field(name="⏱️》Uptime", value=f"`{uptime}`", inline=True)
        embed.set_footer(text="💣》SR-ROOT-BOMBER")
        await ctx.respond(embed=embed)

    # ── /reload ──
    @discord.slash_command(name="reload", description="🔄》ریست API (ادمین)")
    @is_admin()
    @allowed_channel()
    async def reload_apis(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="🔄》RELOADING...", color=config.INFO_COLOR)
        await ctx.respond(embed=embed)
        try:
            import importlib
            importlib.reload(api_handler)
            self.handler = Handler()
            embed_success = discord.Embed(
                title="✅》RELOADED!",
                description=f"SMS: `{self.handler.sms_api_count}` | Call: `{self.handler.call_api_count}`",
                color=config.SUCCESS_COLOR
            )
            embed_success.set_footer(text="💣》SR-ROOT-BOMBER")
            await ctx.edit(embed=embed_success)
        except Exception as e:
            embed_error = discord.Embed(title="❌》ERROR", description=f"```{e}```", color=config.ERROR_COLOR)
            await ctx.edit(embed=embed_error)

    # ── /help ──
    @discord.slash_command(name="help", description="ℹ️》راهنما")
    async def help_command(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="ℹ️》HELP", description="**💣》SR-ROOT-BOMBER v2.0**", color=config.INFO_COLOR)
        embed.add_field(name="💣》`/bomb`", value="شروع بمباران SMS/Call", inline=False)
        embed.add_field(name="📊》`/status`", value="وضعیت سیستم", inline=False)
        embed.add_field(name="🔄》`/reload`", value="ریست API (ادمین)", inline=False)
        embed.set_footer(text="💣》SR-ROOT-BOMBER | SR ROOT TEAM")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Bomber(bot))