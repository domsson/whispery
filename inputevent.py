class InputEvent():

    NONE            = 0
    BUTTON_PRESSED  = 1
    BUTTON_RELEASED = 2
    ROTATION_CW     = 3
    ROTATION_CCW    = 4

    def __init__(self, event_type=InputEvent.NONE, input_name=None, input_pin1=None, input_pin2=None):
        self.event_type = event_type
        self.input_name = input_name
        self.input_pin1 = input_pin1
        self.input_pin2 = input_pin2
        
