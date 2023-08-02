# Digitam Multimeter Driver for VXI instrument. Basically write for DMM6500/7510 Series. and 3446X Serise
import vxi11
from enum import Enum

class function(Enum):
    DCV = 0
    ACV = 1
    Ohm2W = 2
    Ohm4W = 3
    DCI = 4
    ACI = 5
    FREQ = 6
    PERIOD = 7
    DIODE = 8
    DCRAT = 9
    TEMP = 10
    CAP = 11

class function_cmd_class():
    def __init__(self,setting_str:str):
        self.func_code = int(setting_str.split("=")[0])
        commande_list = setting_str.split("=")[1].split(",")
        self.func_name = commande_list[0]
        self.func_cmd = commande_list[1]
        self.func_enable = commande_list[2]
        if(self.func_code != 8):
            self.getRange = commande_list[3]
            self.getAutoRange = commande_list[4]
            self.getAutoZero = commande_list[5]
            self.getNPLC = commande_list[6]
            self.getDigits = commande_list[7]
            self.getInputImp = commande_list[8]
            self.setNull = commande_list[9]
            self.RangeList = []
            for cmd in commande_list[10:]:
                if cmd.isdigit() == True:
                    self.RangeList.append(cmd)

class cmd_class():
    def __init__(self,setting_str:str):
        self.cmd_name = setting_str.split("=")[0]
        self.cmd_value = setting_str.split("=")[1]

class DMM:

    def __init__(self,addr,model):
        self.addr=addr
        self.model=model
        self.ini_file_path = ".\\model\\"+model+".ini"
        self.func_list:function_cmd_class = []
        self.cmd_list:cmd_class = []
        self.loadCommand()
        self.instr=vxi11.Instrument(self.addr)
        self.instr.write("SYST:BEEP")
        self.mode=function.DCV
        print(self.instr.ask("*IDN?"))
    def loadCommand(self):
        with open(self.ini_file_path,"r") as f:
            lines = f.readlines()
            f.close()
            for line in lines:
                if(line.startswith(";")==False and line.startswith("[")==False and line.isspace()==False):
                    cmd = line.replace("\r","").replace("\n","")
                    prefix = cmd.split("=")[0]
                    if(prefix.isdigit()==True):
                        self.func_list.append(function_cmd_class(cmd))
                    else:
                        self.cmd_list.append(cmd_class(cmd))
    def set_DCV(self):
        for function in self.func_list:
            if(function.func_name == "DCV" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_ACV(self):
        for function in self.func_list:
            if(function.func_name == "ACV" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_Ohm2W(self):
        for function in self.func_list:
            if(function.func_name == "Ω 2W" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return
    def set_Ohm4W(self):
        for function in self.func_list:
            if(function.func_name == "Ω 4W" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return
            
    def set_DCI(self):
        for function in self.func_list:
            if(function.func_name == "DCI" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_ACI(self):
        for function in self.func_list:
            if(function.func_name == "ACI" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_FREQ(self):
        for function in self.func_list:
            if(function.func_name == "FREQ" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_PERIOD(self):
        for function in self.func_list:
            if(function.func_name == "PERIOD" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_DCRAT(self):
        for function in self.func_list:
            if(function.func_name == "DC:RAT" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_TEMP(self):
        for function in self.func_list:
            if(function.func_name == "TEMP" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_CAP(self):
        for function in self.func_list:
            if(function.func_name == "CAP" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return

    def set_DIODE(self):
        for function in self.func_list:
            if(function.func_name == "DIODE" and function.func_enable == "1"):
                self.instr.write(function.func_cmd)
                return
    def read(self):
        for cmd in self.cmd_list:
            if(cmd.cmd_name.lower()=="read"):
                value = self.instr.ask(cmd.cmd_value)
        return float(value)
    def returnFunc(self,param_name:str):
        for cmd in self.cmd_list:
            if(cmd.cmd_name.lower()==param_name.lower()):
                return cmd.cmd_value
    def set_NPLC(self,mode:function,nplc:str):
        for function in self.func_list:
            if(function.func_name==mode.name):
                self.instr.write(function.)

if __name__=="__main__":
    my_dmm=DMM("192.168.31.237","34465A")
    my_dmm.set_DCV()
    print(my_dmm.read())