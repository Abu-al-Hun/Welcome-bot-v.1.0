import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import os
from art import text2art  
from colorama import Fore, Style, init

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))
Exit_channel = int(os.getenv('Exit_channel'))
EMBED_IMAGE_URL = os.getenv('EMBED_IMAGE_URL')
BUTTON_URL = os.getenv('BUTTON_URL')
BUTTON_NAME = os.getenv('BUTTON_NAME')  
member_ROLE_ID = int(os.getenv('member_ROLE_ID'))  
BOT_ROLE_ID = int(os.getenv('BOT_ROLE_ID'))  

intents = discord.Intents.default()
intents.members = True  

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    try:
        # Create ASCII Art text for "Data Team Skoda"
        ascii_art_text = text2art("Wick Studio")

        # Print the ASCII Art text in the console with light color
        print(Fore.LIGHTCYAN_EX + ascii_art_text + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX + f"Logged in as {bot.user}" + Style.RESET_ALL)

        # Change bot presence
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name="Wick Studio"))
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error in on_ready event: {e}" + Style.RESET_ALL)
        
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Wick Studio!", 
            description=f"Hello {member.mention}, welcome to the server!", 
            color=0xf30d0d
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="👥 Current Member Count", value=f"{member.guild.member_count}", inline=False)
        embed.set_footer(text="We're glad to have you with us!")
        embed.set_image(url=EMBED_IMAGE_URL)

        button = Button(label=BUTTON_NAME, url=BUTTON_URL)
        view = View()
        view.add_item(button)
        
        await channel.send(embed=embed, view=view)

    if member.bot:
        role = discord.utils.get(member.guild.roles, id=BOT_ROLE_ID)
    else:
        role = discord.utils.get(member.guild.roles, id=member_ROLE_ID)

    if role:
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            print(f"Bot does not have permission to add roles.")
        except discord.HTTPException as e:
            print(f"An error occurred while adding the role: {e}")
    else:
        print(f"Role ID {member_ROLE_ID} or {BOT_ROLE_ID} not found for member join event.")

@bot.event
async def on_member_remove(member):
    leave_channel = bot.get_channel(Exit_channel)
    if leave_channel:
        embed = discord.Embed(
            title="👋 Member Left",
            description=f"{member.name} has left the server.",
            color=0xf30d0d
        )
        embed.set_footer(text="We're sorry to see you go.")
        await leave_channel.send(embed=embed)
    else:
        print(f"Channel ID {Exit_channel} not found for member leave event.")

bot.run(DISCORD_TOKEN)
