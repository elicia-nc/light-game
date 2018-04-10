#!/usr/bin/python
from bibliopixel.drivers.APA102 import DriverAPA102
from bibliopixel.led import *

from bibliopixel.animation import BaseStripAnim
from bibliopixel.drivers.driver_base import ChannelOrder
import bibliopixel.colors as colors

import time

STRIP_METERS = 3
LIGHTS_PER_METER = 144
TOTAL_LIGHTS = STRIP_METERS * LIGHTS_PER_METER

driver = DriverAPA102(TOTAL_LIGHTS, c_order=ChannelOrder.GRB, SPISpeed=2)
led = LEDStrip(driver)
rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo, colors.Violet]

led.setMasterBrightness(100)
		
for color in rainbow:
  led.fill(color)
  led.update()      
  time.sleep(5)
