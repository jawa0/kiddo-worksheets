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


def generate_subtraction_digits():
	are_different = False
	while not are_different:
		x = random.randint(1, 9)
		y = random.randint(1, 9)
		are_different = (x != y)
	
	return max(x, y), min(x, y)
	
 
if __name__ == '__main__':
	surface = cairo.PDFSurface(OUTPUT_FILE_NAME, 
							   PAGE_WIDTH_IN * PTS_PER_IN,
							   PAGE_HEIGHT_IN * PTS_PER_IN)
	
	cr = cairo.Context(surface)
	
	for d in range(10):
		print(cr.text_extents(str(d)))

	cr.set_font_size(FONT_HEIGHT_IN * PTS_PER_IN)
	for i in range(20):
		col = i // 10
		row = i % 10

		cr.move_to((LEFT_MARGIN_IN + col * 4) * PTS_PER_IN, 
				  (TOP_MARGIN_IN  + row * 1) * PTS_PER_IN)
		
		text = "%d - %d = ___" % generate_subtraction_digits()
		cr.show_text(text)
		bearing_x, bearing_y, width, height, advance_x, advance_y = \
			cr.text_extents(text)
			
		cr.rel_move_to(-advance_x, 0)
	cr.show_page()
		