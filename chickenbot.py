#!/usr/bin/python3
# coding: utf-8

"""Bot for SNM chicken cult server. Made by d3giigii."""

import configparser
import discord
import logging

from discord import client
from discord.ext import commands

# Parse the config file. 
config = configparser.ConfigParser() 
config._DEFAULT_INTERPOLATION = configparser.ExtendedInterpolation() 
config.read('config.ini') 
config.read('token.ini')

# Setup from config
prefix_char = str(config.get('OPTIONS', 'PrefixChar')) 
bot = commands.Bot(command_prefix=prefix_char)

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