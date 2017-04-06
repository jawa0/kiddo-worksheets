import cairo

OUTPUT_FILE_NAME = 'sheet.pdf'
PAGE_WIDTH_INCHES = 8.5
PAGE_HEIGHT_INCHES = 11.0
 
POINTS_PER_INCH = 72.0
 
 
if __name__ == '__main__':
	surface = cairo.PDFSurface(OUTPUT_FILE_NAME, 
							   PAGE_WIDTH_INCHES * POINTS_PER_INCH,
							   PAGE_HEIGHT_INCHES * POINTS_PER_INCH)
	
	cr = cairo.Context(surface)
	cr.show_page()
		