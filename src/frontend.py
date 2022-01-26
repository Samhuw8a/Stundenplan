class UI():
    def __init__(self)->None:
        print("Init UI")

    def day(self,lektionen:dict)->None:
        print(lektionen)
    
    def week(self,info:dict)->None:
        print(info)

    def lecon(self,info:dict)->None:
        print(info)

def main()->None:
    u = UI()

if __name__=='__main__':
    main()
