#! /usr/bin/python3
from src.backend import Handler,Args
from src.frontend import UI
from src.editor import Editor
import sys

PATH = "src/Stunden.json"
TEMP = "src/Temps.json"

class Main():
    def __init__(self,backend,frontend,editor)->None:
        self.cmds:tuple = ("list", "day", "now", "add", "del", "temp")
        flags:tuple     = ("-h", "--help", "-d")
        self.handler    = backend
        self.editor     = editor
        self.ui         = frontend
        self.ui.cmds    = self.cmds
        self.args       = Args(self.cmds,flags)
        self.weekdays   = ("Mo","Di","Mi","Do","Fr","Sa","So")
        self.usage_str  = """[red]Usage:
        [blue]main [list,day,now,add,del] [-d, -h, --help]

        [usage]list:
            [text]List all items in your Plan
        [usage]day [-d]:
            [text]list all lecons in the currrent day.
            [text]if -d is set it will list all items at that day


        [usage]now:
            [text]Show your current lecon
        [usage]add:
            [text]Add an entry
        [usage]del:
            [text]Delete an entry
        """

    def run(self)->None:
        s,f = self.args.parse(sys.argv)
        if 'h' in f or 'help' in f:
            self.ui.usage(self.usage_str)
        elif not s:
            self.cmd_ui()
        else:
            for cmd in s:
                if   cmd == "list":
                    self.cmd_list()
                elif cmd == "temp":
                    self.cmd_temp()
                elif cmd == "day":
                    self.cmd_day( "" if "d" not in f else f["d"])
                elif cmd == "now":
                    self.cmd_now()
                elif cmd == "add":
                    self.cmd_add()
                elif cmd == "del":
                    self.cmd_del()
        exit()

    def cmd_temp(self)->None:
        temps  = self.handler.get_temps()
        cmd = self.ui.temp(temps)
        if cmd == "add":
            versch = self.editor.add_temp()
            temps["verschiebungen"].append(versch)
        elif cmd == "rem":
            temps = self.editor.del_temp(temps)
        self.handler.set_temps(temps)


    def cmd_ui(self)->None:
        cmd,d = self.ui.tui()
        if cmd   == "list":
            self.cmd_list()
        elif cmd == "day":
            self.cmd_day(d)
            print(d)
        elif cmd == "now":
            self.cmd_now()
        elif cmd == "add":
            self.cmd_add()
        elif cmd == "del":
            self.cmd_del()
        elif cmd == "temp":
            self.cmd_temp()

    def cmd_del(self)->None:
        p = self.handler.Stundenplan
        while True:
            self.cmd_list()
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
    handler = Handler(PATH,TEMP)
    frontend = UI()
    editor = Editor()
    sp=Main(handler,frontend,editor)
    sp.run()

if __name__=='__main__':
    main()
