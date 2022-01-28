import json

class Editor():

    def __init__ (self)->None:
        self.weekdays=("Mo","Di","Mi","Do","Fr","Sa","So")

    def format_day(self,inp)->str:
        for wday in self.weekdays:
            if inp.lower() == wday.lower():
                return wday
        print("Day not correct defaulting to 'Mo'")
        return "Mo"

    def delete_lecons(self,plan:dict)->dict:
        while True:
            try:
                inp = input("Tag: ")
                if len(inp)!=2:
                    raise ValueError
                day = self.format_day(inp)
                break
            except ValueError:
                print("Bitte gib den Wochentag in der abgekürzten Form ein")
        start = input("Startzeit deiner Lektion: ")
        del plan[day][start]
        return plan

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
    e = Editor()

if __name__=='__main__':
    main()
