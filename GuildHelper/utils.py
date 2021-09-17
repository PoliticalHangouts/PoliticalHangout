from replit import db

class MissingArgumentError(Exception):
  def __init__(self, argument: str, function: str):
    self.message=f"{function} is missing required argument {argument}."
  
  def __str__(self):
    return self.message

class PollInvalidError(Exception):
  def __init__(self, poll_name: str):
    self.message="The poll you requested of {} was not found in the database".format(poll_name)
  def __str__(self):
    return self.message

class PollExistsError(Exception):
  def __init__(self, poll_name: str):
    self.message="The poll you attempted to create {} already exists".format(poll_name)
  def __str__(self):
    return self.message

class InvalidFileError(Exception):
  def __init__(self, file_type: str=None):
    if file_type == None:
      raise MissingArgumentError('filepath', 'InvalidFileError')
    
    self.message=f"File of type {file_type} is not an accepted file format."
  
  def __str__(self):
    return self.message

def get_guild_embed(guild: str):
  if 'guilds' not in db:
    db['guilds'] = {}
  if 'Sphinxes' not in db:
    db['Sphinxes'] = {}

def get_poll(poll_name: str):
  if 'polls' not in db:
    db['polls'] = {}
  if poll_name not in db['polls']:
    raise PollInvalidError(poll_name)
  else:
    return db['polls'][poll_name]

def create_poll(poll_name: str, poll_question: str):
  if 'polls' not in db:
    db['polls'] = {}
  if poll_name in db['polls']:
    raise PollExistsError(poll_name)
  else:
    db['polls'][poll_name] = poll_question

def get_prefix(bot, message):
  if 'prefixes' not in db:
    db['prefixes'] = {}
  
  if str(message.guild.id) not in db['prefixes']:
    return "g!"
  
  else:
    return db['prefixes'][str(message.guild.id)]

def parse_file(filepath: str=None):
  if filepath == None:
    raise MissingArgumentError('filepath', 'parse_file')

  if filepath.endswith('.coglist'):
    with open(filepath) as f:
      file_data = f.read()

    response = file_data.split(', ')
  
  elif filepath.endswith('.secret'):
    with open(filepath) as f:
      response = f.read()

  else:
    raise InvalidFileError(filepath.split('.')[len(filepath.split('.'))-1])
  return response
