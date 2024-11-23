import discord
from discord.ext import commands
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("دەبی گێت لە دەنگم بی")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("لە مارێ نیمە")

@bot.command()
async def play(ctx, url: str):
    vc = ctx.voice_client
    if not vc:
        await ctx.send("دەبی بێمە ژۆرێ گێم لە دەنگتان نیە")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(url2), after=lambda e: print(f'Finished playing: {e}'))

    await ctx.send(f'Playing: {info["title"]}')

@bot.command()
async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("بەسە گۆرانی هی کافرانە")
    else:
        await ctx.send("هیچ گۆرانیەک لێ نادرێ تازیەمان هەیە")

bot.run(os.getenv('DISCORD_TOKEN'))