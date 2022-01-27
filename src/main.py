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
        #  self.cmd_now()
        self.cmd_day("Mo")
        exit()
    
    def cmd_list (self)->None:
        #TODO: Wochenansicht im Frontend
        info = self.handler.Stundenplan
        self.ui.week(info)

    def cmd_day  (self,d:str="")->None:
        if d not in self.weekdays:
            d = self.handler.today()
        info = self.handler.lookup_by_Wday(d)
        self.ui.day(info)

    def cmd_now (self)->None:
        d = self.handler.today()
        info = self.handler.lookup_by_Wday(d)
        #TODO: zeit finden
        c = self.handler.get_time()
        z=c
        for t in info:
            e = info[t]["Ende"]
            if self.handler.is_in_lecon(c,t,e):
                z = t
        #  z="8:00"
        info = info[z] if z in info else {}
        self.ui.lecon(info,c,z)
        
def main()->None:
    handler = Handler()
    frontend = UI()
    sp=Main(handler,frontend)
    sp.run()

if __name__=='__main__':
    main()
