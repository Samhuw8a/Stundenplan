class Invalid_arg(Exception):
    def __init__(self,argument)->None:
        super().__init__(self)
        self.argument=argument

    def __str__(self)->str:
        return f"Invalid argument: argument {self.argument} not found"

class Args():
    def __init__(self,cmds:tuple,flags:tuple,usage:str)->None:
        self.cmds  = cmds
        self.flags = flags
        self.usage = usage
        self.help:tuple  = ()

    def parse(self,args:list)->tuple:
        cmds:list  = []
        flags:dict = {}
        i=0
        while i <len(args):
            arg = args[i]
            if arg in self.help:
                print(self.usage)
            elif arg in self.cmds:
                cmds.append(arg)
            elif arg in self.flags:
                sub = "" if i==len(args)-1 else args[i+1]
                i+=1
                flags[arg.split("-")[-1]] = sub

            else:
                raise Invalid_arg(arg)
            i+=1

        return cmds,flags
