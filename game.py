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

# -------------------
# basic light strip
# -------------------

STRIP_METERS = 3
LIGHTS_PER_METER = 144
TOTAL_LIGHTS = STRIP_METERS * LIGHTS_PER_METER

class Player(object):
    def __init__(self, led):
        self.position = 2
        self.color = colors.Violet
        self.led = led
        self.is_attacking = False
        self.last_attack_time = time.time()

    def move_down(self, speed=1):
        self.led.set(self.position, colors.Black)
        self.led.update()
        if self.position - speed > 0:
            self.position -= speed
            self.update()
        else:
            self.color = colors.Red
            self.update()

    def move_up(self, speed=1):
        self.led.set(self.position, colors.Black)
        self.led.update()
        if self.position + speed < TOTAL_LIGHTS:
            self.position += speed
            self.update()

    def update(self):
        self.led.set(self.position, self.color)
        self.led.update()

    def attack(self):
        self.color = colors.Blue
        self.is_attacking = True
        self.last_attack_time = time.time()
        self.update()

    def stop_attack(self):
        self.color = colors.Green
        self.is_attacking = False
        self.update()

    # def can_attack(self):
    #     if not self.is_attacking:
    #         if time.time() - self.last_attack_time > 3:
    #             return True


class Enemy(object):
    def __init__(self, led):
        self.position = TOTAL_LIGHTS
        self.color = colors.Red
        self.led = led

    def move_down(self, speed=1):
        self.led.set(self.position, colors.Black)
        self.led.update()
        if self.position - speed > 0:
            self.position -= speed
            self.color = colors.Red
            self.update()
        else:
            self.color = colors.Red
            self.update()

    def update(self):
        self.led.set(self.position, self.color)
        self.led.update()

    def die(self):
        self.color = colors.Black
        self.update()


class LightGame(object):

    def __init__(self):
        self.driver = DriverAPA102(TOTAL_LIGHTS, c_order=ChannelOrder.BGR, SPISpeed=2)
        self.led = LEDStrip(self.driver)
        self.led.setMasterBrightness(70)

        self.player = Player(self.led)
        self.enemy = Enemy(self.led)
        self.animation = lights.WinAnimation(self.led)
        
        self.player.position = 5
        self.enemy.position = TOTAL_LIGHTS - 2
        self.led.set(self.player.position, colors.Blue)
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
        

        wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        wii.state
        defaultY = wii.state['acc'][cwiid.Y]
        defaultX = wii.state['acc'][cwiid.X]

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

            # if the enemy hasn't died yet
            if self.enemy:
                # check for collision
                if self.player.position in range(self.enemy.position-1, self.enemy.position+2):
                    if self.player.is_attacking == True:
                        self.enemy.die()
                        self.enemy = None
                    else:
                        anim = lights.Death(self.led)
                        anim.run(sleep=2, max_steps=200)
                        self.clear_all()
            if self.enemy:
                self.enemy.move_down()

            if self.player.position == TOTAL_LIGHTS - 1:
                self.animation.run(sleep=0.5, max_steps=200)
                self.player.position = 2
                self.clear_all()


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
                self.player.move_up()      

            if (buttons & cwiid.BTN_DOWN):
                self.player.move_down() 

            if (buttons & cwiid.BTN_1):
                print 'Button 1 pressed'
                time.sleep(button_delay)          

            if (buttons & cwiid.BTN_2):
                print 'Button 2 pressed'
                time.sleep(button_delay)          

            if (buttons & cwiid.BTN_A):
                self.animation.run(sleep=0.5, max_steps=200)      

            if (buttons & cwiid.BTN_B):
                defaultY = wii.state['acc'][cwiid.Y]
                defaultX = wii.state['acc'][cwiid.X]
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

            if (wii.state['acc'][cwiid.Y] - defaultY) > 5:
                self.player.move_up()

            if (defaultY - wii.state['acc'][cwiid.Y]) > 5:
                self.player.move_down()

            # if (wii.state['acc'][cwiid.Y] - defaultY) > 10:
            #     self.player.move_up(2)

            # if (defaultY - wii.state['acc'][cwiid.Y]) > 10:
            #     self.player.move_down(2)

            # if (wii.state['acc'][cwiid.Y] - defaultY) > 15:
            #     self.player.move_up(4)

            # if (defaultY - wii.state['acc'][cwiid.Y]) > 15:
            #     self.player.move_down(4)

            if (wii.state['acc'][cwiid.X] - defaultX) > 10 or (defaultX - wii.state['acc'][cwiid.X]) > 10:
                self.player.attack()
            else:
                self.player.stop_attack()


    def clear_all(self):
        self.led.fill(colors.Black)
        self.led.update()  
        self.player.position = 2
        if self.enemy:
            self.enemy.position = TOTAL_LIGHTS - 2
        else:
            self.enemy = Enemy(self.led)
        self.player.update()












