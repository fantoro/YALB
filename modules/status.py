#!/usr/bin/python

'''
   Copyright 2021 fantoro

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from discord.ext import commands
import discord

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def setGame(self, name):
        print("Setting status")
        status = discord.Game(name)
        await self.bot.change_presence(activity=status)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setGame("{0}help".format(self.bot.command_prefix))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def playing(self, ctx, *, name):
        response = discord.Embed(title="playing")
        response.add_field(name="Setting status...", value="Setting status to: Playing {0}".format(name))
        await ctx.send(embed=response)

        await self.setGame(name);

def setup(bot):
    print("Loading Status")
    bot.add_cog(Status(bot))

def teardown(bot):
    print("Unloading Status")
    bot.remove_cog("Status")
