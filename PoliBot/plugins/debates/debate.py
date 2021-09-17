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
    
    self.concluders = []
    
    
  @property
  def get_debater_choices(
    self
  ) -> typing.Any:
    choices = []
    for debater in self.debate_room.debaters:
      choices.append(
        {
          name=debater.name,
          value=debater.member
        }
      )
    return choices
    
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
    
  @commands.Cog.listener()
  async def on_voice_state_update(
    self,
    member: discord.Member,
    before,
    after
  ) -> None:
    if after.channel.id == 806018840176885791 and not member.bot:
      if not self.debate_room:
        self.debate_room = DebateRoom(
          [ctx.author]
        )
      self.debate_room.add_participant(
        User(
          member.display_name,
          member
        )
      )
    if not after.channel:
      self.debate_room.participants.remove(self.debate_room.get_user_by_id(member.id))
    pass
      
    
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
        "choices": self.choices,
        "required": False,
        "default": "null"
      }
    ]
  )
  async def _proposition(
    self,
    ctx: SlashContext,
    proposition: str,
    member: discord.Member
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
   
  @only_debate_rooms
  @cog_ext.cog_slash(
    name="for",
    description="Sets you as for the proposition: {}".format(self.debate_room.proposition)
  )
  async def _for(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    self.debate_room.get_user_by_id(ctx.author.id).stance = "for"
    return await ctx.channel.send("Stance set to **for**")
  
  @only_debate_rooms
  @cog_ext.cog_slash(
    name="against",
    descrption="Sets you as against the proposition: {}".format(self.debate_room.proposition)
  )
  async def _against(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    self.debate_room.get_user_by_id(ctx.author.id).stance = "against"
    return await ctx.channel.send("Stance set to **against**")
      
  @only_debate_rooms
  @cog_ext.cog_slash(
    name="debate",
    description="Sets you as a debater for proposition: {}".format(self.debate_room.proposition)
  )
  async def _debate(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    self.debate_room.add_debater(self.debate_room.get_user_by_id(ctx.author.id))
    return await ctx.channel.send("You are now debating proposition: {}".format(self.debate_room.proposition))
  
  @only_debate_rooms
  @cog_ext.cog_slash(
    name="vote",
    description="Allowa you to vote for a member of your choice."
    options = [
      {
        "name": "member",
        "description": "The member you would like to vote for.",
        "option_type": 7,
        "choices" = self.get_debater_choices,
        "required": True
      }
    ]
  )
  async def _vote(
    self,
    ctx: SlashContext,
    member: discord.Member
  ) -> discord.Message:
    self.debate_room.get_user_by_id(member.id).votes += 1
    return await ctx.channel.send("Set vote for {}".format(member.display_name))
  
  @only_debate_rooms
  @cog_ext.cog_slash(
    name="conclude",
    description="Conclude a debate"
  )
  async def _conclude(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    self.concluders.append(ctx.author)
    if self.concluders / len(self.debate_room.participants) > 0.49:
      outcome = self.debate_room.end(self.debate_room.winner, self.debate_room.loser)
      return await ctx.channel.send(
        embed = discord.Embed(
          description="Debate concluded with {} votes.".format(len(self.concluders)),
          color=discord.Colour.green()
        ).set_author(name="Debate concluded.").add_field(title=self.debate_room.winner.name, value = self.debate_room.winner.final_points).add_field(title=self.debate_room.loser.name, value=self.debate_room.loser.final_points)
    else:
        return await ctx.channel.send("Vote cast to conclude.")
        
def setup(bot):
  bot.add_cog(Debates(bot))
