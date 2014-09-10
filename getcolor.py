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
		self.thumbSize = 400  
		self.map = {
			'redId': (255,0,0),
			'greenId': (0, 255, 0),
			'blueId': (0, 0, 255),
			'yellowId': (255, 255, 0),
			'black': (0, 0, 0),

		}
		self.background = (255,255,255)


	def loadImage(self, src):
		fd = urllib.urlopen(src)
		image = cStringIO.StringIO(fd.read())

		img = Image.open(image)
		img = img.resize((self.thumbSize, self.thumbSize))
		img = img.quantize(3)
		img = img.convert('RGB')

		self.img = img

	def distance(self, a, b):
		return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2
		
	def mean(self):
		colors = self.img.getcolors()
		colors.sort()
		colors.reverse()
		print colors

		#skip background
		for color in colors:
			primary = color[1]
			distance = self.distance(primary, self.background)
			if distance > 100:
				break

		#calculate min distance
		mindistance = (255**2) * 3
		result = 'Error'

		for id, mapcolor in self.map.iteritems():
			distance = self.distance(primary, mapcolor)
			if distance < mindistance:
				mindistance = distance
				result = id
		print mindistance
		return result


if __name__ == '__main__':
	src = sys.argv[1]
	a = imageMean()
	a.loadImage(src)
	print a.mean()


