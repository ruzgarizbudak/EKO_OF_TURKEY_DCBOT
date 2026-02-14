import discord
from discord.ext import commands
from logic import DB_Manager
from config import TOKEN, DATABASE
from chart import aylik_enflasyon_grafik
import random

# Veritabanı
db = DB_Manager(DATABASE)

# Intentler
intents = discord.Intents.all()
intents.members = True

# Bot
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('Merhaba ben istediginiz')

# Sunucuya biri girince karşılama
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="genel")
    if channel:
        await channel.send(
            f"👋 Hoş geldin {member.mention}!\n"
            f"Ben bu sunucunun botuyum 🤖\n"
            f"`/toplam` yazarak enflasyon hesaplayabilir,\n"
            f"`/oyun` ile mini oyun oynayabilirsin 🎮"
        )

@bot.command()
async def about(ctx):
    await ctx.send("🤖 Bot Adı: EnflasyonBot/n📊 Ne yapar?/nTürkiye’ye ait aylık ve yıllık enflasyon verilerini analiz eder,/ngrafikler üretir ve yıl içi toplam (birikimli) enflasyonu hesaplar./n🧠 Öne çıkan özellikler/n📈 Yıllık aylık enflasyon grafiklerini oluşturur/n📊 Yıl içi toplam (bileşik) enflasyonu gösterir/n🗓️ Ay-Yıl bazlı sorgulama yapabilir/n⚡ Hızlı ve sade sonuçlar/n 🛠️ Kullanılan Teknolojiler/nPython/nSQLite/ndiscord.py/nmatplotlib/n📌 Komutlar/n!toplam → Ay-Yıl girerek yıl içi toplam enflasyonu öğren/n!grafik 2021 → Seçilen yılın aylık enflasyon grafiğini getir/n!yardim → Komut listesini gösterir")


# TOPLAM KOMUTU (DEĞİŞTİRİLMEDİ)
@bot.command()
async def toplam(ctx):
    await ctx.send("Ay ve Yıl şeklinde giriniz (örn: 10-2021)")
    msg = await bot.wait_for(
        "message",
        check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
        timeout=30
    )
    date = msg.content.strip()
    sonuc = db.yil_toplam(date)
    if sonuc is not None:
        await ctx.send(f"**{date}** için yıl içi toplam enflasyon: **%{sonuc}**")
    else:
        await ctx.send("Bu tarihe ait veri bulunamadı.")

# MİNİ OYUN
@bot.command()
async def oyun(ctx):
    sayi = random.randint(1, 10)
    await ctx.send(
        "🎮 **Sayı Tahmin Oyunu**\n"
        "1 ile 10 arasında bir sayı tuttum!\n"
        "Tahminini yaz (30 saniyen var ⏳)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)

        if not msg.content.isdigit():
            await ctx.send("❌ Lütfen geçerli bir sayı gir.")
            return

        tahmin = int(msg.content)

        if tahmin == sayi:
            await ctx.send("🎉 **Tebrikler! Doğru bildin!**")
        else:
            await ctx.send(f"😅 Yanlış! Doğru sayı **{sayi}** idi.")

    except:
        await ctx.send("⏰ Süre doldu! Oyun bitti.")




@bot.command()
async def grafik(ctx, year: int = None):

    if year is None:
        await ctx.send("Lütfen yıl giriniz (örn: 2021)")
        return

    data = db.aylik_veri(year)

    if not data:
        await ctx.send("❌ Bu yıla ait veri bulunamadı.")
        return

    dosya = aylik_enflasyon_grafik(data, year)

    await ctx.send(
        file=discord.File(dosya),
        content=f"📈 {year} Aylık Enflasyon Grafiği"
    )



# Botu çalıştır
bot.run(TOKEN)
