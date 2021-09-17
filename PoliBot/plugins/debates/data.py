import typing
import random
import discord
from replit import db

from plugins.debate import calculation


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

    
def is_sorted(
  values: typing.List[Proposition]
) -> bool:
  for i in range(0, len(values)):
    if i == len(values):
      break
    
    if values[i].votes > values[i+1].votes:
      continue
      
    else:
      return False
    
  return True

def sort(
  values: typing.List[Proposition]
) -> typing.List[Proposition]:
  previous_value = 0
  n = 0
  while True:
    for i in range(0, len(values)):
      if previous_value == 0:
        previous_value = values[i]
        n = i
        continue
      else:
        if values[i].votes > previous_value.votes:
          values[i], values[n] = values[n], values[i]
          n = i
          continue
        else:
          continue
    
    if is_sorted(values):
      break
    else:
      continue
  
  return values

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

class DebateRoom:
  def __init__(
    self,
    users: typing.List[discord.Member]=[],
  ) -> None:
    self.users = users
    self.props = []
    
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
     
  @property
  def proposition(
    self
  ) -> Proposition:
    return sort(self.props)[0]
    
  def add_proposition(
    self,
    prop: Proposition
  ) -> None:
    self.props.append(prop)
    
  def add_participant(
    self,
    user: User
  ) -> None:
    self.participants.append(user)
    
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
    
