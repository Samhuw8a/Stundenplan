from rich.console import Console
from rich.theme   import Theme
from rich.panel   import Panel
from rich.table   import Table
from itertools    import zip_longest
from PyInquirer   import prompt, Separator,style_from_dict,Token,style_from_dict,Token

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
        ans = prompt(self.ui_qs,style = self.qstyle)
        d   = ""
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
    
    def temp(self,info:dict)->None:
        v      = info["verschiebungen"]
        i      = info["inactive"]
        vs     = ""
        ina    = ""

        for el in v:
            vs+=f"[fach]{el['old'][0]} -> {el['old'][0]}\n"
            vs+=f"[zeit]{el['old'][1]} -> {el['old'][1]}\n"
            self.cons.print(Panel(vs,title="Verschiebungen",width=30))
            vs = ""
        for el in i:
            ina+=f"[fach]{el['old'][0]} -> {el['old'][0]}\n"
            ina+=f"[zeit]{el['old'][1]} -> {el['old'][1]}\n"
            self.cons.print(Panel(ina,title="Inaktiv",width=30))
            ina = ""

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

    def time_left(self, cur,end)->int:
        h = int(end.split(":")[0]) - int(cur.split(":")[0]) 
        m = int(end.split(":")[1]) - int(cur.split(":")[1]) 
        return h*60+m

    def lecon(self,info:dict,start:str)->None:
        out = ""
        t_left=0
        if info:
            t_left = self.time_left(start,info["Ende"])
            out += f"[fach]{info['Fach']}\n"
            out += f"[zimmer]{info['Zimmer']}\n"
            out += f"[text]{info['Anzahl_Lek']} Lektionen\n"
            out += f"[zeit]{info['Ende']}"
        else:
            out ="[error]Du hast im moment Keine Lektion"

        pan = Panel(out,title=f"[zeit]{t_left}/{start}",width=30,padding=1)
        self.cons.print(pan)

def main()->None:
    u = UI()

if __name__=='__main__':
    main()
