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
import discord, os

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as {0}.".format(str(self.bot.user)))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def getmodules(self, ctx):
        cogs = self.bot.cogs.keys()
    
        response = discord.Embed(title="getmodules")
        respValue = "```\n"
        for cog in cogs:
            respValue += "{0}\n".format(cog)
        respValue += "```"

        response.add_field(name="Modules", value=respValue)

        '''
        response = "List of loaded modules:\n```"
        for cog in cogs:
            response += "{0}\n".format(cog)
        response += "```"
        '''

        await ctx.send(embed=response)

    @commands.command(description="Shows you this message")
    async def help(self, ctx):
        cmds = self.bot.commands
        
        response = discord.Embed(title="help")
        for cmd in cmds:
            if not cmd.hidden:
                if cmd.description != "":
                    response.add_field(name=cmd.name, value=cmd.description)
                else:
                    response.add_field(name=cmd.name, value="No description")

        await ctx.send(embed=response)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx):
        response = discord.Embed(title="reload")
        response.add_field(name="Reloading modules...", value="Reloading Core...")
        await ctx.send(embed=response)
        print("Reloading modules...")

        self.bot.reload_extension("core")

        response = discord.Embed(title="reload")
        response.add_field(name="Done!", value="Reloaded all modules")
        await ctx.send(embed=response)
        print("Done!")
    
def setup(bot):
    print("Loading Core")
    bot.add_cog(Core(bot))

    if not os.path.isdir("./modules"):
        return
    files = os.listdir("./modules")
    for f in files:
        fi = "./modules/{0}".format(f)
        if os.path.isfile(fi):
            if len(fi) < 3:
                continue

            ext = fi[-3:]
            if ext != ".py":
                continue

            module = f[:-3]
            bot.load_extension("modules.{0}".format(module))

def teardown(bot):
    print("Unloading Core")
    bot.remove_cog("Core")
    
    modules = bot.extensions.keys()
    for m in modules:
        bot.unload_extension(m)
