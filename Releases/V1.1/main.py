#! /usr/bin/python3
import sys
import json
from PyInquirer import prompt
from typing import Tuple,Dict,List
import datetime

PATH = "/Users/Samuel/Programieren/Stundenplan/src/Stunden.json"

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
        self.lookup = {
            "0":"Mo",
            "1":"Di",
            "2":"Mi",
            "3":"Do",
            "4":"Fr",
            "5":"Sa",
            "6":"So"
        }

    def Wday_from_date (self,date:Tuple[int,int,int]) -> str:
        y,m,d = date
        return self.lookup[str(datetime.date(y,m,d).weekday())]
    
    def lookup_by_Wday(self,Wday:str)->dict:
        return self.Stundenplan[Wday]

    def today(self)->str:
        return self.lookup[str(datetime.date.today().weekday())]

    def get_time(self)->str:
        return datetime.datetime.now().strftime("%H:%M")
    
    def is_in_lecon(self,cur:str,targer_start:str,targer_end:str)->bool:
        c = int(cur.split(":")[0] + cur.split(":")[1])
        s = int(targer_start.split(":")[0] + targer_start.split(":")[1])
        e = int(targer_end.split(":")[0] + targer_end.split(":")[1])
        return c >=s and c <=e

    @property
    def Stundenplan(self)->dict:
        return self.loader.get_plan()

    def sort(self,day:dict)->dict:
        lookup:dict = {}
        sort  :list = []
        new   :dict = {}

        for k in day.keys():
            t = int(k.replace(":",""))
            lookup[t] = {k: day[k]}
            sort.append(t)

        sort.sort()
        for k in sort:
            time=list(lookup[k].keys())[0]
            new[time]=lookup[k][time]

        return new

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
                'type'     : 'input',
                'name'     : 'start',
                'message'  : 'Startzeit deiner Lektion',
            }]
        self.create_qs=[
            {
                'type'    : 'list',
                'name'    : 'tag',
                'message' : 'Welcher Wochentag willst du wählen',
                'choices' : ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So' ],
            }, {
                'type': 'input',
                'name': 'zimmer',
                'message':'Zimmer'
            }, {
                'type': 'input',
                'name': 'fach',
                'message':'Fach'
            }, {
                'type': 'input',
                'name': 'lek',
                'message':'Anzahl Lektionen'
            }, {
                'type': 'input',
                'name': 'start',
                'message':'Start der Lektion'
            }, {
                'type': 'input',
                'name': 'ende',
                'message':'Ende der Lektion'
            },
        ]
    def delete_lecons(self,plan:dict)->dict:
        ans   = prompt(self.del_qs)
        day   = ans['tag']
        start = ans['start']
        del plan[day][start]
        return plan

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
    def day(self,lektionen:dict)->None:
        for t,lek in lektionen.items():
            print("-"*25)
            print("|"+t+":")
            print(f"|\t{lek['Fach']}")
            print(f"|\t{lek['Zimmer']}")
            print(f"|\t{lek['Anzahl_Lek']} Lektionen")
            print("-"*25)
    
    def week(self,info:dict)->None:
        for day,leks in info.items():
            out = f"{day}: | "
            for t,inf in leks.items():
                out += f"{t}: {inf['Fach']} | "
            print(out)
            print("-"*45)


    def lecon(self,info:dict,current_time:str,start:str)->None:
        if info:
            print("-"*25)
            print(f"|{start} | {info['Ende']}:")
            print(f"|\t{info['Fach']}")
            print(f"|\t{info['Zimmer']}")
            print(f"|\t{info['Anzahl_Lek']} Lektionen")
            print("-"*25)
        else:
            print("Du hast im moment Keine Lektion")

class Main():
    def __init__(self,backend,frontend,editor)->None:
        cmds:tuple    = ("list", "day", "now", "add", "del")
        flags:tuple   = ("-h", "--help", "-d")
        self.handler  = backend
        self.editor   = editor
        self.ui       = frontend
        self.args     = Args(cmds,flags)
        self.weekdays = ("Mo","Di","Mi","Do","Fr","Sa","So")
        self.usage    = """Usage:
        main [list,day,now,add,del] [-d, -h, --help]

        list:
            List all items in your Plan
        day [-d]:
            list all lecons in the currrent day.
            if -d is set it will list all items at that day
        now:
            Show your current lecon
        add:
            Add an entry
        del:
            Delete an entry
        """


    def run(self)->None:
        s,f = self.args.parse(sys.argv[1:])
        if 'h' in f or 'help' in f:
            print(self.usage)
            exit()
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
    handler = Handler(PATH)
    frontend = UI()
    editor = Editor()
    sp=Main(handler,frontend,editor)
    sp.run()

if __name__=='__main__':
    main()
