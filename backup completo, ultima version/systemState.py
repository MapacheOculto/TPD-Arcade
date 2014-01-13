
class systemState:

    def __init__(self):
        self.stateDictionary = {}
        self.currentState = None

    def update(self, elapsedTime):
        if self.currentState == None:
            return
        self.currentState.update(elapsedTime)
    
    def render(self):
        if self.currentState == None:
            return
        self.currentState.render()

    def append(self, gameObject, key):
        self.stateDictionary.update({key:gameObject})

    def changeState(self, key):
        self.currentState = self.stateDictionary[key]

    def exists(self, key):
        pass


class gameObject:

    def update(self, elapsedTime):
        pass

    def render(self):
        pass
