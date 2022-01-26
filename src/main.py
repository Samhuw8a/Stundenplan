from backend import Handler
from frontend import UI

class Main():

    def __init__(self,backend_handler,frontend_handler)->None:
        self.handler = backend_handler
        self.ui = frontend_handler
        print("Hello World")

def main()->None:
    handler = Handler()
    frontend = Handler()
    sp=Main(handler,frontend)
