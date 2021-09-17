import typing

def calculate_points(
  i: int,
  j: int
) -> typing.Tuple(int, int):
  p = i+j
  _ = 200-18.5/p
  score_factor = 5-int(i + j / _)
  return (i + int(18.5*score_factor), j - int(18.5*score_factor))
