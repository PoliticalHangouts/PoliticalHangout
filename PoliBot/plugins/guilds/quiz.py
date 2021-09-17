import typing
import discord

import asyncio

from plugins.guilds.data import Guild
from discord.ext import commands

class Response:
  def __init__(
    self,
    values = typing.Tuple[int, int],
  ) -> None:
    self.values=values

async def create_question(
  question_number: int,
  prompt: str,
  options: typing.List[str],
  time_limit: int,
  bot: commands.Bot,
  ctx: commands.Context,
  guild: Guild,
  values: typing.Dict[str, Tuple(int)]
) -> Response:
  message = await ctx.send(
    embed = discord.Embed(
      description="```\n{}```".format(
        prompt
      ),
      color=guild.colour
    ).set_author(name="Question {0} - {1}".format(
      question_number,
      time_limit
    ))
  )
  
  for option in options:
    message.add_reaction(option)
  
  await asyncio.sleep(2)
  
  response = await bot.wait_for(
    'reaction_add',
    check=lambda reaction, user: reaction.message == message and reaction.emoji in options and reaction.user == ctx.author, time_limit
  )
  
  return Response(
    values[response[0].emoji]
  )
