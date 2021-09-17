import typing

def calculate_points(
  i: int,
  j: int
) -> typing.Tuple(int, int):
  score_factor = int(i + j + 200-18.5 / i * 18.5)
  return (i + score_facor, j - score_factor)
