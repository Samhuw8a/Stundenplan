from rich.console  import Console
from rich.theme    import Theme
from rich.panel    import Panel
from rich.table    import Table
from itertools     import zip_longest
from PyInquirer    import prompt,style_from_dict,Token
from src.questions import UI_qs,Temp_qs,Day_qs
import math
import rich

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
        self.ui_qs=UI_qs
        self.temp_qs=Temp_qs
        self.day_qs=Day_qs

    def tui(self)->tuple:
        """Das Terminal User interface"""
        ans = prompt(self.ui_qs,style = self.qstyle)
        d   = ""
        cmd = ans["cmd"]
        if cmd == "day":
            d = prompt(self.day_qs,style=self.qstyle)["day"]
        return cmd,d

    def usage(self, usage_str:str)->None:
        self.cons.print(usage_str)

    def day(self,lektionen:dict,day:str)->None:
        """gib alle fächer an einem Tag aus"""
        self.cons.print(" "*8 + day,style="boldtext")
        tab = Table.grid()
        tab.add_column()
        row = []

        for t,lek in lektionen.items():
            pan = self.create_lec(lek,t)
            row.append(pan)

        tab.add_row(*row)
        self.cons.print(tab)

    def deconst_week(self,info:dict)->dict:
        """Alle Fächer an eine Tag in liste form"""
        return {day:[
            (t,lek["Fach"]) for t,lek in leks.items() if lek != None]
        for day,leks in info.items()}
    
    def temp(self,info:dict)->str:
        """listet alle verschiebungen auf"""
        cmd = prompt(self.temp_qs)["cmd"]
        if cmd == "list":
            for group in info.values():
                for el in group:
                    vs=f"[fach]{el['old'][0]} -> {el['new'][0]}\
                            \n[zeit]{el['old'][1]} -> {el['new'][1]}"
                    self.cons.print(Panel(vs,
                                          title="Verschiebungen"if el["active"] else "Inaktiv",
                                          width=30))

        return cmd if cmd != "list" else ""

    def week(self,info:dict)->None:
        """gibt den vollen Stundenplan aus"""
        week = Table(title="[text][bold]Deine Woche: ")
        d_week = self.deconst_week(info)
        for day in d_week:
            week.add_column(day,justify="center",style="#fadc84  bold underline")

        for w in zip_longest(*d_week.values()):
            week.add_row(
                *[f"[fach]{d[0] if d != None else '[red]KA'} "+\
                  f"{d[1] if d != None else ''}" \
                  for d in w]
            )
        self.cons.print(week)

    def time_left(self, cur,end)->int:
        """gibt die Zeit bis zum Ende der Lektion aus."""
        h = int(end.split(":")[0]) - int(cur.split(":")[0]) 
        m = int(end.split(":")[1]) - int(cur.split(":")[1]) 
        return h*60+m

    def lecon(self,info:dict,start:str)->None:
        """printed eine Lektion aus"""
        pan = self.create_lec(info,start)
        self.cons.print(pan)

    def create_lec(self,info:dict,start:str)->Panel:
        """gib eine Lektion als rich Panel aus"""
        t_left=0
        if info:
            t_left = self.time_left(start,info["Ende"])
            out = f"[fach]{info['Fach']}\n[zimmer]{info['Zimmer']}\n[text]{info['Anzahl_Lek']} Lektionen\n[zeit]{info['Ende']}"
        else:
            out ="[error]Du hast im moment Keine Lektion"

        pan = Panel(out,title=f"[zeit]{t_left}/{start}",width=30,padding=1)
        return pan

def main()->None:
    u = UI()

if __name__=='__main__':
    main()
