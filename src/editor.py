import json
from backend import Loader

class Editor():

    def __init__ (self,path:str)->None:
        self.loader = Loader(path)
        self.weekdays=("Mo","Di","Mi","Do","Fr","Sa","So")

    def format_day(self,inp)->str:
        for wday in self.weekdays:
            if inp.lower == wday.lower():
                return wday
        return "Mo"

    def create_lecon(self)->tuple:
        while True:
            try:
                inp = input("Tag: ")
                if len(inp)!=2:
                    raise ValueError
                day = self.format_day(inp)
                break
            except ValueError:
                print("Bitte gib den Wochentag in der abgekürzten Form ein")

        zimmer = input("Zimmer: ")
        fach = input("Fach: ")
        anzahl_lek = input("Anzahl_lek: ")
        start = input("Start: ")
        ende = input("Ende: ")
        return day,start,{
            "Zimmer": zimmer,
            "Fach": fach,
            "Anzahl_Lek": anzahl_lek,
            "Ende": ende
        }

def main()->None:
    e = Editor("Stunden.json")

if __name__=='__main__':
    main()
