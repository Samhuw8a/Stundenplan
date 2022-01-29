from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from itertools import zip_longest

class UI():
    def __init__(self)->None:
        self.style= {
            "zeit"   : "#fadc84  bold underline",
            "fach"   : "#84b2fa  italic",
            "zimmer" : "#d984fa  ",
            "text"   : "#7dd198  ",
            "error"  : "red bold "
        }
        self.styling = Theme(self.style)
        self.cons = Console(theme=self.styling)

    def day(self,lektionen:dict)->None:
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
                 f"[fach]{MO[0] if MO != None else ''} {MO[1] if MO != None else ''}",
                 f"[fach]{DI[0] if DI != None else ''} {DI[1] if DI != None else ''}",
                 f"[fach]{MI[0] if MI != None else ''} {MI[1] if MI != None else ''}",
                 f"[fach]{DO[0] if DO != None else ''} {DO[1] if DO != None else ''}",
                 f"[fach]{FR[0] if FR != None else ''} {FR[1] if FR != None else ''}",
                 f"[fach]{SA[0] if SA != None else ''} {SA[1] if SA != None else ''}",
                 f"[fach]{SO[0] if SO != None else ''} {SO[1] if SO != None else ''}"
            )
        self.cons.print(week)

    def lecon(self,info:dict,start:str)->None:
        if info:
            self.cons.print("-"*20)
            self.cons.print (f"| [zeit]{start} {info['Ende']}")
            self.cons.print (f"| [fach]\t{info['Fach']}")
            self.cons.print (f"| [zimmer]\t{info['Zimmer']}")
            self.cons.print (f"| [text]\t{info['Anzahl_Lek']} Lektionen")
        else:
            self.cons.print("[error]Du hast im moment Keine Lektion")

def main()->None:
    u = UI()

if __name__=='__main__'
    main()
