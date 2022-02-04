import json
from PyInquirer import prompt
from src.questions import delete_lec,create_lec,edit_input,add_temps,delete_temps,Zimmer,Fach,Anzahl_Lek,Ende,Start

class Editor():
    def __init__ (self)->None:
        self.weekdays=("Mo","Di","Mi","Do","Fr","Sa","So")
        self.del_qs = delete_lec
        self.create_qs=create_lec
        self.edit_qs=edit_input
        self.temp_add=add_temps
        self.temp_del=delete_temps

    def reac_temp(self, info:dict)->dict:
        ans = prompt(self.temp_del)
        t = ans["tag"]
        s = ans["start"]
        versch = info["inactive"]
        for el in info["inactive"]:
            if el["new"][0] == t and el["new"][1] == s: 
                info["inactive"][versch.index(el)]["active"] = True
        return info

    def add_temp(self)->dict:
        ans = prompt(self.temp_add)
        t   = ans["tag"]
        nt  = ans["n_tag"]
        s   = ans["start"]
        ns  = ans["n_start"]
        return {
            "old":[t,s],
            "new":[nt,ns],
            "active":True
        }

    def del_temp(self,info:dict)->dict:
        ans    = prompt(self.temp_del)
        t      = ans["tag"]
        s      = ans["start"]
        versch = info["verschiebungen"]
        for el in versch:
            if el["new"][0] == t and el["new"][1] == s: 
                info["verschiebungen"][versch.index(el)]["active"] = False
        return info

    def edit_lecons(self,plan:dict)->dict:
        ans = prompt(self.edit_qs)
        t   = ans["tag"]
        s   = ans["start"]
        cmd = ans["cmd"]
        if cmd == "Zimmer":
            zimmer = prompt(Zimmer)["cmd"]
            plan[t][s]["Zimmer"]=zimmer

        elif cmd == "Fach":
            fach = prompt(Fach)["cmd"]
            plan[t][s]["Fach"]=fach

        elif cmd == "Anzahl_Lek":
            anz = prompt(Anzahl_Lek)["cmd"]
            plan[t][s]["Anzahl_Lek"]=anz

        elif cmd == "Ende":
            ende = prompt(Ende)["cmd"]
            plan[t][s]["Ende"]=ende

        elif cmd == "Start":
            start = prompt(Start)["cmd"]
            plan[t][s]["Start"]=start
        return plan

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

def main()->None:
    e = Editor()
    e.create_lecon()

if __name__=='__main__':
    main()
