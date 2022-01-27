class UI():
    def __init__(self)->None:
        print("Init UI")

    def day(self,lektionen:dict)->None:
        for t,lek in lektionen.items():
            print("-"*25)
            print("|"+t+":")
            print(f"|\t{lek['Fach']}")
            print(f"|\t{lek['Zimmer']}")
            print(f"|\t{lek['Anzahl_Lek']} Lektionen")
            print("-"*25)
    
    def week(self,info:dict)->None:
        print(info)

    def lecon(self,info:dict,current_time:str,start:str)->None:
        if info:
            print("-"*25)
            print(f"|{start} | {info['Ende']}:")
            print(f"|\t{info['Fach']}")
            print(f"|\t{info['Zimmer']}")
            print(f"|\t{info['Anzahl_Lek']} Lektionen")
            print("-"*25)
        else:
            print("Du hast im moment Keine Lektion")

def main()->None:
    u = UI()

if __name__=='__main__':
    main()
