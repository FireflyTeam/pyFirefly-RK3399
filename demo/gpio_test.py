#!/usr/bin/env python

from fireflyP import Gpio

import time
import pdb


LED_BLUE="GPIO2D3"
LED_YELLOW="GPIO0B5"

PWM1="GPIO7A1"
GPIO7A1_IOMUX_GPIO=0
GPIO7A1_IOMUX_PWM1=1


if __name__ ==  '__main__':
    Gpio.init()
      
    g1b1=Gpio('GPIO1A7')
    g2  =Gpio('GPIO4D5')
    g2.en_clk()              #gpio2-4的时钟需要使能才能写数据
    g1b1.set_dir(Gpio.OUTPUT)
    g2  .set_dir(Gpio.INPUT)
    while(True):
    	g1b1.set_level(Gpio.HIGH)
    	a=g1b1.get_level()
        c = g2.get_level()
    	print("gpiolow is %r"%a)
        print("c is %r"% c)
    	time.sleep(1)

    	g1b1.set_level(Gpio.LOW)
		b=g1b1.get_level()
        c = g2.get_level()
		print("gpiohigh is %r "%b)
        print("c is %r"%c)
    	time.sleep(1)
    '''
    gpio_blue_led=Gpio(LED_BLUE)
    gpio_yellow_led=Gpio(LED_YELLOW)
    gpio_blue_led.set_dir(Gpio.OUTPUT)
    gpio_yellow_led.set_dir(Gpio.OUTPUT)
    while(True):
        gpio_blue_led.set_level(Gpio.HIGH)
        gpio_yellow_led.set_level(Gpio.LOW)
        time.sleep(0.5)
        gpio_blue_led.set_level(Gpio.LOW)
        gpio_yellow_led.set_level(Gpio.HIGH)
        time.sleep(0.5)
    '''
