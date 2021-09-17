import typing
import discord

class Colour:
  def __init__(
    self,
    hex: int
  ) -> None:
    self.hex=hex

class Guild:
  def __init__(
    self,
    colour: Colour,
    name: str
  ) -> None:
    self.colour=colour.hex
    self.name=name
    
    self.members: typing.List[discord.Member] = []
    
  
  @property
  def members(
    self
  ) -> typing.List[discord.Member]:
    return self.members
  
  def not_yet_guild(
    func
  ) -> typing.Any:
    def wrapper(*args, **kwargs):
      if args[0] not in self.members:
        func(*args, **kwargs)
        return
      else:
        return
 
  def in_guild(
    func
  ) -> typing.Any:
    def wrapper(*args, **kwargs):
      if args[0] not in self.members:
        return
      else:
        func(*args, **kwargs)
        return
  
  @not_yet_guild
  def add_member(
    self,
    member: discord.Member
  ) -> None:
    self.members.append(member)
    
  @in_guild
  def remove_member(
    self,
    member: discord.Member
  ) -> None:
    self.members.remove(member)
