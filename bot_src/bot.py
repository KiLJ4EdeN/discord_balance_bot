"""
main crap for the bot
"""
# bot.py
import discord
import numpy as np
# IMPORT THE OS MODULE.
import os

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

# DATABASE
from database import SQLiteDatabase

# LOGGING
import logging

# for python code running
import ast

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix=".")

# Initiate the database
db = SQLiteDatabase(initiate=True)


# ON_MESSAGE() EVENT LISTENER. NOTICE IT IS USING @BOT.EVENT AS OPPOSED TO @BOT.COMMAND().
@bot.event
async def on_message(message):
    # CHECK IF THE MESSAGE SENT TO THE CHANNEL IS "HELLO".
    if message.content == "hello":
        # SENDS A MESSAGE TO THE CHANNEL.
        await message.channel.send("pies are better than cakes. change my mind.")
    # INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.
    await bot.process_commands(message)


@bot.command(
    help="get all user balances",
    brief="get all user balances"
)
async def fetchall(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.author.send(f"You don't have the privileges for this command!")
    else:
        response = ""
        res = db.fetch_all()
        for row in res:
            name = row.name
            bal = row.balance
            # change username to nickname
            # user = await bot.fetch_user(int(user_id))
            response += f'{name} balance is {int(bal)}\n'
        await ctx.author.send(response)


# COMMAND .adduser, adds a user to the database using their nickname
@bot.command(
    help="usage: .adduser @Insane-Kazzak",
    brief="adds a user to the database with 0 balance"
)
async def adduser(ctx, user: discord.User):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.author.send(f"You don't have the privileges for this command!")
    else:
        try:
            db.fetch_user_balance(user_id=user.id)
            await ctx.author.send(f"user: {user.display_name} is already registered! skipping...")
        except AttributeError:
            db.insert_users(user_list=[{'uid': user.id, 'name': user.display_name, 'balance': 0},
                                       ])
            await ctx.author.send(f"user: {user.display_name} successfully created!")


# COMMAND .removeuser, adds a user to the database using their nickname
@bot.command(
    help="usage: .remuser @Insane-Kazzak",
    brief="adds a user to the database with 0 balance"
)
async def removeuser(ctx, user: discord.User):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.author.send(f"You don't have the privileges for this command!")
    else:
        try:
            db.fetch_user_balance(user_id=user.id)
            db.drop_user(user_id=user.id)
            await ctx.author.send(f"user: {user.display_name} successfully deleted.")
        except AttributeError:
            await ctx.author.send(f"user: {user.display_name} does not exist!")


# COMMAND .add, add balance for a user
@bot.command(
    help="usage: .add @Insane-Kazzak 1000",
    brief="adds balance for a user"
)
async def add(ctx, user: discord.User, value: float):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.author.send(f"You don't have the privileges for this command!")
    else:
        try:
            bal = db.fetch_user_balance(user_id=user.id)
            db.update_user_balance(user_id=user.id, value=bal+value)
            await ctx.author.send(f"user: {user.display_name} balance increased from {int(bal)} to {int(bal+value)}")
        except AttributeError:
            await ctx.author.send(f"user: {user.display_name} does not exist!")


# COMMAND .deduct, lower balance of a user
@bot.command(
    help="usage: .deduct @Insane-Kazzak 1000",
    brief="lowers balance of a user"
)
async def deduct(ctx, user: discord.User, value: float):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.author.send(f"You don't have the privileges for this command!")
    else:
        try:
            bal = db.fetch_user_balance(user_id=user.id)
            db.update_user_balance(user_id=user.id, value=bal-value)
            await ctx.author.send(f"user: {user.display_name} balance decreased from {int(bal)} to {int(bal-value)}")
        except AttributeError:
            await ctx.author.send(f"user: {user.display_name} does not exist!")


# COMMAND .reset, resets balance of a user
@bot.command(
    help="usage: .reset Insane-Kazzak",
    brief="resets balance of a user"
)
async def reset(ctx, user: discord.User):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.author.send(f"You don't have the privileges for this command!")
    else:
        try:
            bal = db.fetch_user_balance(user_id=user.id)
            db.update_user_balance(user_id=user.id, value=0)
            await ctx.author.send(f"user: {user.display_name} balance reset from {int(bal)} to 0")
        except AttributeError:
            await ctx.author.send(f"user: {user.display_name} does not exist!")


# COMMAND .B. THIS DMs THE USER THEIR BALANCE
@bot.command(
    help="DMs the balance",
    brief="DMs the balance"
)
async def b(ctx):
    try:
        # fetch user balance based on ID
        try:
            bal = db.fetch_user_balance(user_id=ctx.author.id)
            await ctx.author.send(f"your balance is: {int(bal)}")
        except AttributeError:
            await ctx.author.send(f"user: {ctx.author.nick} does not exist in the database!")
    # if we cant fetch the nickname then its pretty much gg
    except AttributeError:
        await ctx.author.send(f"could not acquire nickname.")


# COMMAND .PRINT. THIS TAKES AN IN A LIST OF ARGUMENTS FROM THE USER AND SIMPLY PRINTS THE VALUES BACK TO THE CHANNEL.
@bot.command(
    help="print arg1 arg2 ...",
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
    help=".cut {total balance to cut ex: 1000} {list of percentages ex: 70 20 10}",
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
    help=".divide num1 num2, ex: .divide 6000 12",
    brief="divides two numbers"
)
async def divide(ctx, *args):
    # check zero args
    if len(args) == 0:
        response = "you must provide exactly two arguments to .divide !"
        await ctx.author.send(response)
    elif len(args) == 1:
        response = "you must provide exactly two arguments to .divide !"
        await ctx.author.send(response)
    elif len(args) > 2:
        response = "you must provide exactly two arguments to .divide !"
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


# COMMAND .PING. INVOKES ONLY WHEN THE MESSAGE ".PING" IS SEND IN THE DISCORD SERVER.
# ALTERNATIVELY @BOT.COMMAND(NAME="PING") CAN BE USED IF ANOTHER FUNCTION NAME IS DESIRED.
@bot.command(
    help="Uses come crazy logic to determine if pong is actually the correct value or not.",
    brief="Prints pong back to the channel."
)
async def ping(ctx):
    # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
    await ctx.channel.send("pong")


@bot.command(
    help="prints guild members",
    brief="prints guild members"
)
async def get_members(ctx):
    response = ''
    for member in ctx.message.guild.members:
        response += member.name + '\n'
    await ctx.author.send(response)


@bot.command(
    help="is a user admin",
    brief="is a user admin"
)
async def is_admin(ctx):
    await ctx.author.send(f"{ctx.message.author.guild_permissions.administrator}")


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


# runs python in the bot
@bot.command()
async def python(ctx, *, cmd):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.author.send(f"You don't have the privileges for this command!")
    else:
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)
