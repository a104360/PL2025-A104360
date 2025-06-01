class LoopCounter:
    def __init__(self):
        self.while_counter = 0
        self.for_counter = 0
        self.if_counter = 0

    def get_while(self):
        return self.while_counter

    def get_for(self):
        return self.for_counter

    def get_if(self):
        return self.if_counter

    def inc_while(self):
        self.while_counter += 1

    def inc_for(self):
        self.for_counter += 1

    def inc_if(self):
        self.if_counter += 1


counter = LoopCounter()