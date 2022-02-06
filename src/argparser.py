class Invalid_arg(Exception):
    def __init__(self,argument)->None:
        super().__init__(self)
        self.argument=argument

    def __str__(self)->str:
        return f"Invalid argument: argument {self.argument} not found"

class Flag():
    def __init__(self,flag_str:str,options:str)->None:
        self.flag_str = flag_str
        self.options = options

    def __str__(self)->str:
        return "-"*((len(self.flag_str)>1)+1)+self.flag_str

class Args():
    def __init__(self,cmds:tuple,usage:str)->None:
        self.cmds  = cmds
        self.usage = usage
        self.flags = []
        self.help:tuple  = ()

    def flag_add(self,flag:str,options:int)->None:
        self.flags.append(Flag(flag,options))

    def parse(self,args:list)->tuple:
        cmds:list  = []
        flags:list = {}
        i=0
        while i <len(args):
            arg = args[i]
            if arg in self.help:
                print(self.usage)

            elif arg in self.cmds:
                cmds.append(arg)

            elif arg in [str(i) for i in self.flags]:
                for flag in self.flags:
                    if str(flag)== arg:
                        if len(args)-flag.options-i <1:
                            raise Invalid_arg(str(flag))

                        sub = args[i+1:i+flag.options+1]
                        i+=flag.options
                        flags[arg.replace("-","")] = sub
            else:
                raise Invalid_arg(arg)

            i+=1

        return cmds,flags
