"""
main crap for the bot
"""
# bot.py

import numpy as np
# IMPORT THE OS MODULE.
import os

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix=".")


# ON_MESSAGE() EVENT LISTENER. NOTICE IT IS USING @BOT.EVENT AS OPPOSED TO @BOT.COMMAND().
@bot.event
async def on_message(message):
    # CHECK IF THE MESSAGE SENT TO THE CHANNEL IS "HELLO".
    if message.content == "hello":
        # SENDS A MESSAGE TO THE CHANNEL.
        await message.channel.send("pies are better than cakes. change my mind.")
    # INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.
    await bot.process_commands(message)


# COMMAND .PING. INVOKES ONLY WHEN THE MESSAGE ".PING" IS SEND IN THE DISCORD SERVER.
# ALTERNATIVELY @BOT.COMMAND(NAME="PING") CAN BE USED IF ANOTHER FUNCTION NAME IS DESIRED.
@bot.command(
    # ADDS THIS VALUE TO THE .HELP PING MESSAGE.
    help="Uses come crazy logic to determine if pong is actually the correct value or not.",
    # ADDS THIS VALUE TO THE .HELP MESSAGE.
    brief="Prints pong back to the channel."
)
async def ping(ctx):
    # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
    await ctx.channel.send("pong")


# COMMAND .PRINT. THIS TAKES AN IN A LIST OF ARGUMENTS FROM THE USER AND SIMPLY PRINTS THE VALUES BACK TO THE CHANNEL.
@bot.command(
    # ADDS THIS VALUE TO THE .HELP PRINT MESSAGE.
    help="Looks like you need some help.",
    # ADDS THIS VALUE TO THE .HELP MESSAGE.
    brief="Prints the list of values back to the channel."
)
async def print(ctx, *args):
    response = ""

    # LOOPS THROUGH THE LIST OF ARGUMENTS THAT THE USER INPUTS.
    for arg in args:
        response = response + " " + arg

    # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
    await ctx.channel.send(response)


# COMMAND .B. THIS DMs THE USER THEIR BALANCE
@bot.command(
    # ADDS THIS VALUE TO THE .HELP PRINT MESSAGE.
    help="DMs the balance",
    # ADDS THIS VALUE TO THE .HELP MESSAGE.
    brief="DMs the balance"
)
async def b(ctx):
    response = f"Your Balance is ... \n{ctx.author}"
    # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
    await ctx.author.send(response)


# COMMAND .CUT. THIS DMs THE USER THEIR BALANCE
@bot.command(
    # ADDS THIS VALUE TO THE .HELP PRINT MESSAGE.
    help=".cut {list of percentages ex: 70 20 10} {total balance to cut ex: 1000}",
    # ADDS THIS VALUE TO THE .HELP MESSAGE.
    brief="Calculates respective cuts based on percentages given"
)
async def cut(ctx, *args):
    # check zero args
    if len(args) == 0:
        response = "you must provide at least two arguments to .cut !"
        await ctx.author.send(response)
    elif len(args) == 1:
        response = "you must provide at least two arguments to .cut !"
        await ctx.author.send(response)
    else:
        response = ""
        # LOOPS THROUGH THE LIST OF ARGUMENTS THAT THE USER INPUTS.
        try:
            total_money = float(args[-1])
            sum = 0
            for arg in args[:-1]:
                cut = int(total_money * (float(arg) / 100.))
                response += f"cut for {arg} is: {cut}\n"
                sum += float(arg)
            if int(sum) != 100:
                response = "arguments must sum up to 100% !"
                await ctx.author.send(response)
            else:
                await ctx.author.send(response)
        except ValueError:
            response = "arguments to .cut ! MUST be numbers"
            await ctx.author.send(response)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)
