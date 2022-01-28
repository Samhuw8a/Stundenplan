from backend import Handler,Args
from frontend import UI
from editor import Editor
from typing import Tuple,List
import sys

class Main():
    def __init__(self,backend,frontend,editor)->None:
        cmds:tuple    = ("list", "day", "now", "add")
        flags:tuple   = ("-h", "--help", "-d")
        self.handler  = backend
        self.editor   = editor
        self.ui       = frontend
        self.args     = Args(cmds,flags)
        self.weekdays = ("Mo","Di","Mi","Do","Fr","Sa","So")

    def run(self)->None:
        s,f = self.args.parse(sys.argv[1:])
        #  print(self.handler.today())
        #  self.cmd_now()
        #  self.cmd_day("Mo")
        #  self.cmd_add()
        self.cmd_list()
        exit()

    def cmd_add(self)->None:
        p= self.handler.Stundenplan
        while True:
            day,time,lek = self.editor.create_lecon()
            p[day][time]=lek
            if input("Nochmal Y/n").lower() == "n": break
        self.handler.loader.set_plan(p)
    
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
    editor = Editor()
    sp=Main(handler,frontend,editor)
    sp.run()

if __name__=='__main__':
    main()
