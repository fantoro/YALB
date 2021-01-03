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

class HelloWorld(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Hello World!")
    async def helloworld(self, ctx):
        await ctx.send("Hello World!")

def setup(bot):
    print("Loading HelloWorld")
    bot.add_cog(HelloWorld(bot))

def teardown(bot):
    print("Unloading HelloWorld")
    bot.remove_cog("HelloWorld")
