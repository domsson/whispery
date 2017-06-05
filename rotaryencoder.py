import math
from inputevent import InputEvent

class RotaryEncoder():

    #CCW  = -1
    #NONE =  0
    #CW   =  1

    # Initialise rotary encoder object
    def __init__(self, gpio, pin_a, pin_b, callback, name=None):
        self.gpio = gpio
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.callback = callback
        self.name = name

        self.rotary_a = 0
        self.rotary_b = 0
        self.last_state = 0
        self.last_delta = 0
        self.steps = 0

        # The following lines enable the internal pull-up resistors
        # on version 2 (latest) boards
        self.gpio.setup(self.pin_a, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(self.pin_b, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)

        # Add event detection to the GPIO inputs
        self.gpio.add_event_detect(self.pin_a, self.gpio.BOTH, callback=self.switch_event)
        self.gpio.add_event_detect(self.pin_b, self.gpio.BOTH, callback=self.switch_event)

    # Call back routine called by switch events
    def switch_event(self, switch):
        self.rotary_a = self.gpio.input(self.pin_a)
        self.rotary_b = self.gpio.input(self.pin_b)

        delta = 0
        state = self.rotary_a ^ self.rotary_b | self.rotary_b << 1
        if state != self.last_state:
            delta = (state - self.last_state) % 4
            if delta == 3:
                delta = -1
            elif delta == 2:
                delta = int(math.copysign(delta, self.last_delta))

            self.last_delta = delta
            self.last_state = state

            self.steps = self.steps + abs(self.last_delta)

            if self.steps >= 4:
                self.steps = 0
                event = InputEvent(event_type=InputEvent.NONE, input_name=self.name, input_pin1=self.pin_a, input_pin2=self.pin_b)
                if self.last_delta = -1:
                    event.event_type = InputEvent.ROTATION_CCW
                elif self.last_delta = 1:
                    event.event_type = InputEvent.ROTATION_CW
                self.callback(event)
