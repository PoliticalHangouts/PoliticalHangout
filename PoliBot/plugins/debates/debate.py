import discord
import typing
from plugins.debates.data import *

from discord_slash import cog_ext, SlashContext
from discord.ext import commandd

class MustHaveOneArgumentError(Exception):
  def __str__(self) -> str:
    return "You must have at least one option when using this command."

debate_rooms = [
  888483117701156896
]  
  
class Debates(commands.Cog):
  def __init__(
    self,
    bot: commands.Bot
  ) -> None:
    self.bot=bot
    
    self.choices = [
      {
      "name": "None",
      "value": "null"
      }
    ]
    
    self.debate_room = None
    
    self.voters = []
    
    
  def only_debate_rooms(
    func
  ) -> None:
    def wrapper(*args, **kwargs):
      if args[0].channel.id in debate_rooms:
        func(*args, **kwargs)
        return
      else:
        pass
    return wrapper
  
  def not_yet_voted(
    func
  ) -> None:
    def wrapper(*args, **kwargs) -> None:
      if args[0].author.id in self.voters:
        pass
      else:
        func(*args, **kwargs)
        return
    return wrapper
    
  @only_debate_rooms
  @not_yet_voted
  @cog_ext.cog_slash(
    name="proposition",
    description="Sets a proposition, or votes for that of another member",
    options = [
      {
        "name": "proposition",
        "description": "The propoition you want to set.",
        "option_type": 4,
        "required": False,
        "default": "null"
      },
      {
        "name": "member",
        "description": "The member whose proposition you would like to vote for.",
        "option_type": 7,
        "choices": self.choices
        "required": False
        "default": "null"
      }
    ]
  )
  async def _proposition(
    self,
    ctx: SlashContext,
    proposition: str,
    member: str
  ) -> typing.Union(discord.Message, None):
    if proposition == "null" and member == "null":
      raise MustHaveOneArgumentError()
    elif proposition == "null":
      proposition = self.debate_room.get_prop_by_id(member.id)
      return await ctx.channel.send(
        embed = discord.Embed(
          description="Voted for proposition {}!".format(proposition)
          color=discord.Colour.green()
        ).set_author(name="Vote casted!")
      )
    else:
      if self.debate_room:
        self.debate_room.props.append(
          Proposition(
            proposition,
            ctx.author,
            ctx.message
          )
        )
        
        self.choices.append(
          {
            "name": "{}".format(ctx.author.display_name),
            "value": ctx.author
          }
        )
        
        return await ctx.channel.send(
          "Proposition set up for voting!"
        )
      else:
        self.debate_room = DebateRoom(
          [ctx.author]
        )
        
        self.debate_room.props.append(
          Proposition(
            proposition,
            ctx.author,
            ctx.message
          )
        )
        
        self.choices.append(
          {
            "name": "{}".format(ctx.author.display_name),
            "value": ctx.author
          }
        )
        
        message = await ctx.channel.send(
          embed=discord.Embed(
            description="{}".format(proposition),
            color=discord.Colour.green()
          ).set_author(name="Proposition set!")
        )
        
        await message.pin()
        
        return
   
      
