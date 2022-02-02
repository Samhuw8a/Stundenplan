#! /usr/bin/python3
import sys
import json
from typing import Tuple,Dict,List
import datetime
from rich.console import Console
from rich.theme   import Theme
from rich.panel   import Panel
from rich.table   import Table
from itertools    import zip_longest
from PyInquirer   import prompt, Separator,style_from_dict,Token,style_from_dict,Token

PATH = "Stunden.json"
class Editor():
    def __init__ (self)->None:
        self.weekdays=("Mo","Di","Mi","Do","Fr","Sa","So")
        self.del_qs=[
            {
                'type'    : 'list',
                'name'    : 'tag',
                'message' : 'Welcher Wochentag willst du wählen',
                'choices' : ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So' ],
                }, {
                'type'    : 'input',
                'name'    : 'start',
                'message' : 'Startzeit deiner Lektion',
                'validate': self.is_valid_time
            }]
        self.create_qs=[
            {
                'type'    : 'list',
                'name'    : 'tag',
                'message' : 'Welcher Wochentag willst du wählen',
                'choices' : ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So' ],
            }, {
                'type'    : 'input',
                'name'    : 'zimmer',
                'message' : 'Zimmer'
            }, {
                'type'    : 'input',
                'name'    : 'fach',
                'message' : 'Fach',
                'validate': lambda x: x.isalpha()
            }, {
                'type'    : 'input',
                'name'    : 'lek',
                'message' : 'Anzahl Lektionen',
                'validate': lambda x: str(x).isdigit()
            }, {
                'type'    : 'input',
                'name'    : 'start',
                'message' : 'Start der Lektion',
                'validate': self.is_valid_time
            }, {
                'type'    : 'input',
                'name'    : 'ende',
                'message' : 'Ende der Lektion',
                'validate': self.is_valid_time
            },
        ]

    def delete_lecons(self,plan:dict)->dict:
        ans   = prompt(self.del_qs)
        day   = ans['tag']
        start = ans['start']
        del plan[day][start]
        return plan

    def is_valid_time(self, time:str)->bool:
        try:
            int(time.split(":")[0])
            int(time.split(":")[1])
            return True
        except:
            pass

        return False

    def create_lecon(self)->tuple:
        ans        = prompt(self.create_qs)
        day        = ans['tag']
        zimmer     = ans['zimmer']
        fach       = ans['fach']
        anzahl_lek = ans['lek']
        start      = ans['start']
        ende       = ans['ende']
        return day,start,{
            "Zimmer"     : zimmer,
            "Fach"       : fach,
            "Anzahl_Lek" : anzahl_lek,
            "Ende"       : ende
        }

class UI():
    def __init__(self)->None:
        self.style= {
            "zeit"     : "#fadc84 bold underline",
            "fach"     : "#84b2fa italic",
            "zimmer"   : "#d984fa ",
            "text"     : "#7dd198 ",
            "boldtext" : "#7dd198 bold ",
            "error"    : "red bold ",
            "usage"    : "#fadc84 bold"
        }
        self.styling = Theme(self.style)
        self.cons    = Console(theme= self.styling)

        self.qstyle  = style_from_dict({
            Token.Separator    : 'bg: #cc5454',
            Token.QuestionMark : '#673ab7',
            Token.Selected     : '#cc4454',  # default
            Token.Pointer      : '#673ab7 bold',
            Token.Instruction  : '',  # default
            Token.Answer       : '#f44336 bold',
            Token.Question     : 'underline bold',
            Token.Separator    : '#fadc84'
        })
        self.ui_qs=[ {
            'type'    : 'list',
            'name'    : 'cmd',
            'message' : 'Was willst du machen',
            'choices' : [ 'list', 'day', 'now', Separator("==>edit<=="), 'add', 'del' ]
        } ]
        self.day_qs=[
            {
                'type'    : 'list' ,
                'name'    : 'day',
                'message' : 'welcher Tag willst du',
                'choices' : [ "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
            }
        ]

    def tui(self)->tuple:
        ans = prompt(self.ui_qs,style=self.qstyle)
        d = ""
        cmd = ans["cmd"]
        if cmd== "day":
            d = prompt(self.day_qs,style=self.qstyle)["day"]
        print(cmd,d)
        return cmd,d

    def usage(self, usage_str:str)->None:
        self.cons.print(usage_str)

    def day(self,lektionen:dict,day:str)->None:
        self.cons.print(" "*8 +day,style="boldtext")
        for t,lek in lektionen.items():
            self.lecon(lek,t)

    def deconst_week(self,info:dict)->dict:
        o:dict = {}
        for day,leks in info.items():
            w = []
            for t,lek in leks.items():
                w.append((t,lek["Fach"]))
            o[day]= w
        return o

    def week(self,info:dict)->None:
        week = Table(title="[text][bold]Deine Woche: ")
        d_week = self.deconst_week(info)
        for day in d_week:
            week.add_column(day,justify="center",style="#fadc84  bold underline")

        for MO,DI,MI,DO,FR,SA,SO in zip_longest(*d_week.values()):
            week.add_row(
                 f"[fach]{MO[0] if MO != None else '[red]KA'} {MO[1] if MO != None else ''}",
                 f"[fach]{DI[0] if DI != None else '[red]KA'} {DI[1] if DI != None else ''}",
                 f"[fach]{MI[0] if MI != None else '[red]KA'} {MI[1] if MI != None else ''}",
                 f"[fach]{DO[0] if DO != None else '[red]KA'} {DO[1] if DO != None else ''}",
                 f"[fach]{FR[0] if FR != None else '[red]KA'} {FR[1] if FR != None else ''}",
                 f"[fach]{SA[0] if SA != None else '[red]KA'} {SA[1] if SA != None else ''}",
                 f"[fach]{SO[0] if SO != None else '[red]KA'} {SO[1] if SO != None else ''}"
            )
        self.cons.print(week)

    def lecon(self,info:dict,start:str)->None:
        out = ""
        if info:
            out += f"[fach]{info['Fach']}\n"
            out += f"[zimmer]{info['Zimmer']}\n"
            out += f"[text]{info['Anzahl_Lek']} Lektionen\n"
            out += f"[zeit]{info['Ende']}"
        else:
            out ="[error]Du hast im moment Keine Lektion"

        pan = Panel(out,title=f"[zeit]{start}",width=30,padding=1)
        self.cons.print(pan)

class Args():
    def __init__(self,cmds:tuple,flags:tuple)->None:
        self.cmds  = cmds
        self.flags = flags

    def parse(self,args:List[str])->Tuple[list,dict]:
        cmds:list  = []
        flags:dict = {}
        i=0
        while i <len(args):
            arg = args[i]
            if arg in self.cmds:
                cmds.append(arg)
            elif arg in self.flags:
                if i==len(args)-1:
                    sub = ""
                else:
                    sub = args[i+1]
                flags[arg.split("-")[-1]] = sub
            i+=1

        return cmds,flags

class Loader():
    def __init__(self,path:str)->None:
        self.path = path

    def get_plan(self)->Dict[str,dict]:
        with open(self.path,"r") as f:
            return json.load(f)

    def set_plan(self,plan:Dict[str,dict])->None:
        with open(self.path,"w") as f:
            json.dump(plan,f,indent=4)

class Handler():
    def __init__(self,path:str)->None:
        self.loader = Loader(path)
        self.lookup = { "0":"Mo", "1":"Di", "2":"Mi", "3":"Do", "4":"Fr", "5":"Sa", "6":"So" }

    def Wday_from_date (self,date:Tuple[int,int,int]) -> str:
        y,m,d = date
        return self.lookup[str(datetime.date(y,m,d).weekday())]
    
    def lookup_by_Wday(self,Wday:str)->dict:
        return self.Stundenplan[Wday]

    def today(self)->str:
        return self.lookup[str(datetime.date.today().weekday())]

    def get_time(self)->str:
        return datetime.datetime.now().strftime("%H:%M")

    def format_week_string(self,d:str)->str:
        l={ "mo":"Mo", "di":"Di", "do":"Mi", "mi":"Do", "fr":"Fr", "sa":"Sa", "so":"So" }
        return l[d.lower()] if d.lower() in l else self.today()
    
    def is_in_lecon(self,cur:str,targer_start:str,targer_end:str)->bool:
        c =          int(cur.split(":")[0]          + cur.split(":")[1])
        s = int(targer_start.split(":")[0] + targer_start.split(":")[1])
        e =   int(targer_end.split(":")[0]   + targer_end.split(":")[1])
        return c >= s and c <= e

    @property
    def Stundenplan(self)->dict:
        return self.loader.get_plan()

    def sort(self,day:dict)->dict:
        lookup: dict = {}
        new   : dict = {}
        sort  : list = []

        for k in day.keys():
            t         = int(k.replace(":",""))
            lookup[t] = {k: day[k]}
            sort.append(t)
        sort.sort()

        for k in sort:
            time      = list(lookup[k].keys())[0]
            new[time] = lookup[k][time]
        return new

class Main():
    def __init__(self,backend,frontend,editor)->None:
        cmds:tuple     = ("list", "day", "now", "add", "del")
        flags:tuple    = ("-h", "--help", "-d")
        self.handler   = backend
        self.editor    = editor
        self.ui        = frontend
        self.args      = Args(cmds,flags)
        self.weekdays  = ("Mo","Di","Mi","Do","Fr","Sa","So")
        self.usage_str = """[red]Usage:
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
                elif cmd == "day":
                    self.cmd_day( "" if "d" not in f else f["d"])
                elif cmd == "now":
                    self.cmd_now()
                elif cmd == "add":
                    self.cmd_add()
                elif cmd == "del":
                    self.cmd_del()
        exit()

    def cmd_ui(self)->None:
        cmd,d = self.ui.tui()
        if cmd   == "list":
            self.cmd_list()
        elif cmd == "day":
            self.cmd_day(d)
        elif cmd == "now":
            self.cmd_now()
        elif cmd == "add":
            self.cmd_add()
        elif cmd == "del":
            self.cmd_del()

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
    handler = Handler(PATH)
    frontend = UI()
    editor = Editor()
    sp=Main(handler,frontend,editor)
    sp.run()

if __name__=='__main__':
    main()
