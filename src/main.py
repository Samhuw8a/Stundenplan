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

    def run(self)->None:
        print("Running")
        s,f = self.args.parse(sys.argv[1:])
        print(s)
        print(f)
        exit()

def main()->None:
    handler = Handler()
    frontend = UI()
    sp=Main(handler,frontend)
    sp.run()

if __name__=='__main__':
    main()
