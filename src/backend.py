import json
from typing import Tuple,Dict

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
    def __init__(self)->None:
        self.loader = Loader("Stunden.json")
        print("Init Handler")

    def Wday_from_date (self,date:Tuple[int,int,int]) -> int:
        return 0

    @property
    def Stundenplan(self)->dict:
        return self.loader.get_plan()

    def sort(self,day:dict)->dict:
        lookup:dict={}
        sort:list=[]
        new:dict={}

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
    h = Handler()
    r = h.Stundenplan
    #  r["M"]["7:00"] = {}
    r["M"] = h.sort(r["M"])
    h.loader.set_plan(r)

if __name__=='__main__':
    main()
