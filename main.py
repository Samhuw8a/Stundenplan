#! /usr/bin/python3
from src.backend import Handler,Args
from src.frontend import UI
from src.editor import Editor
import sys

class Main():
    def __init__(self,backend,frontend,editor)->None:
        cmds:tuple          = ("list", "day", "now", "add", "del")
        flags:tuple         = ("-h", "--help", "-d")
        self.weekdays:tuple = ("Mo","Di","Mi","Do","Fr","Sa","So")
        self.handler        = backend
        self.editor         = editor
        self.ui             = frontend
        self.args           = Args(cmds,flags)

    def run(self)->None:
        s,f = self.args.parse(sys.argv[1:])
        for cmd in s:
            if   cmd == "list":
                self.cmd_list()
            elif cmd == "day":
                self.cmd_day( "" if "d" not in f else f["d"])
            elif cmd == "now":
                self.cmd_now()
            elif cmd == "add":
                self.cmd_add()
            elif cmd == "del":
                self.cmd_del()
            exit()

    def cmd_del(self)->None:
        p= self.handler.Stundenplan
        while True:
            self.cmd_list()
            p = self.editor.delete_lecons(p)
            if input("Nochmal Y/n").lower() == "n": break
        self.handler.loader.set_plan(p)

    def cmd_add(self)->None:
        p= self.handler.Stundenplan
        while True:
            day,time,lek = self.editor.create_lecon()
            p[day][time]=lek
            if input("Nochmal Y/n").lower() == "n": break
        self.handler.loader.set_plan(p)
    
    def cmd_list (self)->None:
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
