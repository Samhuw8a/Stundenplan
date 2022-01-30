import json
from PyInquirer import prompt,style_from_dict

class Editor():
    def __init__ (self)->None:
        self.weekdays=("Mo","Di","Mi","Do","Fr","Sa","So")
        self.del_qs=[
            {
                'type'    : 'list',
                'name'    : 'tag',
                'message' : 'Welcher Wochentag willst du wählen',
                'choices' : ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So' ],
                }, {
                'type'    : 'input',
                'name'    : 'start',
                'message' : 'Startzeit deiner Lektion',
                'validate': self.is_valid_time
            }]
        self.create_qs=[
            {
                'type'    : 'list',
                'name'    : 'tag',
                'message' : 'Welcher Wochentag willst du wählen',
                'choices' : ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So' ],
            }, {
                'type'    : 'input',
                'name'    : 'zimmer',
                'message' : 'Zimmer'
            }, {
                'type'    : 'input',
                'name'    : 'fach',
                'message' : 'Fach'
            }, {
                'type'    : 'input',
                'name'    : 'lek',
                'message' : 'Anzahl Lektionen',
                'validate': lambda x: str(x).isdigit()
            }, {
                'type'    : 'input',
                'name'    : 'start',
                'message' : 'Start der Lektion',
                'validate': self.is_valid_time
            }, {
                'type'    : 'input',
                'name'    : 'ende',
                'message' : 'Ende der Lektion',
                'validate': self.is_valid_time
            },
        ]

    def delete_lecons(self,plan:dict)->dict:
        ans   = prompt(self.del_qs)
        day   = ans['tag']
        start = ans['start']
        del plan[day][start]
        return plan

    def is_valid_time(self, time:str)->bool:
        try:
            int(time.split(":")[0])
            int(time.split(":")[1])
            return True
        except:
            pass

        return False

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
