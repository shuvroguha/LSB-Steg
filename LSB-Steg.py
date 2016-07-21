import math
import numpy
import sys
from PIL import Image
from skimage import io, color, util

print("Begin")

# convert to 8 bit color
# TODO: take inputs
cover = Image.open("cover2.png").convert("RGB")
hidden = Image.open("dollar.png").convert("RGB")


# TODO: for ease right now
cover = cover.resize((100,100))
#cover.show()

# split into 3 color bands
cover_r, cover_g, cover_b = cover.split()
hidden_r, hidden_g, hidden_b = hidden.split()

# check that cover image is big enough
if ((cover.width * cover.height) < (8 * (hidden.width * hidden.height))):
	sys.exit("Cover image not large enough")

# convert images to pixel values
cover_r_pix = list(cover_r.getdata())
cover_g_pix = list(cover_g.getdata())
cover_b_pix = list(cover_b.getdata())
hidden_r_pix = list(hidden_r.getdata())
hidden_g_pix = list(hidden_g.getdata())
hidden_b_pix = list(hidden_b.getdata())

# bitmasks with 1 in position 0-7
bitmasks = [1, 2, 4, 8, 16, 32, 64, 128]

i = 0
for pixel in hidden_r_pix:
	for mask in bitmasks:
		if( (pixel & mask) == mask):
			cover_r_pix[i] = cover_r_pix[i] | 1
		else:
			cover_r_pix[i] = cover_r_pix[i] & ~(1)
		i = i + 1

i = 0
for pixel in hidden_g_pix:
	for mask in bitmasks:
		if( (pixel & mask) == mask):
			cover_g_pix[i] = cover_g_pix[i] | 1
		else:
			cover_g_pix[i] = cover_g_pix[i] & ~(1)
		i = i + 1

i = 0
for pixel in hidden_b_pix:
	for mask in bitmasks:
		if( (pixel & mask) == mask):
			cover_b_pix[i] = cover_b_pix[i] | 1
		else:
			cover_b_pix[i] = cover_b_pix[i] & ~(1)
		i = i + 1


combined = zip(cover_r_pix, cover_g_pix, cover_b_pix)
final = Image.new(cover.mode, cover.size)
final.putdata(combined)
#final.show()

''' Decode '''

# TODO take inputs
image = final

# split input into color bands
cover_r, cover_g, cover_b = image.split()

# get pixel values from color bands
cover_r_pix = cover_r.getdata()
cover_g_pix = cover_g.getdata()
cover_b_pix = cover_b.getdata()

hidden_r_pix = []
hidden_g_pix = []
hidden_b_pix = []

i = 0
hidden_pix = 0
for pixel in cover_r_pix:
	if(i > 7):
		hidden_r_pix.append(hidden_pix)
		hidden_pix = 0
		i = 0
	if( (pixel & 1) == 1):
		hidden_pix = hidden_pix | (1 << i)
	i = i + 1

i = 0
hidden_pix = 0
for pixel in cover_g_pix:
	if(i > 7):
		hidden_g_pix.append(hidden_pix)
		hidden_pix = 0
		i = 0
	if( (pixel & 1) == 1):
		hidden_pix = hidden_pix | (1 << i)
	i = i + 1

i = 0
hidden_pix = 0
for pixel in cover_b_pix:
	if(i > 7):
		hidden_b_pix.append(hidden_pix)
		hidden_pix = 0
		i = 0
	if( (pixel & 1) == 1):
		hidden_pix = hidden_pix | (1 << i)
	i = i + 1

combined = zip(hidden_r_pix, hidden_g_pix, hidden_b_pix)
final_hidden = Image.new("RGB", (32, 100))
final_hidden.putdata(combined)
final_hidden.show()
		
print("End")
