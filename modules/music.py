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
import youtube_dl as ytdl
import discord, threading

async def is_in_voice_channel(ctx):
    return ctx.author.voice.channel != None

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def stoppedPlaying(self, exception):
        print("Stopped playback")
        for vc in self.bot.voice_clients:
            if not vc.is_playing():
                self.bot.loop.create_task(vc.disconnect())

    def PlayYtdl(self, args, ctx, ytdl_opts, vc):
        with ctx.typing():
            with ytdl.YoutubeDL(ytdl_opts) as ydl:
                vid = ydl.extract_info(args)

        if 'entries' in vid:
            vid = vid['entries'][0]

        print(vid)

        audio = discord.FFmpegOpusAudio("./cache/{0}.opus".format(vid["id"]))

    
        print("Playing {0}".format(vid["title"]))
        vc.play(audio, after=self.stoppedPlaying)

        response = discord.Embed(title="play")
        response.add_field(name="Now playing", value=f"[{vid['title']}]({vid['webpage_url']})")
        self.bot.loop.create_task(ctx.send(embed=response))

    @commands.command(description="Plays an audio file")
    @commands.guild_only()
    @commands.check(is_in_voice_channel)
    async def play(self, ctx, *, args):
        if ctx.guild.me.voice == None or ctx.guild.me.voice.channel != ctx.author.voice.channel:
            await ctx.author.voice.channel.connect()

        vc = ctx.guild.voice_client

        if vc.is_playing():
            response = discord.Embed(title="play")
            response.add_field(name="Already Playing", value="The bot is already playing something")
            await ctx.send(embed=response)
            return

        response = discord.Embed(title="play")
        response.add_field(name="Searching...", value=args)
        await ctx.send(embed=response)

        ytdl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'opus',
                    'preferredquality': '128'
                    }],
                'default_search': 'ytsearch',
                'noplaylist': True,
#                'download_archive': './cache/files.txt',
                'outtmpl': './cache/%(id)s.opus'
                }

        t = threading.Thread(target=self.PlayYtdl, args=(args,ctx,ytdl_opts,vc))
        t.start()


def setup(bot):
    print("Loading Music")
    bot.add_cog(Music(bot))

def teardown(bot):
    print("Unloading Music")
    bot.remove_cog("Music")
