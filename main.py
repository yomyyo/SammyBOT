import discord
from discord.ext import commands

import datetime
import time

client = commands.Bot(command_prefix='$')

time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}

#Command starts here
@client.command(pass_context = True)
async def unban(ctx,member:discord.Member):
    if member == ctx.message.author:
        await ctx.channel.send("You cannot unban yourself")
        return

    user = member
    role = discord.utils.get(user.guild.roles, name="jail")
    await user.remove_roles(role)
    await ctx.channel.send("No More Jail for " + member.name)

@client.command(pass_context = True)
async def numword(ctx, *message):
    if not message: #nothing is passed after the command
        return await ctx.channel.send("**Please pass in required arguments**") 

    res = len(message)
    # printing result
    await ctx.channel.send("The number of words in message are : " +  str(res))
    

@client.event
async def on_ready():
    print('Bot is Ready')

@client.event
async def on_message(ctx):
    await client.process_commands(ctx)
    global author_msg_counts

    author_id = ctx.author.id
    # Get current epoch time in milliseconds
    curr_time = datetime.datetime.now().timestamp() * 1000

    # Make empty list for author id, if it does not exist
    if not author_msg_times.get(author_id, False):
        author_msg_times[author_id] = []

    # Append the time of this message to the users list of message times
    author_msg_times[author_id].append(curr_time)

    # Find the beginning of our time window.
    expr_time = curr_time - time_window_milliseconds

    # Find message times which occurred before the start of our window
    expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
    ]

    # Remove all the expired messages times from our list
    for msg_time in expired_msgs:
        author_msg_times[author_id].remove(msg_time)
    # ^ note: we probably need to use a mutex here. Multiple threads
    # might be trying to update this at the same time. Not sure though.

    if len(author_msg_times[author_id]) > max_msg_per_window:
        await ctx.channel.send(ctx.author.name + " is going to jail and getting their ass beat for spam")
        user = ctx.author
        role = discord.utils.get(user.guild.roles, name="jail")
        await user.add_roles(role)
        


    

    
client.run('ODY5NzQyNTYzMzY2Njc4NTM4.YQCo4g.ECxK0ncDb9ykpJ3px5i0xpuRxsA')