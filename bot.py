import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
from itertools import cycle
import time
import youtube_dl
import pip

my_token ='NTI2NjE0NDc4MTUwNjk2OTYw.Dysr4g.q3Bq_EbVrnBAB4WPk-fEJYWYUec'

client = commands.Bot(command_prefix = '-')

client.remove_command('help')
status = ['+help for commands', 'https://lixorbot.weebly.com', "LixorBot"]

players = {}


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name =current_status))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print('The bot is online and is connected to discord')


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Newcomer')
    await client.add_roles(member, role)


@client.event
async def on_message(message):
    
    await client.process_commands(message)
    if message.content.startswith('+help'):
        userID = message.author.id
        await client.send_message(message.channel, '<@%s> ***Check*** `DM` ***For Information*** :mailbox_with_mail: ' % (userID))
        
    await client.process_commands(message)
    if message.content.startswith('+video'):
        userID = message.author.id
        await client.send_message(message.channel, '<@%s> ***Check*** `DM` ***For Information*** :mailbox_with_mail: ' % (userID))
        
        
        

@client.command(pass_context =True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(Colour = discord.Colour.orange())
    embed.set_author(name = 'Help Commands')
    embed.add_field(name ='+say', value ='Returns what the user says.', inline=False)
    embed.add_field(name ='+clear', value ='Deletes certain amount of messages, default amount is 10', inline=False)
    embed.add_field(name ='+join', value ='The bot joins the current voice channel, the user must be in a voice channel to use this comand', inline=False)
    embed.add_field(name ='+leave', value ='The bot leaves the current voice channel.', inline=False)
    embed.add_field(name ='+play', value ='Plays the audio from a youtube url', inline=False)
    embed.add_field(name ='+userinfo', value ='Gives the server information on the selected user', inline=False)
    embed.add_field(name ='+Ban', value ='New Function Thanks To @Annonymous_Forces#8796 for code', inline=False)
    embed.add_field(name ='+kick', value 
=' New Function Thanks To @Annonymous_Forces#8796 for code'
,inline=False)

    await client.send_message(author, embed=embed)


@client.command(pass_context = True)
async def clear(ctx, amount = 10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' messages were deleted so ya! ')


@client.command(pass_context =True)
async def video(ctx):
    author = ctx.message.author
    embed = discord.Embed(Colour = discord.Colour.orange())
    embed.set_author(name = 'New Video Commands')
    embed.add_field(name ='Subscribe LixorHaxz YT', value ='https://youtu.be/pBlOIZUYmDA', inline=False)

    await client.send_message(author, embed=embed)
    
    
@client.command()
async def findworld(type):
	await client.say('https://growtopiagame.com/worlds/'f'{type}.png')
	
	
@client.command()
async def link(type):
	await client.say('https://www.ss'f'{type}')
    
    

@client.command(pass_context = True)
async def join(ctx):
    channel =  ctx.message.author.voice.voice_channel
    embed = discord.Embed(
        title = 'Voice channel',
        description = 'commands for the voice channel.',
        colour = discord.Colour.blue())

    embed.add_field(name = '+play', value = 'play youtube audio with url', inline = False)
    embed.add_field(name = '+pause', value = 'pauses audio', inline = False)
    embed.add_field(name = '+resume', value = 'resumes audio', inline = False)
    embed.add_field(name = '+leave', value = 'leave voice channel', inline = False)

    await client.say(embed=embed)
    await client.join_voice_channel(channel)


@client.command(pass_context = True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(pass_context = True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()


@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    """Kick A User from server"""
    await client.kick(userName)
    await client.say("Successfully User Has Been Kicked!")

@client.command(pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, userName: discord.User):
    """Ban A User from server"""
    await client.ban(userName)
    await client.say("Successfully User Has Been Banned!")

@client.command()
async def say(*args):
        output = ''
        for word in args:
            output += word
            output += ' '
        await client.say(output)


@client.command(pass_context=True)
async def memberinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)


client.loop.create_task(change_status())
client.run(my_token)
