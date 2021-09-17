from replit import db

class MissingArgumentError(Exception):
  def __init__(self, argument: str, function: str):
    self.message=f"{function} is missing required argument {argument}."
  
  def __str__(self):
    return self.message

class InvalidFileError(Exception):
  def __init__(self, file_type: str=None):
    if file_type == None:
      raise MissingArgumentError('filepath', 'InvalidFileError')
    
    self.message=f"File of type {file_type} is not an accepted file format."
  
  def __str__(self):
    return self.message


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

def get_prefix(bot, message):
  if 'prefixes' not in db:
    db['prefixes'] = {}
  elif not message.guild:
    return "!"
  if str(message.guild.id) not in db['prefixes']:
    return "!"
  else:
    return db['prefixes'][str(message.guild.id)]
