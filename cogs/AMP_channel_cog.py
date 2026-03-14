from __future__ import annotations
import discord
from discord.ext import commands
from discord import app_commands
import logging
import os


import AMP_Handler
import DB as DB
import modules.banner_creator as BC
import utils

# Assuming utils and AMP_Handler are imported as in other cogs
# from .. import utils, AMP_Handler, DB
Dependencies = ['AMP_server_cog.py']

class ChannelCog(commands.Cog):
    def __init__(self, client: discord.Client):
        self._client = client
        self.logger = logging.getLogger()
        self.AMPHandler = AMP_Handler.getAMPHandler()
        self.AMPInstances = self.AMPHandler.AMP_Instances
        self.DBHandler = DB.getDBHandler()
        self.DB = self.DBHandler.DB

    @commands.hybrid_group(name='server')
    async def server(self, context: commands.Context):
        if context.invoked_subcommand is None:
            await context.send('Please try your command again...', ephemeral=True, delete_after=self._client.Message_Timeout)

    @server.command(name='channel')
    @app_commands.autocomplete(server=utils.autocomplete_servers)
    async def server_channel_init(self, context: commands.Context, server):
        """Creates a category and channels for the AMP server (console, events, chat) and links them."""
        self.logger.command(f'{context.author.name} used Server Channel Init...')
        await context.defer(ephemeral=True)

        amp_server = await utils.botUtils(self._client)._serverCheck(context, server, False)
        if not amp_server:
            return await context.send('Server not found.', ephemeral=True, delete_after=self._client.Message_Timeout)

        guild = context.guild
        category_name = f"{amp_server.InstanceName}"
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            category = await guild.create_category(category_name)
            self.logger.info(f"Created category: {category_name}")

        # Create channels if not exist
        channel_names = {
            "console": f"{amp_server.InstanceName}-console",
            "chat": f"{amp_server.InstanceName}-chat",
            "events": f"{amp_server.InstanceName}-events"
        }
        created_channels = {}
        for key, name in channel_names.items():
            channel = discord.utils.get(category.channels, name=name)
            if not channel:
                channel = await guild.create_text_channel(name, category=category)
                self.logger.info(f"Created channel: {name}")
            created_channels[key] = channel

        # Link channels to AMP server in DB
        db_server = self.DB.GetServer(InstanceID=amp_server.InstanceID)
        db_server.Console_Channel = created_channels["console"].id
        db_server.Discord_Chat_Channel = created_channels["chat"].id
        db_server.Discord_Event_Channel = created_channels["events"].id
        amp_server._setDBattr()

        await context.send(
            f"Initialized channels for **{amp_server.InstanceName}**:\n"
            f"- Console: <#{created_channels['console'].id}>\n"
            f"- Chat: <#{created_channels['chat'].id}>\n"
            f"- Events: <#{created_channels['events'].id}>",
            ephemeral=True, delete_after=self._client.Message_Timeout
        )

async def setup(client):
    await client.add_cog(ChannelCog(client))