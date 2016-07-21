import math
import numpy
import sys
from PIL import Image
from skimage import io, color, util

print("Begin")

# convert to 8 bit color
cover = Image.open("cover.png").convert("P")
hidden = Image.open("dollar.png").convert("P")
print cover.palette

# TODO: for ease right now
cover = cover.resize((100,100))
#cover.show()

# check that cover image is big enough
if ((cover.width * cover.height) < (8 * (hidden.width * hidden.height))):
	sys.exit("Cover image not large enough")

cover_b = list(cover.getdata())
hidden_b = list(hidden.getdata())
bitmasks = [1, 2, 4, 8, 16, 32, 64, 128]

i = 0
# get a pixel from hidden image
for pixel in hidden_b:
	# inner loop runs 8 times
	for mask in bitmasks:
		# mask one of the bits
		# if its a 1, change cover pixel's LSB to 1
		# otherwise change cover pixel's LSB to 0
		if ((pixel & mask) == mask):
			temp = cover_b[i]
			cover_b[i] = cover_b[i] | 1
			if (abs(temp - cover_b[i]) > 1):
				print("big diff")
		else:
			temp = cover_b[i]
			cover_b[i] = cover_b[i] >> 1
			cover_b[i] = cover_b[i] << 1
			if (abs(temp - cover_b[i]) > 1):
				print("big diff")
		i = i + 1

finished = Image.new(cover.mode, cover.size)
finished.putdata(cover_b, scale = 1.0, offset = 0.0)
finished.palette = cover.palette
finished.show()
		
print("End")
#im.show()
#r.show()
#g.show()
#a.show()	
#b.show()
