from colormath.color_objects import XYZColor, sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from PIL import Image
import urllib2 as urllib
import cStringIO
import sys

"""
Map image dominant color to palette and return 
"""
class imageMean:
	def __init__(self):
		self.img = None
		self.thumbSize = 400  
		self.map = {
			'redId': self.convertToLAB((255,0,0)),
			'greenId': self.convertToLAB((0, 255, 0)),
			'blueId': self.convertToLAB((0, 0, 255)),
			'yellowId': self.convertToLAB((255, 255, 0)),
			'black': self.convertToLAB((0, 0, 0)),

		}
		self.background = self.convertToLAB((255,255,255))


	def loadImage(self, src):
		fd = urllib.urlopen(src)
		image = cStringIO.StringIO(fd.read())

		img = Image.open(image)
		img = img.resize((self.thumbSize, self.thumbSize))
		img = img.quantize(3)
		img = img.convert('RGB')

		self.img = img

	def convertToLAB(self, color):
		r,g,b = tuple([c / 255.0 for c in color])
		rgb = sRGBColor(r,g,b)
		return convert_color(rgb, LabColor, target_illuminant='d50')

	def distance(self, a, b):
		return delta_e_cie2000(a, b)
		
	def mean(self):
		colors = self.img.getcolors()
		colors.sort()
		colors.reverse()
		print colors

		#skip background
		for color in colors:
			primary = self.convertToLAB(color[1])
			distance = self.distance(primary, self.background)
			if distance > 100:
				break

		#calculate min distance
		mindistance = 10
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


