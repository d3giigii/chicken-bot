#!/usr/bin/python3
# coding: utf-8

"""Bot for SNM chicken cult server. Made by d3giigii."""

# import asyncio
import configparser
import discord
import logging
import youtube_dl

from discord import client
from discord.errors import ClientException
from discord.ext import commands

# Parse the config file. 
config = configparser.ConfigParser() 
config._DEFAULT_INTERPOLATION = configparser.ExtendedInterpolation() 
config.read('config.ini') 
config.read('token.ini')

# Setup from config
prefix_char = str(config.get('OPTIONS', 'PrefixChar')) 
bot = commands.Bot(command_prefix=prefix_char)
ffmpeg_path = "C:\\Users\\sonof\\ffmpeg\\bin\\ffmpeg.exe"
err_str = "Error: "

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, 
                                          download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), 
            data=data)

# Command handling
@bot.event 
async def on_message(message): 
    if message.author is client.User: 
        return 
    else:
        await bot.process_commands(message)

@bot.command()
async def cluck(ctx):
    await ctx.send("cluck")

@bot.command()
async def play(ctx, input : str):
    await disconnect(ctx)
    try:
        player = await YTDLSource.from_url(input, stream=True)
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        vc.play(player)
        await ctx.send("Playing " +player.title)
    except (AttributeError, ClientException, RuntimeError) as e:
        await ctx.send(err_str, e.__str__())

@bot.command()
async def disconnect(ctx):
    server = ctx.message.guild.voice_client
    try:
        await server.disconnect()
    except AttributeError:
        pass

# On driver start. 
@bot.event 
async def on_ready(): 
    print('Logged in as: ' + bot.user.name + '#' + bot.user.discriminator) 
    print('Version: ' + discord.__version__)

    # Setup error logging. 
    log_filename = 'discord.log' 
    logger = logging.getLogger('discord') 
    logger.setLevel(logging.DEBUG) 
    handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='a') 
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')) 
    logger.addHandler(handler) 
    print('Logger started. See ' + log_filename + ' for log details.')

# Log in. 
token = str(config.get('BOT_TOKEN', 'Token')) 
bot.run(token)