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
    def Stundenplan(self):
        return self.loader.get_plan()

def main()->None:
    h = Handler()
    r = h.Stundenplan
    print(r)
    h.loader.set_plan(r)

if __name__=='__main__':
    main()
