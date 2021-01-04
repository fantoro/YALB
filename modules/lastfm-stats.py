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
import requests, time, discord, musicbrainzngs, modules.lastfmstats.secrets

class LastfmStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = modules.lastfmstats.secrets.token
        self.lastcall = 0
        musicbrainzngs.set_useragent("YALB", "0.1", "https://github.com/fantoro/YALB")

    def api(self, payload):
        if time.time() - self.lastcall < 2:
            time.sleep(3)

        headers = {"User-Agent": "YALB/0.1"}

        payload["api_key"] = self.key
        payload["format"] = "json"
        
        response = requests.get("http://ws.audioscrobbler.com/2.0/", headers=headers, params=payload)
        self.lastcall = time.time()
        
        return response.json()

    @commands.command(description="Returns top track for given user")
    async def toptrack(self, ctx, username):
        payload = {
            "method": "user.gettoptracks",
            "user": username,
            "period": "overall",
            "limit": "1"
        }

        trackdata = self.api(payload)

        response = discord.Embed(title="toptrack")
        if "error" in trackdata:
            response.add_field(name="Failed to load top track", value=trackdata["message"])
            await ctx.send(embed=response)
            return

        toptrack = trackdata["toptracks"]["track"][0]
        response.add_field(name="{0}'s top track".format(username), value="{0} - {1}".format(toptrack["artist"]["name"], toptrack["name"]))

        recording = musicbrainzngs.search_recordings(tid=toptrack["mbid"])
        recording = recording["recording-list"][0]
        release = recording["release-list"][0]
        imgs = musicbrainzngs.get_image_list(release["id"])

        url = requests.get(imgs["images"][0]["thumbnails"]["small"])
        url = url.url
        
        response.set_thumbnail(url=url)

        await ctx.send(embed=response)

def setup(bot):
    print("Loading LastfmStats")
    bot.add_cog(LastfmStats(bot))

def teardown(bot):
    print("Unloading LastfmStats")
    bot.remove_cog("LastfmStats")
