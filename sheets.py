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


def generate_single_digit_subtraction(can_be_equal=False):
  """Generate a pair of single digits (a, b) representing the subtraction a - b.
  If can_be_equal is True, then a can be equal to b. Otherwise, not 
  (the default is False). The generated a will always be >= b so that the result
  of the subtraction a-b is non-negative."""
  
  good_pair = False
  while not good_pair:
    x = random.randint(1, 9)
    y = random.randint(1, 9)
    good_pair = can_be_equal or (x != y)
  
  return max(x, y), min(x, y)
  

if __name__ == '__main__':
  surface = cairo.PDFSurface(OUTPUT_FILE_NAME, inches(PAGE_WIDTH_IN),
                              inches(PAGE_HEIGHT_IN))
  cr = cairo.Context(surface)
  
  digit_pairs = set([])
  while len(digit_pairs) < 20:
    digit_pairs.add(generate_single_digit_subtraction())
  
  for d in range(10):
    print(cr.text_extents(str(d)))

  cr.set_font_size(FONT_HEIGHT_IN * PTS_PER_IN)
  for i, pair in enumerate(digit_pairs):
    col = i // 10
    row = i % 10

    cr.move_to(inches(LEFT_MARGIN_IN + col * 4), 
                inches(TOP_MARGIN_IN  + row * 1))
    
    text = "%d - %d = ___" % pair
    cr.show_text(text)
    bearing_x, bearing_y, width, height, advance_x, advance_y = \
      cr.text_extents(text)
      
    cr.rel_move_to(-advance_x, 0)
  cr.show_page()
    