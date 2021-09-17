import typing
import random
import discord
from replit import db

from plugins.debate import calculation

class User:
  def __init__(
    self,
    name: str,
    member: discord.Member
  ) -> None:
    self.name=name
    self.member = member
    
    self.stance = None
    self.votes = 0
    self.final_points = 0
    
  @property
  def points(
    self
  ) -> int:
    if str(self.member.id) in db["users"]:
      return db["users"][str(self.member.id)]
    else:
      return 200
    
  def set_stance(
    self,
    stance: str
  ) -> None:
    self.stance=stance

class Proposition:
  def __init__(
    self,
    prop: str,
    author: discord.Member,
    message: discord.Message
  ) -> None:
    self.prop=prop

    self.author=author
    
    self.votes: typing.List[discord.Member] = [author]
    
    self.created_at = message.created_at
    self.priority = False

class DebateRoom:
  def __init__(
    self,
    users: typing.List[discord.Member]=[],
    prop: Proposition=None
  ) -> None:
    self.users=users
    self.prop=prop
    
    self.participants: typing.List[User] = []
    self.debaters: typing.List[User] = []
    
  @property
  def for(
    self
  ) -> typing.List[User]:
    for = []
    for participant in self.participants:
      if participant.stance == "for":
        for.append(participant)
      else:
        continue
     return for
  
  @property
  def against(
    self
  ) -> typing.List[User]:
    against = []
    for participant in participants:
      if participant.stance == "against":
        against.append(participant)
      else:
        continue
        
  def add_debater(
    self,
    user: User
  ) -> None:
    self.debaters.append(user)
    
  @property
  def winner(
    self
  ) -> User:
    if self.debaters[0].votes > self.debaters[1].votes:
      return self.debaters[0]
    elif self.debaters[0].votes == self.debaters[1].votes:
      if self.debaters[0].points > self.debaters[1].points:
        return self.debaters[1]
      elif self.debaters[0].points == self.debaters[1].points:
        return random.choice(self.debaters)
      else:
        return self.debaters[0]
    else:
      return self.debaters[1]
      
      
  @property
  def loser(
    self
  ) -> User:
    return self.debaters.remove(self.winner)
  
  def end(
    self,
    winner: User,
    loser: User
  ) -> typing.Tuple[User, User]:
    db["users"][str(winner.member.id)], winner.final_points = calculation.calculate_points(
      winner.points,
      loser.points
    )[0]
    
    db["users"][str(loser.member.id)], loser.final_points = calculation.calculate_points(
      winner.points,
      loser.points
    )[0]
    
    return (winner, loser)
    
