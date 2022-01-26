from backend import Handler
from frontend import UI
from typing import Tuple,List
import sys

class Args():
    def __init__(self,cmds:tuple,flags:tuple)->None:
        self.cmds  = cmds
        self.flags = flags

    def parse(self,args:List[str])->Tuple[list,list]:
        cmds:list = []
        flags:list = []
        for arg in args:
            if arg in self.cmds:
                cmds.append(arg)
            elif arg in self.flags:
                flags.append(arg.split("-")[-1])

        return cmds,flags

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
        #  print(self.handler.today())
        self.cmd_day("Mo")
        exit()
    
    def cmd_list (self)->None:
        pass

    def cmd_day  (self,d:str="")->None:
        if d not in self.weekdays:
            d = self.handler.today()
        info = self.handler.lookup_by_Wday(d)
        self.ui.day(info)

    def cmd_now  (self)->None:
        pass

def main()->None:
    handler = Handler()
    frontend = UI()
    sp=Main(handler,frontend)
    sp.run()

if __name__=='__main__':
    main()
