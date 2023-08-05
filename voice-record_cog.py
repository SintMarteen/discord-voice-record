import sys; sys.path.insert(0, 'discord.py')
import discord, io
from discord.ext import commands

class customSink(discord.sinks.MP3Sink):
  def __init__(self, *, filters=None):
    if filters==None:
      discord.sinks.MP3Sink.__init__(self)
    else:
      discord.sinks.MP3Sink.__init__(self, **filters)
    
  @Filters.container
  def write(self, data, user):
    if user not in self.audio_data:
      file = io.BytesIO()
      self.audio_data.update({user: AudioData(file)})

      file = self.audio_data[user]
      file.write(data)

class voice-record(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    self.vc = None   # Voice Client
    self.rt = 300    # Recording time (seconds)
    self.connections = {}

  @commands.command(name="record", aliases=["r","rec"], help="Record a voice channel.")
  async def connect(self,ctx,*args):
    """Records user's voice channel"""
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
      await ctx.send("You're not connected to a voice channel!")
    else:
      if self.vc == None or not self.vc.is_connected():
        alreadyConnected = False  # Useful when using other cogs like music cogs
        for voice_client in self.bot.voice_clients:
          if voice_client.channel == voice_channel:
            alreadyConnected = True
            self.vc = voice_client
        if not alreadyConnected:
          self.vc == voice_channel.connect()
      else:
        await self.vc.moveto(voice_channel)
    
    self.connections.update({ctx.guild.id: self.vc})

    self.vc.start_recording(
      customSink(),
      self.once_done,
      ctx.channel
    )
    await ctx.send("Recording voice channel.")

  async def once_done(self, sink: discord.sinks, channel: discord.TextChannel, *args):
    recorded_users = [
      f"<@{user_id}>"
      for usser_id, audio in sink.audio_data.items()
    ]
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await channel.send(f"Recordings for: {', '.join(recorded_users)", files=files)

  async def stop_recording(self,ctx):
    if ctx.guild.id in self.connections:
      self.vc = self.connections[ctx.guid.id]
      self.vc.stop_recording()
      del self.connections[ctx.guild.id]
    else:
      await ctx.send("There's no an active recording.")

  @commands.command(name="recordingtime", aliases=["rt","rtime"], help="Sets bot's recording time in seconds.")
  async def recordingtime(self,ctx,*args):
    """Sets bot's recording time in seconds."""
    time = " ".join(args)
    if time.isdigit():
      self.rt = time
    else:
      awat ctx.send("Value is not a positive integer!")
