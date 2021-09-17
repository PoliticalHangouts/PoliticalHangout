import typing

def calculate_points(
  i: int,
  j: int
) -> typing.Tuple(int, int):
  score_factor = 5-int(i + j / 181.5)
  return (i + int(18.5*score_factor), j - int(18.5*score_factor))
