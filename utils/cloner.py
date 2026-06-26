import discord
import asyncio
import aiohttp

class Cloner:

  @staticmethod
  async def guild_create(guild_to, guild_from, on_progress=None):
    try:
      icon_image = None
      if guild_from.icon:
        try:
          icon_image = await guild_from.icon.read()
        except discord.errors.DiscordException:
          pass
      await guild_to.edit(name=f'{guild_from.name}')
      if icon_image is not None:
        try:
          await guild_to.edit(icon=icon_image)
        except Exception:
          pass
    except discord.errors.Forbidden:
      pass
    if on_progress:
      on_progress("Sunucu profili", 1, 1)

  @staticmethod
  async def roles_create(guild_to, guild_from, on_progress=None):
    roles = [role for role in guild_from.roles if role.name != "@everyone"]
    roles.reverse()
    total = len(roles)
    for i, role in enumerate(roles):
      try:
        kwargs = {
          'name': role.name,
          'permissions': role.permissions,
          'colour': role.colour,
          'hoist': role.hoist,
          'mentionable': role.mentionable
        }
        await guild_to.create_role(**kwargs)
      except (discord.Forbidden, discord.HTTPException):
        pass
      if on_progress:
        on_progress("Roller", i + 1, total)

  @staticmethod
  async def channels_delete(guild_to, on_progress=None):
    channels = guild_to.channels
    total = len(channels)
    for i, channel in enumerate(channels):
      try:
        await channel.delete()
      except (discord.Forbidden, discord.HTTPException):
        pass
      if on_progress:
        on_progress("Kanallar (silme)", i + 1, total)

  @staticmethod
  async def categories_create(guild_to, guild_from, on_progress=None):
    channels = guild_from.categories
    total = len(channels)
    for i, channel in enumerate(channels):
      try:
        overwrites_to = {}
        for key, value in channel.overwrites.items():
          target = discord.utils.get(guild_to.roles, name=getattr(key, 'name', None))
          if target is None:
            target = guild_to.get_member(getattr(key, 'id', None))
          if target:
            overwrites_to[target] = value
        new_channel = await guild_to.create_category(name=channel.name, overwrites=overwrites_to)
        await new_channel.edit(position=channel.position)
      except (discord.Forbidden, discord.HTTPException):
        pass
      if on_progress:
        on_progress("Kategoriler", i + 1, total)

  @staticmethod
  async def channels_create(guild_to, guild_from, on_progress=None):
    channels = guild_from.text_channels + guild_from.voice_channels
    channel_types = {
      discord.TextChannel: guild_to.create_text_channel,
      discord.VoiceChannel: guild_to.create_voice_channel
    }
    total = len(channels)
    for i, channel in enumerate(channels):
      await asyncio.sleep(0.2)
      category = discord.utils.get(guild_to.categories, name=getattr(channel.category, "name", None))
      overwrites_to = {}
      for key, value in channel.overwrites.items():
        target = discord.utils.get(guild_to.roles, name=getattr(key, 'name', None))
        if target is None:
          target = guild_to.get_member(getattr(key, 'id', None))
        if target:
          overwrites_to[target] = value
      try:
        new_channel = await channel_types[type(channel)](name=channel.name, overwrites=overwrites_to, position=channel.position)
        if category is not None:
          await new_channel.edit(category=category)
      except (discord.Forbidden, discord.HTTPException, Exception):
        pass
      if on_progress:
        on_progress("Kanallar", i + 1, total)

  @staticmethod
  async def emojis_create(guild_to, guild_from, on_progress=None):
    total = len(guild_from.emojis)
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession(headers=headers) as session:
      for i, emoji in enumerate(guild_from.emojis):
        try:
          await asyncio.sleep(0.2)
          async with session.get(emoji.url) as resp:
            emoji_image = await resp.read()
          await guild_to.create_custom_emoji(name=emoji.name, image=emoji_image)
        except (discord.Forbidden, discord.HTTPException):
          pass
        if on_progress:
          on_progress("Emojiler", i + 1, total)