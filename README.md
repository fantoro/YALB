# Yet Another Last.fm Bot

**YALB** *(or **Y**et **A**nother **M**usic **B**ot)* will be a [Discord](https://discord.com/)
music bot made with [Last.fm](https://last.fm/) scrobbling in mind.

## Why?

I noticed that none of the popular music bots on Discord have any sort of scrobbling feature so I decided to make one that scrobbles myself.

## TODO

 - [ ] Last.fm account integration
   - [ ] Last.fm API
     - [x] Extremely basic API integration
   - [ ] Last.fm login
   - [ ] Last.fm stats commands
   - [ ] Automatic scrobbling for users in the voice channel who have linked their Last.fm accounts
     - [ ] Make it opt-in/easily togglable
 - [ ] Music playback in Discord voice channels
   - [ ] Queue system
     - [ ] Decide on the queue system database (maybe store it in the memory, I don't care about scalability this bot isn't gonna be on many servers most likely, although it is a good idea to future proof for anything so I don't know)
   - [ ] Better integration with `asyncio` in some of the methods
   - [ ] Custom `discord.py` `VoiceClient` to better track everything (also might take care of the previous TODO/TODOs)
   - [x] `youtube-dl` integration
 - [ ] Better `help` command that integrates with `discord.py`'s `ext.commands` better
 - [ ] Improved performance *(might require a rewrite considering how fucking awful my code is)*
 - [x] Terrible and simple module system for improved maintainability and rewritability
   - [ ] Make the module system actually good
 - [ ] Try to focus and actually make a good TODO list
 - [x] Have no fucking clue what you're doing
