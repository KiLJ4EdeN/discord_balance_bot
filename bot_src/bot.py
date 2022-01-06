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

# DATABASE
from database import SQLiteDatabase

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix=".")

# Initiate the database
db = SQLiteDatabase(initiate=False)


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


# COMMAND .adduser, adds a user to the database using their nickname
@bot.command(
    help="usage: .adduser Insane-Kazzak",
    brief="adds a user to the database with 0 balance"
)
async def adduser(ctx, name: str):
    name = name.lower()
    try:
        db.fetch_user_balance(user_name=name)
        await ctx.author.send(f"user: {name} is already registered! skipping...")
    except AttributeError:
        db.insert_users(user_list=[{'name': name, 'balance': 0},
                                   ])
        await ctx.author.send(f"user: {name} successfully created!")


# COMMAND .add, add balance for a user
@bot.command(
    help="usage: .add Insane-Kazzak 1000",
    brief="adds balance for a user"
)
async def add(ctx, name: str, value: float):
    name = name.lower()
    try:
        bal = db.fetch_user_balance(user_name=name)
        db.update_user_balance(user_name=name, value=bal+value)
        await ctx.author.send(f"user: balance increased from {bal} to {bal+value}")
    except AttributeError:
        await ctx.author.send(f"user: {name} does not exist!")


# COMMAND .deduct, lower balance of a user
@bot.command(
    help="usage: .deduct Insane-Kazzak 1000",
    brief="lower balance of a user"
)
async def deduct(ctx, name: str, value: float):
    name = name.lower()
    try:
        bal = db.fetch_user_balance(user_name=name)
        db.update_user_balance(user_name=name, value=bal-value)
        await ctx.author.send(f"user: balance decreased from {bal} to {bal-value}")
    except AttributeError:
        await ctx.author.send(f"user: {name} does not exist!")


# COMMAND .reset, resets balance of a user
@bot.command(
    help="usage: .reset Insane-Kazzak",
    brief="resets balance of a user"
)
async def reset(ctx, name: str):
    name = name.lower()
    try:
        db.fetch_user_balance(user_name=name)
        db.update_user_balance(user_name=name, value=0)
        await ctx.author.send(f"user: balance reset to 0")
    except AttributeError:
        await ctx.author.send(f"user: {name} does not exist!")


# COMMAND .B. THIS DMs THE USER THEIR BALANCE
@bot.command(
    # ADDS THIS VALUE TO THE .HELP PRINT MESSAGE.
    help="DMs the balance",
    # ADDS THIS VALUE TO THE .HELP MESSAGE.
    brief="DMs the balance"
)
async def b(ctx):
    name = ctx.author.nick
    name = name.lower()
    try:
        bal = db.fetch_user_balance(user_name=name)
        await ctx.author.send(f"your balance is: {bal}")
    except AttributeError:
        await ctx.author.send(f"user: {name} does not exist!")


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


# COMMAND .CUT. calcs cut
@bot.command(
    # ADDS THIS VALUE TO THE .HELP PRINT MESSAGE.
    help=".cut {total balance to cut ex: 1000} {list of percentages ex: 70 20 10}",
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
            total_money = float(args[0])
            sum = 0
            for arg in args[1:]:
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


# COMMAND .divide. divide a number by another
@bot.command(
    # ADDS THIS VALUE TO THE .HELP PRINT MESSAGE.
    help=".divide num1 num2, ex: .divide 6000 12",
    # ADDS THIS VALUE TO THE .HELP MESSAGE.
    brief="divides two numbers"
)
async def divide(ctx, *args):
    # check zero args
    if len(args) == 0:
        response = "you must provide at least two arguments to .divide !"
        await ctx.author.send(response)
    elif len(args) == 1:
        response = "you must provide at least two arguments to .divide !"
        await ctx.author.send(response)
    else:
        response = ""
        # LOOPS THROUGH THE LIST OF ARGUMENTS THAT THE USER INPUTS.
        try:
            total_money = float(args[0])
            division = float(args[1])
            if total_money <= division:
                response = "first argument must be bigger than the second one!"
                await ctx.author.send(response)
            else:
                response += f"division is {int(total_money / division)}\n"
                await ctx.author.send(response)
        except ValueError:
            response = "arguments to .divide ! MUST be numbers"
            await ctx.author.send(response)

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)
