from backend import Handler
from frontend import UI
from typing import Tuple,List
import sys

class Args():
    def __init__(self,subs:tuple,flags:tuple)->None:
        self.subs  = subs
        self.flags = flags

    def parse(self,args:List[str])->Tuple[list,list]:
        subs:list = []
        flags:list = []
        for arg in args:
            if arg in self.flags:
                flags.append(arg)

            elif arg in self.subs:
                subs.append(arg.split("-")[-1])
        return subs,flags

class Main():
    def __init__(self,backend,frontend)->None:
        subs  = ("list", )
        flags = ("-h"  , )
        self.handler = backend
        self.ui      = frontend
        self.args    = Args(subs,flags)

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
