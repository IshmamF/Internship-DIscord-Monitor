import discord
import requests
import json
import aiohttp
import internships
import asyncio
from discord_webhook import AsyncDiscordWebhook
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord.ext import commands
import time

TOKEN = ""
CHANNEL_ID = 

intents=discord.Intents.all()

class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        help_message = '# Commands:\n\n' \
                   '**%webhook <insert webhook>** - set the webhook where you want the monitor to send updates, omit the <>\n' \
                   '**%all <insert state as two letters>** - allows you to toggle through all the internships and filter state you want, including the filter is not required. Omit the <>'
        await self.get_destination().send(help_message)

client = commands.Bot(command_prefix='%', intents=intents, help_command=CustomHelpCommand())


def webhook(locations, company_name, internship_info, company_site):
    webhook = DiscordWebhook(url="", username="Internship")

    if company_site:
        embed = DiscordEmbed(
            title=company_name, description=locations + '\n' + '**Site:** ' + company_site, color='03b2f8'
        )
    else: 
        embed = DiscordEmbed(
            title=company_name, description=locations, color='03b2f8'
        )

    embed.set_author(
        name= "Pitt Computer Science Club",
        url="https://github.com/pittcsc/Summer2024-Internships",
        icon_url="https://avatars.githubusercontent.com/u/7276234?s=200&v=4",
    )

    embed.set_timestamp()
    for role, website in internship_info.items():
        if website == 0:
            website = ''
        embed.add_embed_field(name=role, value=website, inline=False)
    
    webhook.add_embed(embed)
    response = webhook.execute()

async def update_internships(current_internships, current_num_interns):

    while True:
        new_intern_list = internships.get_internships()
        new_num_interns = len(new_intern_list) - current_num_interns

        if new_num_interns > 0:
            new_internships_list = internships.new_internships(new_intern_list, new_num_interns)

            for item in new_internships_list:
                title, link = internships.get_internship_title(item)
                locations = internships.get_locations(item)
                internship_roles = internships.intern_dictionary(item)
                webhook(locations, title, internship_roles, link)
            
            current_internships = new_intern_list
            current_num_interns = len(current_internships)

            await asyncio.sleep(600)  # Wait for 10 minutes

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    current_internships = internships.get_internships()
    current_num_interns = len(current_internships)

    client.loop.create_task(update_internships(current_internships, current_num_interns))

client.run(TOKEN)