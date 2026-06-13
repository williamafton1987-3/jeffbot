import discord
import random
import time
import os, json
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands
load_dotenv(".env")
token = os.getenv("BOTKEY")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
trusteduser = int(os.getenv("TRUSTEDUSER"))
jeffserver = int(os.getenv("JEFFSERVER"))
@bot.event
async def on_ready():
    print(f'the bot is in {len(bot.guilds)} servers.')
    print(f'Logged on as {bot.user}!')
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
        cleardatastore.start()
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not message.guild.id == jeffserver:
        return
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

storedppsizes = {}

def comparetime(key: int):
    if key in storedppsizes:
        storedtime = storedppsizes[key]["currtime"]
        epochtime = int(time.time())
        if (abs(epochtime - storedtime)) >= 60:
            return True
        else:
            storedppsizes.pop(key)
            return False
    else:
        return False

@bot.tree.command(name="dihsize", description="Measure dihsizes!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def dihsize(interaction: discord.Interaction, user: discord.User):
    userid=user.id
    rigtheseids = {963992516598837339: [5,30], 1508688100002369600: [1,5], 1148756266567614468: [15,25], 1295157844617723976: [1,1], 877773433977589780: [0, 25], 1165247192504729742: [1, 3]}
    ppsize = 0

    if comparetime(userid):
        ppsize = storedppsizes[userid]["size"]
    elif userid in rigtheseids:
        ppsize = min(random.randint(rigtheseids[userid][0], rigtheseids[userid][1]), random.randint(rigtheseids[userid][0], rigtheseids[userid][1]))
    else:
        ppsize = min(random.randint(1, 25), random.randint(1, 25))
    embed = discord.Embed(
        title=f"**{user.display_name}'s dih size**",
        description=f"**8"+ ("="* ppsize) + "D**",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)
    storedppsizes[userid] = {"size": ppsize, "currtime": int(time.time())}
    print(f"{interaction.user.display_name}({interaction.user.id}) ran dihsize on {user.display_name}({user.id}) with these results in {interaction.guild_id} \n 8{"="*ppsize}D")


@tasks.loop(seconds=60.0)
async def cleardatastore():
    for userid, data in list(storedppsizes.items()):
        storedtime = data["currtime"]
        epochtime = int(time.time())
        if (abs(epochtime - storedtime)) >= 60:
            storedppsizes.pop(userid)


@bot.tree.command(name="clearstoreddata", description="clears stored ppsize data")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def cleardata(interaction: discord.Interaction):
    global storedppsizes
    if interaction.user.id == trusteduser:
        await interaction.response.send_message(f"cleared stored data: ```py\n{json.dumps(storedppsizes, indent = 4)}\n```", ephemeral = True)
        storedppsizes = {}
    else:
        await interaction.response.send_message(f"sorry {interaction.user.display_name}, you arent allowed to use this command", ephemeral = True)

@bot.tree.command(name="viewstoreddata", description="reads stored ppsize data")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def viewdata(interaction: discord.Interaction):
    if interaction.user.id == trusteduser:
        await interaction.response.send_message(f"```python\n{json.dumps(storedppsizes, indent = 4)}\n```", ephemeral= True)
    else:
        await interaction.response.send_message(f"sorry {interaction.user.display_name}, you arent allowed to use this command", ephemeral = True)

@bot.tree.command(name="sendauth", description="sends the bot authorization link")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def auththisapp(interaction: discord.Interaction, target: discord.User):
    await interaction.response.send_message('sending message', ephemeral= True)
    await interaction.followup.send(f"<@{target.id}>\n<https://discord.com/oauth2/authorize?client_id=1512242688685117670>")

nether = app_commands.Group(
    name="nether", 
    description="nether highway",
    allowed_installs=app_commands.AppInstallationType(guild=True, user=True),
    allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)
)

@nether.command(name="register", description="registers your nether highway portal")
async def regportal(interaction: discord.Interaction, name: str, x: int, z: int):
    if len(name) > 39:
        await interaction.response.send_message(f"name is too long, it is {len(name) - 39} character(s) too long")
        return
    portaldata= {}
    with open("netherportal.json", "r", encoding="utf-8") as portaljson:
        portaldata = json.load(portaljson)
    portaldata[name] = {"x":x, "z":z}
    with open("netherportal.json", "w", encoding= "utf-8") as file:
        json.dump(portaldata, file, indent=4)
    await interaction.response.send_message(f"registered {name} at {x}, {z}", ephemeral=True)

@nether.command(name="delete", description="deletes a nether highway entry")
async def delete(interaction: discord.Interaction):
    if interaction.user.id == trusteduser:
        await interaction.response.send_message(ephemeral=True, view=3)
    else:
        await interaction.response.send_message(f"sorry {interaction.user.display_name}, you arent allowed to use this command", ephemeral = True)


bot.tree.add_command(nether)

bot.run(token)