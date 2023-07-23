import discord
from discord.ext import commands
import os
import asyncio

class voice-record(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    self.vc = None   # Voice Channel
    self.rt = 300    # Recording time (seconds)

  @commands.command(name="connect", aliases=["c","join","j"], help="Connects to voice channel.")
  async def connect(self,ctx,*args):
    if voice_channel is None:
      await ctx.send("Primero conecta a un canal, tonto estúpido.")
    else:
      if self.vc == None or not self.vc.is_connected():
        self.vc == voice_channel.connect()
      else:
        await self.vc.moveto(voice_channel)
