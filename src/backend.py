import json
from typing import Tuple,Dict
import datetime

class Args():
    def __init__(self,cmds:tuple,flags:tuple)->None:
        self.cmds  = cmds
        self.flags = flags

    def parse(self,args:list)->Tuple[list,dict]:
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
    def __init__(self,path:str, temps:str)->None:
        self.loader      = Loader(path)
        self.temp_loader = Loader(temps)
        self.weekdays    = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
        self.lookup      = {self.weekdays[i]: str(i) for i in range(7)}

    def Wday_from_date (self,date:Tuple[int,int,int]) -> str:
        y,m,d = date
        return self.lookup[str(datetime.date(y,m,d).weekday())]
    
    def lookup_by_Wday(self,Wday:str)->dict:
        return self.Stundenplan[Wday]

    def today(self)->str:
        return self.lookup[str(datetime.date.today().weekday())]

    def get_time(self)->str:
        return datetime.datetime.now().strftime("%H:%M")
    
    def get_temps(self)->dict:
        return self.temp_loader.get_plan()

    def set_temps(self,temps:dict)->None:
        self.temp_loader.set_plan(temps)

    def update_tems(self,temp:dict)->dict:
        for el in temp["verschiebungen"]:
            if not el["active"]:
                temp["verschiebungen"].remove(el)
                temp["inactive"].append(el)

        for el in temp["inactive"]:
            if el["active"]:
                temp["inactive"].remove(el)
                temp["verschiebungen"].append(el)

        return temp
    
    def insert_temps(self,plan:dict)->dict:
        temp: dict = self.temp_loader.get_plan()
        temp = self.update_tems(temp)
        for el in temp["verschiebungen"]:
            o = el["old"]
            n = el["new"]
            nd = plan[n[0]][n[1]] if n[1] in plan[n[0]] else None
            od = plan[o[0]][o[1]] if o[1] in plan[o[0]] else None
            plan[n[0]][n[1]] = od
            plan[o[0]][o[1]] = nd
            #  del plan[o[0]][o[2]]
            plan[n[0]] = self.sort(plan[n[0]])

        self.temp_loader.set_plan(temp)
        return plan

    def format_week_string(self,d:str)->str:
        l={i.lower(): i for i in self.weekdays}
        return l[d.lower()] if d.lower() in l else self.today()
    
    def is_in_lecon(self,cur:str,targer_start:str,targer_end:str)->bool:
        c = int(cur.replace(":", ""))
        s = int(targer_start.replace(":", ""))
        e = int(targer_end.replace(":", ""))
        return c >= s and c <= e

    @property
    def Stundenplan(self)->dict:
        return self.insert_temps(self.loader.get_plan())

    def sort(self,day:dict)->dict:
        lookup: dict = {int(k.replace( ":","")):{k:day[k]} for k in day.keys()}
        sort  : list = [int(k.replace(":","")) for k in day.keys()]
        sort.sort()
        new ={list(lookup[k].keys())[0] : lookup[k][list(lookup[k].keys())[0]] for k in sort}
        return new

def main()->None:
    h       = Handler("Stunden.json","Temps.json")
    r       = h.Stundenplan
    r["Mo"] = h.sort(r["Mo"])
    h.loader.set_plan(r)
    print(h.is_in_lecon("8:45","8:00","8:45"))

if __name__=='__main__':
    main()
