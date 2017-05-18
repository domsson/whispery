class PushButton:

    FALLING = -1
    RISING  =  1
    NONE    =  0

    def __init__(self, gpio, pin, bnc, callback, name=None):
        self.gpio = gpio
        self.pin = pin
        self.bnc = bnc
        self.callback = callback
        self.name = name

        # Enable the internal pull-up resistors on version 2 boards
        self.gpio.setup(self.pin, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)

        # Add event detection to the GPIO inputs
        self.gpio.add_event_detect(self.pin, self.gpio.BOTH, callback=self.button_event, bouncetime=self.bnc)

    # Call back routine called by switch events
    def button_event(self, pin):
        event = self.NONE
        if self.gpio.input(pin):
            event = self.RISING
        else:
            event = self.FALLING
        self.callback(self.pin, event)
