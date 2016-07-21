import math
import numpy
import sys
from PIL import Image
from skimage import io, color, util

# hides the data from pixels_to_hide in the LSBs of cover_pixels
def encode(pixels_to_hide, cover_pixels):
	# bitmasks with 1 in position 0-7
	bitmasks = [1, 2, 4, 8, 16, 32, 64, 128]

	i = 0
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

def decode(cover_pixels):
	hidden_pixels = []
	i = 0
	px = 0

	for pixel in cover_pixels:
		if(i > 7):
			hidden_pixels.append(px)
			px = 0
			i = 0
		if( (pixel & 1) == 1):
			px = px | (1 << i)
		i = i + 1

	return hidden_pixels

print("Begin")

# convert to 8 bit color
# TODO: take inputs
cover = Image.open("cover2.png").convert("RGB")
message = Image.open("dollar.png").convert("RGB")

# TODO: for ease right now
cover = cover.resize((100,100))
#cover.show()

# split into 3 color bands
cover_r, cover_g, cover_b = cover.split()
message_r, message_g, message_b = message.split()

# check that cover image is big enough
if ((cover.width * cover.height) < (8 * (message.width * message.height))):
	sys.exit("Cover image not large enough")

# convert images to pixel values
cover_r_pix = list(cover_r.getdata())
cover_g_pix = list(cover_g.getdata())
cover_b_pix = list(cover_b.getdata())
message_r_pix = list(message_r.getdata())
message_g_pix = list(message_g.getdata())
message_b_pix = list(message_b.getdata())

# encode message in cover
encode(message_r_pix, cover_r_pix)
encode(message_g_pix, cover_g_pix)
encode(message_b_pix, cover_b_pix)

# combine rbg into image
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

# decode cover image bands
hidden_r_pix = decode(cover_r_pix)
hidden_g_pix = decode(cover_g_pix)
hidden_b_pix = decode(cover_b_pix)

# combine rgb into the hidden message
combined = zip(hidden_r_pix, hidden_g_pix, hidden_b_pix)
final_hidden = Image.new("RGB", (32, 100))
final_hidden.putdata(combined)
final_hidden.show()
		
print("End")
