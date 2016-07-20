import math
import numpy
from PIL import Image
from skimage import io, color, util

print "Hello World"

im = Image.open("cover.png")
print(im.format, im.size, im.mode)			