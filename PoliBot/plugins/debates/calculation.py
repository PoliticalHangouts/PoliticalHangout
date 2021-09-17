import typing

def calculate_points(
  i: int,
  j: int
) -> typing.Tuple(int, int):
  score_factor = int(i + j + 200 / i * 32)
  return (i + score_facor, j - score_factor)
