#Python For Firefly Port

fireflyP is designed for using devices port on firefly or other similar platforms.It can support RK3399 now. 
Like GPIO .

**NOTE**: fireflyP is still in development. if you find something wrong, please let me know, and if you fix bugs, it is nice to give me 'Pull requests'


##Install
fetch source code:

    $ git clone https://github.com/zhansb/pyFireflyP.git
    $ cd pyFireflyP

install python modules(python can be python2 or python3):

    $ sudo python setup.py install


##Usage
GPIO and PWM control regs directly by devmem in fireflyP, and independent of kernel space.

The devmem source is modifed from [pydevmem](https://github.com/kylemanna/pydevmem) (Thanks to Kyle).

You need root privilege to execute it!

###Gpio
####Interface:
    init()
        Init GPIO function
        implement it before using Gpio
    get_level(self)
        Returns the level of the pin for input direction
        or return setting of the DR register for output gpios.
    
    set_dir(self, dir)
        set GPIO direction
        :dir: refer to GpioDir
    
    set_drv(self, drv)
        set GPIO drv
        :drv: refer to GpioDrv
    
    set_level(self, level)
        set GPIO output signal
        :level: refer to GpioLevel
    
    set_mux(self, mux)
        set GPIO mux
        :mux: refer to GpioMux
    
    set_pull(self, pull)
        set GPIO pull
        :pull: refer to GpioPull
	en_clk(self)
	    enable GPIO CLK
		GPIO0-1 0x0104
		GPIO2-4 0x037c
####Example for turn on/off the yellow led on firefly-rk3288:
    $sudo python
    >>> from fireflyP import Gpio
    >>> Gpio.init()
    >>> LED_YELLOW="GPIO8A2"
    >>> led_yellow=Gpio(LED_YELLOW)
    >>> led_yellow.set_dir(Gpio.OUTPUT) #set_dir have contained set_mux(GpioMux.MUX_GPIO)
    >>> led_yellow.set_level(Gpio.LOW)  #turn on the yellow led
    >>> led_yellow.set_level(Gpio.HIGH) #turn off the yellow led

or you can refer to demo/gpio_test.py 
