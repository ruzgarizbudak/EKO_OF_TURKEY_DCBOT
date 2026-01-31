import discord
from discord.ext import commands
from logic import DB_Manager
from config import TOKEN ,DATABASE

db = DB_Manager(DATABASE)

intents = discord.Intents.all()


bot = commands.Bot(command_prefix='/' , intents=intents)


@bot.event
async def on_ready():
    print('Bot hazir')

@bot.command()
async def toplam(ctx):
    await ctx.send("Ay ve Yıl şeklinde giriniz (örn: 10-2021)")
    msg = await bot.wait_for("message",check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30)
    date = msg.content.strip()
    sonuc = db.yil_toplam(date)
    if sonuc is not None:
        await ctx.send(f"**{date}** için yıl içi toplam enflasyon: **%{sonuc}**")
    else:
        await ctx.send(" Bu tarihe ait veri bulunamadı.")


bot.run(TOKEN)
