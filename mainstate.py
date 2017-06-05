class PlayerState():

    def __init__(self, gpio, player, display):
        self.gpio = gpio
        self.player = player
        self.display = display
        self.next = None
        self.on_enter()

    def go_to(self.state):
        self.next = state

    def on_enter(self):
        raise NotImplementedError((self.__class__.__name__) + ".on_enter()")

    def on_exit(self);
        raise NotImplementedError((self.__class__.__name__) + ".on_exit()")

    def update(self):
        raise NotImplementedError((self.__class__.__name__) + ".update()")

    def cleanup(self):
        self.on_exit()
