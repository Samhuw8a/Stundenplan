#! /usr/bin/python3
from src.backend import Handler
from src.frontend import UI
from src.editor import Editor
from src.argparser import Args
from src import usage
import sys

PATH = "src/Stunden.json"
TEMP = "src/Temps.json"

class Main():
    def __init__(self,backend,frontend,editor)->None:
        self.handler    = backend
        self.editor     = editor
        self.ui         = frontend
        self.weekdays   = ("Mo","Di","Mi","Do","Fr","Sa","So")

    def eval(self,cmd,flags)->None:
        s,f = cmd,flags
        if not s:
            cmd,d = self.ui.tui()
        else :
            cmd = s[0]
            d = "" if "d"not in f else f["d"]
        self.run(cmd,d)

    def run(self,cmd,d)->None:
        if   cmd == "list":
            self.cmd_list()
        elif cmd == "temp":
            self.cmd_temp()
        elif cmd == "day":
            self.cmd_day(d)
        elif cmd == "now":
            self.cmd_now()
        elif cmd == "add":
            self.cmd_add()
        elif cmd == "del":
            self.cmd_del()
        elif cmd == "ed":
            self.cmd_ed()

    def cmd_temp(self)->None:
        temps = self.handler.get_temps()
        temps = self.handler.update_tems(temps)
        cmd   = self.ui.temp(temps)
        if cmd == "add":
            versch = self.editor.add_temp()
            temps["verschiebungen"].append(versch)
        elif cmd == "rem":
            temps = self.editor.del_temp(temps)
        elif cmd == "reactivate":
            temps = self.editor.reac_temp(temps)
        elif cmd == "clear":
            temps["inactive"] = []

        self.handler.set_temps(temps)

    def cmd_ed(self)->None:
        p = self.handler.Stundenplan
        while True:
            p = self.editor.edit_lecons(p)
            if input("Nochmal Y/n").lower() == "n": break
        self.handler.loader.set_plan(p)

    def cmd_del(self)->None:
        p = self.handler.Stundenplan
        while True:
            p = self.editor.delete_lecons(p)
            if input("Nochmal Y/n").lower() == "n": break
        self.handler.loader.set_plan(p)

    def cmd_add(self)->None:
        p= self.handler.Stundenplan
        while True:
            day,time,lek = self.editor.create_lecon()
            p[day][time] = lek
            if input("Nochmal Y/n").lower() == "n": break
        self.handler.loader.set_plan(p)
    
    def cmd_list (self)->None:
        self.ui.week(self.handler.Stundenplan)

    def cmd_day (self,d:str="")->None:
        d    = self.handler.format_week_string(d)
        info = self.handler.lookup_by_Wday(d)
        self.ui.day(info,d)

    def cmd_now (self)->None:
        wday         = self.handler.today()
        info         = self.handler.lookup_by_Wday(wday)
        current_time = self.handler.get_time()
        z            = current_time
        for t in info:
            e = info[t]["Ende"]
            if self.handler.is_in_lecon(current_time,t,e):
                z = t
        info = info[z] if z in info else {}
        self.ui.lecon(info,current_time)
        
def main()->None:
    cmds       = ("list", "day", "now", "add", "del", "ed", "temp")
    flags      = ("-d",)

    handler    = Handler(PATH,TEMP)
    frontend   = UI()
    editor     = Editor()
    main       = Main(handler,frontend,editor)
    args       = Args(cmds,flags,usage)
    args.help  = ("help","-h","--help")


    cmds,flags = args.parse(sys.argv[1:])
    main.eval(cmds,flags)
    
if __name__=='__main__':
    main()
