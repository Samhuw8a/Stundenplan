import json
from typing import Tuple,Dict,List
import datetime

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

    def format_week_string(self,d:str)->str:
        l={ "mo":"Mo", "di":"Di", "do":"Mi", "mi":"Do", "fr":"Fr", "sa":"Sa", "so":"So" }
        return l[d.lower()] if d.lower() in l else self.today()
    
    def is_in_lecon(self,cur:str,targer_start:str,targer_end:str)->bool:
        c = int(cur.split(":")[0]          + cur.split(":")[1])
        s = int(targer_start.split(":")[0] + targer_start.split(":")[1])
        e = int(targer_end.split(":")[0]   + targer_end.split(":")[1])
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

def main()->None:
    h       = Handler("src/Stunden.json")
    r       = h.Stundenplan
    r["Mo"] = h.sort(r["Mo"])
    h.loader.set_plan(r)
    print(h.is_in_lecon("8:50","8:00","8:45"))

if __name__=='__main__':
    main()
