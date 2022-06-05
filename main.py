from ast import Break
from lib2to3.pgen2 import token
from xml.dom.minidom import CharacterData
import discord, asyncio, random, json
from discord.ext import commands

gameCommands = ["!hp","!attack","!defense","!stats"]
players = {
    "EMPTYUSER" : {
        "HP" : 100,
        "ATK" : 1,
        "DEF" : 1,
        "XP" : 0,
        "LVL" :0,
        "POS" : [0,0],
        "LVL" :0
    }
}

TOKEN = 'OTgyNTMwODQxOTExNjU2NDQ4.Gn2xOP.PhKhabeAELW5hYhE1pYqviUBQgb7XzvxDwazJk'
client = commands.Bot(command_prefix=["dnd!"],help_command=None)

async def gameLoop(boundChannel):
    await client.wait_until_ready()
    channel = client.get_channel(id=861686873197641731)
    while not client.is_closed():
        return

@client.command(invoke_without_command=True)
async def help(ctx,*,specific=None):
    if specific==None:
        embed = discord.Embed(title="**Help List**",description="Help shows this command",color=discord.Color.blurple())
    else:
        embed = discord.Embed(title="**Command Not Found**",color=discord.Color.red())
    await ctx.send(embed=embed)  

@client.event
async def on_ready():
    print("I'm in " + str(len(client.guilds)) + " servers!")
    print("Logged into {0.user}".format(client))
    print("Formatting playerData to Dict")
    with open('playerData.json') as json_file:
        global players
        data = json.load(json_file)
        players = data
        print(players)
    print("Finished!")

@client.event
async def on_message(message):
    rawUsername = str(message.author)
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    boundChannel = client.get_channel(id=982757997497446410)
    echoTo   = client.get_channel(id=954888757507678230)
    channel = str(message.channel.name)
    
    if message.author == client.user:
        return
    elif user_message == "!createcharacter":
        try:
            players[rawUsername]
            await message.channel.send(f"Character for {username} ({rawUsername}) already exists!")
        except:
            players[rawUsername] = players["EMPTYUSER"]
            await message.channel.send(f"Character for {username} created!")
            with open("playerData.json", "w") as outfile:
                json.dump(players, outfile)

    elif user_message in gameCommands:
        try:
            players[rawUsername]
            if user_message == "!stats":
                await message.channel.send(players[rawUsername])
            elif user_message == "!attack":
                await message.channel.send(players[rawUsername]["ATK"])
            elif user_message == "!defense":
                await message.channel.send(players[rawUsername]["DEF"])
            elif user_message == "!hp":
                await message.channel.send(players[rawUsername]["HP"])
        except KeyError:
            await message.channel.send("Character doesn't exist yet, use '!createcharacter' to make one!")
        except:
            await message.channel.send("An error occured.")

client.run(TOKEN)