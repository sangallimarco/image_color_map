from PIL import Image
import urllib2 as urllib
import cStringIO
import colorsys
from math import floor
import sys

"""
Map image dominant color to palette and return 
"""
class imageMean:
	def __init__(self):
		self.img = None
		self.thumbSize = 200  
		self.map = {
			'redId': colorsys.rgb_to_hls(255,0,0),
			'greenId': colorsys.rgb_to_hls(0, 255, 0),
			'blueId': colorsys.rgb_to_hls(0, 0, 255),
			'yellowId': colorsys.rgb_to_hls(255, 255, 0),

		}

	def loadImage(self, src):
		fd = urllib.urlopen(src)
		image = cStringIO.StringIO(fd.read())

		img = Image.open(image)
		img = img.resize((self.thumbSize, self.thumbSize))
		img = img.quantize(6)
		img = img.convert('RGB')

		self.img = img

	def mean(self):
		colors = self.img.getcolors()
		print colors

		#skip background
		for color in colors:
			r, g, b = [ x/255.0 for x in color[1] ]
			colorhls = colorsys.rgb_to_hls(r, g ,b)
			if  colorhls[2] < 0.9 and colorhls[2] > 0.1:
				break

		#calculate min distance
		minDiff = 100
		result = 'Error'

		for k,v in self.map.iteritems():
			diff = int(abs(v[0] - colorhls[0]) * 100)
			if diff < minDiff:
				minDiff =diff
				result = k
			
		return result


if __name__ == '__main__':
	src = sys.argv[1]
	a = imageMean()
	a.loadImage(src)
	print a.mean()


