# Import time library to see cycle simulation step by step slowly
from time import sleep

# Create basicCycle class to simulate Basic Instruction Cycle taugth in class.
class basicCycle:

    # Declare all proccesor schedule variables
    def __init__(self, memory, programs):
        self.memory = memory
        self.programs = programs
        self.pc = 100
        self.mar = 0
        self.mdr = 0
        self.icr = 0
        self.uc = 0
        self.accumulator = 0
        self.alu = 0
        self.pause = False
        self.idInstruction = 100

    # This method takes an instruction and send it to CU for process it.
    def cycleController(self):
        sleep(1)
        self.mar = self.pc
        self.mdr = self.memory[self.pc]
        self.icr = self.mdr
        self.pc += 1
        self.controlUnity() # Here we called CU method and the magic start!
        # If this conditional is true, the following instruction will start processing automatically
        if self.memory[self.pc] != "" and not self.pause:
            self.cycleController()

    # This method just put each instruction into the memory and then execute all instruction
    def startCycle(self):
        for program in self.programs[:2]:
            self.pause = False
            currentProgram = open(program,"r")
            for line in currentProgram.readlines():
                self.memory[self.idInstruction] = line[:-1]
                self.idInstruction += 1
            self.cycleController()
            print(f"Fin de {program}")       
        self.concurrenceProcess()

    # This method exist because I need to execute two programs at same time
    # They interleave instructions following some rules 
    def concurrenceProcess(self):
        switch = True
        program3 = open(self.programs[-2],"r").readlines()
        program4 = open(self.programs[-1],"r").readlines()
        self.pause = False
        while True:
            if len(program3) == 0 and len(program4) == 0:
                break
            if switch:
                self.memory[self.idInstruction] = program3.pop(0)[:-1]
            else:
                self.memory[self.idInstruction] = program4.pop(0)[:-1]
            if self.memory[self.idInstruction][:3] == "END":
                    switch = not switch
            self.idInstruction += 1
        self.cycleController()
        print(f"Fin de {self.programs[-2]} y {self.programs[-1]}")

    # Here the magic happens!
    # The whole logic of the CU was expressed here
    # Each type of process and how they work 
    def controlUnity(self):
        self.uc = self.icr
        ucList = self.uc.split()
        addressMemory = lambda i : int(ucList[i][1:]) - 1
        match ucList[0]:
            case "SET":
                self.memory[addressMemory(1)] = int(ucList[2])
            case "LDR":
                self.mar = addressMemory(1)
                self.mdr = self.memory[self.mar]
                self.accumulator = self.mdr
            case "ADD":
                self.alu = self.accumulator
                self.mar = addressMemory(1)
                self.mdr = self.memory[self.mar]
                self.accumulator = self.mdr
                if(ucList[3] == "NULL"):
                    if(ucList[2] == "NULL"):
                        self.alu += self.accumulator
                        self.accumulator = self.alu
                    else:
                        self.accumulator = self.memory[addressMemory(1)]
                        self.alu = self.accumulator
                        self.accumulator = self.memory[addressMemory(2)]
                        self.alu += self.accumulator
                        self.accumulator = self.alu
                else:
                    self.accumulator = self.memory[addressMemory(1)]
                    self.alu = self.accumulator
                    self.accumulator = self.memory[addressMemory(2)]
                    self.alu += self.accumulator
                    self.accumulator = self.alu
                    self.memory[addressMemory(3)] = self.accumulator
            case "INC":
                self.mar = addressMemory(1)
                self.mdr = self.memory[self.mar]
                self.accumulator = self.mdr
                self.alu = self.accumulator + 1
                self.accumulator = self.alu
            case "DEC":
                self.mar = addressMemory(1)
                self.mdr = self.memory[self.mar]
                self.accumulator = self.mdr
                self.alu = self.accumulator - 1
                self.accumulator = self.alu
            case "STR":
                self.mar = addressMemory(1)
                self.mdr = self.accumulator
                self.memory[self.mar] = self.mdr
            case "SHW":
                match ucList[1]:
                    case "ACC":
                        print(f"Accumulator: {self.accumulator}")
                    case "ICR":
                        print(f"ICR: {self.icr}")
                    case "MAR":
                        print(f"MAR: {self.mar}")
                    case "MDR":
                        print(f"MDR: {self.mdr}")
                    case "UC":
                        print(f"UC: {self.uc}")
                    case _:
                        print(f"D{addressMemory(1) + 1}: {self.memory[addressMemory(1)]}")
            case "PAUSE":
                self.pause = True
            case "END":
                print("CONTEXT SWITCHING\n")