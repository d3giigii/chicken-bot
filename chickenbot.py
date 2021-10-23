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