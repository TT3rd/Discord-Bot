import discord
import random
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from random import choice
import youtube_dl
import giphy_client
from giphy_client.rest import ApiException

youtube_dl.utils.bug_reports_message = lambda: ''

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
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
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

client = commands.Bot(command_prefix = 'v.')
status = ['V!b!ng']
queue = []

#music commands

@client.command(name='q')
async def q(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')


async def play_next():
    player = await YTDLSource.from_url(queue[0], loop=client.loop)
    voice_channel.play(player, after=lambda e: play_next())


@client.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send('You are not connect to a vc')
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@client.command(name='vibe')
async def play(ctx):
    global queue

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: play_next())

    await ctx.send(f'**Now playing:** {player.title}')
    del(queue[0])

@client.command(name='x')
async def vibe(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

#giphy commands
@client.command()
async def hug(ctx,*,q="anime hug"):

    api_key = 'S1ThmcgfgUrdoIcFI3LINBnKWJZxGhZS'
    api_instance = giphy_client.DefaultApi()

    try:

        api_responce = api_instance.gifs_search_get(api_key, q, limit=5, rating='r')
        lst = list(api_responce.data)
        giff = random.choice(lst)

        await ctx.channel.send(giff.embed_url)

    except ApiException as e:
        print("Exception when calling Api")


@client.command()
async def slap(ctx,*,q="anime slap"):

    api_key = 'S1ThmcgfgUrdoIcFI3LINBnKWJZxGhZS'
    api_instance = giphy_client.DefaultApi()

    try:

        api_responce = api_instance.gifs_search_get(api_key, q, limit=20, rating='r')
        lst = list(api_responce.data)
        giff = random.choice(lst)

        await ctx.channel.send(giff.embed_url)

    except ApiException as e:
        print("Exception when calling Api")

@client.command()
async def rko(ctx,*,q="rko"):

    api_key = 'S1ThmcgfgUrdoIcFI3LINBnKWJZxGhZS'
    api_instance = giphy_client.DefaultApi()

    try:

        api_responce = api_instance.gifs_search_get(api_key, q, limit=20, rating='r')
        lst = list(api_responce.data)
        giff = random.choice(lst)

        await ctx.channel.send(giff.embed_url)

    except ApiException as e:
        print("Exception when calling Api")

@client.command()
async def ddt(ctx,*,q="ddt"):

    api_key = 'S1ThmcgfgUrdoIcFI3LINBnKWJZxGhZS'
    api_instance = giphy_client.DefaultApi()

    try:

        api_responce = api_instance.gifs_search_get(api_key, q, limit=20, rating='r')
        lst = list(api_responce.data)
        giff = random.choice(lst)

        await ctx.channel.send(giff.embed_url)

    except ApiException as e:
        print("Exception when calling Api")

@client.command()
async def thanks(ctx,*,q="thank you"):

    api_key = 'S1ThmcgfgUrdoIcFI3LINBnKWJZxGhZS'
    api_instance = giphy_client.DefaultApi()

    try:

        api_responce = api_instance.gifs_search_get(api_key, q, limit=20, rating='r')
        lst = list(api_responce.data)
        giff = random.choice(lst)

        await ctx.channel.send(giff.embed_url)

    except ApiException as e:
        print("Exception when calling Api")



#basic commands/events
@client.event
async def on_ready():
    change_status.start()
    print('Bot is Ready.')

@client.event
async def on_member_join(ctx):
    change_status.start()
    await ctx.send('Yo wsp, have fun')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(name='credits')
async def credits(ctx):
    await ctx.send('Made by **T^3**')
    await ctx.send('Help from **Mission Bit**')

@client.command()
async def helpme(ctx):
    await ctx.send('**Wsp Im the V!be bot, and Im here to make using Discord a lot funner and easier**')
    await ctx.send('**I can be used to play music**')
    await ctx.send('**v.join makes me join Vc.  v.x removes me from vc  v.q allows you to add a song to the queue. v.vibe plays the next song on the queue**')


@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run('YOUR TOKEN')
