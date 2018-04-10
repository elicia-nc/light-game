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
        self.led.setMasterBrightness(70)

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
        self.led.set(self.player_position, colors.Violet)
        self.led.update()

        wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

        # a thread for the enemy to live in
        # enemy_thread = Thread(target=basic_enemy, args=(1,))

        while True:

            buttons = wii.state['buttons']

            #get the initial XYZ values as offset
            defaultX = wii.state['acc'][cwiid.X]
            defaultY = wii.state['acc'][cwiid.Y]
            defaultZ = wii.state['acc'][cwiid.Z]

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
                self.animation.run(sleep=0.1, max_steps=200)      

            if (buttons & cwiid.BTN_B):
                self.clear_all()         

            if (buttons & cwiid.BTN_HOME):
                print 'Home Button pressed'
                time.sleep(button_delay)           

            if (buttons & cwiid.BTN_MINUS):
                print 'Minus Button pressed'
                time.sleep(button_delay)   

            if (buttons & cwiid.BTN_PLUS):
                print 'Plus Button pressed'
                time.sleep(button_delay)

            if (wii.state['acc'][cwiid.Z] - defaultZ) > 4:
                self.move_up()

            if (defaultZ - wii.state['acc'][cwiid.Z]) > 4:
                self.move_down()


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
            self.animation.run(sleep=0.1, max_steps=200)   

    def clear_all(self):
        self.led.fill(colors.Black)
        self.led.update()  
        self.player_position = 2
        self.led.set(self.player_position, colors.Violet)
        self.led.update()










