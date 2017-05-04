import argparse
import cairo
import random

OUTPUT_FILE_NAME = 'sheet.pdf'

PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11.0
LEFT_MARGIN_IN = 1.0
RIGHT_MARGIN_IN = LEFT_MARGIN_IN
TOP_MARGIN_IN = 0.75
BOTTOM_MARGIN_IN = TOP_MARGIN_IN
 
PTS_PER_IN = 72.0

FONT_HEIGHT_IN = 0.5


def inches(inches):
    """Return the number of points equal to the given number of inches."""
    return inches * PTS_PER_IN


def generate_subtraction_across_ten():
  """Generate a pair of numbers (a, b) representing the subtraction a - b.
  The generated a will be in [11-19], and b will be [2,10] such that a - b is
  less than 10."""
  
  a = random.randint(11, 19)
  b = random.randint(a-9, 10)
  return (a, b)
  
def generate_single_digit_subtraction(can_be_equal=False):
  """Generate a pair of single digits (a, b) representing the subtraction a - b.
  If can_be_equal is True, then a can be equal to b. Otherwise, not 
  (the default is False). The generated a will always be >= b so that the result
  of the subtraction a-b is non-negative."""
  
  good_pair = False
  while not good_pair:
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    good_pair = can_be_equal or (a != b)
  
  return max(a, b), min(a, b)
  

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--subtract-across-ten", action="store_true")
  args = parser.parse_args()
  
  if args.subtract_across_ten:
    generating_function = generate_subtraction_across_ten
  else:
    generating_function = generate_single_digit_subtraction


  surface = cairo.PDFSurface(OUTPUT_FILE_NAME, inches(PAGE_WIDTH_IN),
                              inches(PAGE_HEIGHT_IN))
  cr = cairo.Context(surface)
  
  pairs = set([])
  while len(pairs) < 20:
    pairs.add(generating_function())
  
  for d in range(10):
    print(cr.text_extents(str(d)))

  cr.set_font_size(FONT_HEIGHT_IN * PTS_PER_IN)
  for i, pair in enumerate(pairs):
    col = i // 10
    row = i % 10

    cr.move_to(inches(LEFT_MARGIN_IN + col * 4), 
                inches(TOP_MARGIN_IN  + row * 1))
    
    if args.subtract_across_ten:
      if pair[1] < 10:
        format_str = "{0:2d} - {1: d} = ___"
      else:
        format_str = "{0:2d} - {1:2d} = ___"
      text = format_str.format(pair[0], pair[1])
    else:
      text = "{0:d} - {1:d} = ___".format(pair[0], pair[1])
      
    cr.show_text(text)
    bearing_x, bearing_y, width, height, advance_x, advance_y = \
      cr.text_extents(text)
      
    cr.rel_move_to(-advance_x, 0)
  cr.show_page()
    