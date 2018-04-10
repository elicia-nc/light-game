# stuff for the light strip
from bibliopixel.animation import BaseStripAnim
from bibliopixel.drivers.driver_base import ChannelOrder
import bibliopixel.colors as colors


class StripTest(BaseStripAnim):
	def __init__(self, led, start=0, end=-1):
		# The base class MUST be initialized by calling super like this
		super(StripTest, self).__init__(led, start, end)
		# Create a color array to use in the animation
		self._colors = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo]

	def step(self, amt=1):
		# Fill the strip, with each sucessive color
		# for every led in the strip
		for i in range(self._led.numLEDs):
			self._led.set(i, self._colors[(self._step + i) % len(self._colors)])
		# Increment the internal step by the given amount
		self._step += amt


"""
A variation of the strip test.
This animation will be played at the end of a level. The light strip will fill up with rainbow colours one
light at a time, then flash rainbows for a bit
"""
class WinAnimation(BaseStripAnim):
	def __init__(self, led, start=0, end=-1):
		print "init win"
		super(WinAnimation, self).__init__(led, start, end)
		# set attributes step might need
		self._colors = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo]

	def step(self, amt=1):
		# the light strip hasn't been filled with colour yet
		if self._step*10 < self._led.numLEDs: 
			# move the colours along by 3 before adding another led to the ones being lit up
			# Fill the strip, with each sucessive color
			for i in range(self._step*10):
				self._led.set(i, self._colors[(self._step + i) % len(self._colors)])
		# the light strip is filled. RAINBOWS
		else:
			for i in range(self._led.numLEDs):
				self._led.set(i, self._colors[(self._step + i) % len(self._colors)])
		self._step += amt








