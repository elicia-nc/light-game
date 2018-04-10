#!/usr/bin/python
import lights

from bibliopixel.drivers.APA102 import DriverAPA102
from bibliopixel.led import *

from bibliopixel.animation import BaseStripAnim
from bibliopixel.drivers.driver_base import ChannelOrder
import bibliopixel.colors as colors

# stuff for the wiimote
import cwiid
import time

from threading import Thread

# -------------------
# basic light strip
# -------------------

STRIP_METERS = 3
LIGHTS_PER_METER = 144
TOTAL_LIGHTS = STRIP_METERS * LIGHTS_PER_METER

class LightGame(object):

    def __init__(self):
        self.driver = DriverAPA102(TOTAL_LIGHTS, c_order=ChannelOrder.BGR, SPISpeed=2)
        self.led = LEDStrip(self.driver)
        self.led.setMasterBrightness(100)

        self.animation = lights.WinAnimation(self.led)
        self.player_position = 5
        self.enemy_position = TOTAL_LIGHTS
        self.led.set(self.player_position, colors.Blue)
        self.led.update()


    # def basic_enemy()
    # 	for i in TOTAL_LIGHTS:
    # 		pass
    		
    def run_game(self):
        # ---------------------------------------
        # this is all for setting up the wiimote
        # ---------------------------------------
        button_delay = 0.1

        print 'Press 1 + 2 on your Wii Remote now ...'
        time.sleep(1)

        # Connect to the Wii Remote. If it times out
        # then quit.
        try:
            wii=cwiid.Wiimote()
        except RuntimeError:
            print "Error opening wiimote connection"
            quit()

        print 'Wii Remote connected...\n'
        print 'Press some buttons!\n'
        print 'Press PLUS and MINUS together to disconnect and quit.\n'

        wii.rpt_mode = cwiid.RPT_BTN

        # a thread for the enemy to live in
        # enemy_thread = Thread(target=basic_enemy, args=(1,))

        while True:

            buttons = wii.state['buttons']

            # If Plus and Minus buttons pressed
            # together then rumble and quit.
            if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
                print '\nClosing connection ...'
                wii.rumble = 1
                time.sleep(1)
                wii.rumble = 0
                exit(wii)  

            # the enemy is always coming toward the player


            # Check if other buttons are pressed by
            # doing a bitwise AND of the buttons number
            # and the predefined constant for that button.
            if (buttons & cwiid.BTN_LEFT):
                print 'Left pressed'
                time.sleep(button_delay)         

            if(buttons & cwiid.BTN_RIGHT):
                print 'Right pressed'
                time.sleep(button_delay)          

            if (buttons & cwiid.BTN_UP):
                self.move_up()      

            if (buttons & cwiid.BTN_DOWN):
                self.move_down() 

            if (buttons & cwiid.BTN_1):
                print 'Button 1 pressed'
                time.sleep(button_delay)          

            if (buttons & cwiid.BTN_2):
                print 'Button 2 pressed'
                time.sleep(button_delay)          

            if (buttons & cwiid.BTN_A):
                print 'Button A pressed'
                # sleep slows it down enough to see what's happening
                animation.run(sleep=0.001, max_steps=TOTAL_LIGHTS)
                time.sleep(button_delay)          

            if (buttons & cwiid.BTN_B):
                print 'Button B pressed'
                led.fill(colors.Black)
                led.update()
                time.sleep(button_delay)          

            if (buttons & cwiid.BTN_HOME):
                print 'Home Button pressed'
                time.sleep(button_delay)           

            if (buttons & cwiid.BTN_MINUS):
                print 'Minus Button pressed'
                time.sleep(button_delay)   

            if (buttons & cwiid.BTN_PLUS):
                print 'Plus Button pressed'
                time.sleep(button_delay)


    def move_down(self):
        self.led.set(self.player_position, colors.Black)
        self.led.update()
        if self.player_position - 1 > 0:
            self.player_position -= 1
            self.led.set(self.player_position, colors.Green)
            self.led.update()
        else:
            self.led.set(self.player_position, colors.Red)
            self.led.update() 

    def move_up(self):
        self.led.set(self.player_position, colors.Black)
        self.led.update()
        if self.player_position + 1 < TOTAL_LIGHTS:
            self.player_position += 1
            self.led.set(self.player_position, colors.Green)
            self.led.update()
        else:
            self.animation.run(sleep=0.001, max_steps=TOTAL_LIGHTS)        








