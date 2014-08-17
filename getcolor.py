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
			'redId': self._toHLS((255,0,0)),
			'greenId': self._toHLS((0, 255, 0)),
			'blueId': self._toHLS((0, 0, 255)),
			'yellowId': self._toHLS((255, 255, 0)),

		}

	def _toHLS(self, color):
		r, g, b = [ x/255.0 for x in color ]
		return colorsys.rgb_to_hls(r, g ,b)

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
			colorhls = self._toHLS(color[1])
			if  colorhls[2] < 0.9 and colorhls[2] > 0.1:
				break

		#calculate min distance
		minDiff = 100
		result = 'Error'

		for k,v in self.map.iteritems():
			diff = abs( v[0] - colorhls[0] )
			if diff < minDiff:
				minDiff =diff
				result = k
			
		return result


if __name__ == '__main__':
	src = sys.argv[1]
	a = imageMean()
	a.loadImage(src)
	print a.mean()


