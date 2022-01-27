from backend import Handler,Args
from frontend import UI
from typing import Tuple,List
import sys

class Main():
    def __init__(self,backend,frontend)->None:
        cmds:tuple   = ("list", "day", "now")
        flags:tuple  = ("-h", "--help", "-d")
        self.handler = backend
        self.ui      = frontend
        self.args    = Args(cmds,flags)
        self.weekdays=("Mo","Di","Mi","Do","Fr","Sa","So")

    def run(self)->None:
        s,f = self.args.parse(sys.argv[1:])
        print(self.handler.today())
        self.cmd_day()
        exit()
    
    def cmd_list (self)->None:
        info = self.backend.Stundenplan
        self.ui.week(info)

    def cmd_day  (self,d:str="")->None:
        if d not in self.weekdays:
            d = self.handler.today()
        info = self.handler.lookup_by_Wday(d)
        self.ui.day(info)

    def cmd_now  (self)->None:
        d = handler.today()
        info = self.handler.lookup_by_Wday(d)
        #TODO: zeit finden   

def main()->None:
    handler = Handler()
    frontend = UI()
    sp=Main(handler,frontend)
    sp.run()

if __name__=='__main__':
    main()
