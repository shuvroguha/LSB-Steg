import math
import numpy
import sys
import itertools
from PIL import Image
from skimage import io, color, util

# hides the data from pixels_to_hide in the LSBs of cover_pixels
def encode(pixels_to_hide, cover_pixels):
	# bitmasks with 1 in position 0-7
	bitmasks = [1, 2, 4, 8, 16, 32, 64, 128]

	# start at 26th pixel, after metadata
	i = 26
	for pixel in pixels_to_hide:
		# inner loop runs 8 times - once for each bit in the pixel to hide
		for mask in bitmasks:
			# if the pixel's bit is 1, put a 1 at cover pixel's LSB
			if( (pixel & mask) == mask):
				cover_pixels[i] = cover_pixels[i] | 1
			# if the pixel's bit is 0, put a 0 at cover pixel's LSB
			else:
				cover_pixels[i] = cover_pixels[i] & ~(1)
			i = i + 1

# decoded the data in the LSBs of cover_pixels and returns a list of pixels
def decode(cover_pixels, size):
	count = 0
	hidden_pixels = []
	i = 0
	px = 0
	cover_pixels = itertools.islice(cover_pixels, 26, (26 + size))

	# construct one pixel (px) from every 8 pixels in cover image
	# by looking at the LSB of each of the 8 pixels
	for pixel in cover_pixels:
		# add the constructed pixel to hidden_pixels after 8 loops
		if(i > 7):
			hidden_pixels.append(px)
			count += 1
			px = 0
			i = 0
		# if LSB of cover pixel is 1, make the bit in px 1
		# otherwise do nothing, since it's already 0
		if( (pixel & 1) == 1):
			px = px | (1 << i)
		i = i + 1

	return hidden_pixels

print("Begin")

# convert to 8 bit color
# TODO: take inputs
cover = Image.open("cover2.png").convert("RGB")
message = Image.open("dollar.png").convert("RGB")

MESSAGE_HEIGHT = message.height
MESSAGE_WIDTH = message.width


# TODO: for ease right now
cover = cover.resize((100,100))
#cover.show()

# split into 3 color bands
cover_r, cover_g, cover_b = cover.split()
message_r, message_g, message_b = message.split()

# check that cover image is big enough
if ((cover.width * cover.height) < (9 * (message.width * message.height))):
	sys.exit("Cover image not large enough")

''' Encode '''

# convert images to pixel values
cover_r_pix = list(cover_r.getdata())
cover_g_pix = list(cover_g.getdata())
cover_b_pix = list(cover_b.getdata())
message_r_pix = list(message_r.getdata())
message_g_pix = list(message_g.getdata())
message_b_pix = list(message_b.getdata())

# encode metadata
for i in range(0, 12):
	mask = (1 << i)
	if((MESSAGE_HEIGHT & mask) == mask):
		cover_r_pix[i] = cover_r_pix[i] | 1
	else:
		cover_r_pix[i] = cover_r_pix[i] & ~(1)
for i in range(13, 25):
	mask = (1 << (i-13))
	if((MESSAGE_WIDTH & mask) == mask):
		cover_r_pix[i] = cover_r_pix[i] | 1
	else:
		cover_r_pix[i] = cover_r_pix[i] & ~(1)

# encode message in cover
encode(message_r_pix, cover_r_pix)
encode(message_g_pix, cover_g_pix)
encode(message_b_pix, cover_b_pix)

# combine rgb into image
combined = zip(cover_r_pix, cover_g_pix, cover_b_pix)
final = Image.new(cover.mode, cover.size)
final.putdata(combined)
final.show()

''' Decode '''

# TODO take inputs
image = final

# split input into color bands
cover_r, cover_g, cover_b = image.split()

# get pixel values from color bands
cover_r_pix = cover_r.getdata()
cover_g_pix = cover_g.getdata()
cover_b_pix = cover_b.getdata()

# decode metadata
hidden_height = 0
for i in range(0, 12):
	if((cover_r_pix[i] & 1) == 1):
		hidden_height = hidden_height | (1 << i)
hidden_width = 0
for i in range(13, 25):
	mask = (1 << (i-13))
	if((cover_r_pix[i] & 1) == 1):
		hidden_width = hidden_width | (1 << (i-13))
hidden_size = hidden_height * hidden_width * 8

# decode cover image bands
hidden_r_pix = decode(cover_r_pix, hidden_size)
hidden_g_pix = decode(cover_g_pix, hidden_size)
hidden_b_pix = decode(cover_b_pix, hidden_size)

# combine rgb into the hidden message
combined_hidden = zip(hidden_r_pix, hidden_g_pix, hidden_b_pix)
final_hidden = Image.new("RGB", (hidden_width, hidden_height))
final_hidden.putdata(combined_hidden)
final_hidden.show()

print("End")
