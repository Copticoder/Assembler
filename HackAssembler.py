from Parser import Parser
from Code import Code
import sys
class HackAssembler:
    def __init__(self, asmName) -> None:
        """
        Reads Progam.asm source file and creates a new file Program.hack which has the assembled machine code as a text file.
        The Assembly is implemented as two stages or two passes. The first pass scans the whole program and registers
        symbols in the symbol table. The second pass scans the whole program again substituting the symbols with their
        respective addresses in the symbol table, in addition to generating binary machine code and writing the resulting
        assembled machine code to a new file.
        Usage: python Assembler.py Program.asm
        """

        self.current_addr=16
        self.asmName=asmName
        self.codes=Code()
        self.asmfile=open(asmName,"r").readlines()
        self.parser=Parser(self.asmfile)
        self.symbolTable = dict()
        self.symbolTable.update({
            'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
            'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
            'SCREEN': 0x4000, 'KBD': 0x6000
        })
        self.instructions=""
    
    def firstPasser(self):
        """
        First compilation pass: Determine memory locations of label definitions: (LABEL).
        """
        self.parser.counter=-1
        line_counter=0
        while self.parser.advance():
            commandType=self.parser.commandType()
            if  commandType in ["A_Instruction","C_Instruction",None]:
                line_counter+=1
            else:
                self.symbolTable.update({self.parser.command:line_counter})
                
    
    def getValue(self):
        """get the value of the symbol or variable from the symbol table"""
        return self.symbolTable[self.parser.command]

    def secondPasser(self):
        """
        Second compilation pass: get variables to the symbol table and then Generate the hack machine code for each instruction.
        """

        self.parser.counter=-1
        self.parser.command=""
        while self.parser.advance():
            commandType=self.parser.commandType()
            if commandType== "A_Instruction":
                if not self.parser.command.isnumeric():
                    value=self.checkVarAddr()
                    self.executeA(value)
                else:
                    self.executeA(self.parser.command)
            elif commandType == "C_Instruction":
                self.executeC()
    
    def checkVarAddr(self):
        if self.parser.command not in self.symbolTable:
            self.symbolTable[self.parser.command]=self.current_addr
            self.current_addr+=1
        return self.symbolTable[self.parser.command]

    def executeA(self,address):
        binary=bin(int(address))[2:]
        self.instructions+="0"+(15-len(binary))*"0"+binary+"\n"
    
    def executeC(self):

        destination=self.parser.dest()
        computation=self.parser.comp()
        jump=self.parser.jump()
        destbits= self.codes.dest(destination)
        compbits=self.codes.comp(computation)
        jumpbits=self.codes.jump(jump)
        self.instructions+="111"+compbits+destbits+jumpbits+"\n"

    def assemble(self):
        self.firstPasser()
        self.secondPasser()
        
        hackfile = open(self.asmName.replace(".asm",".hack"), "w")
        hackfile.write(self.instructions)
        hackfile.close()



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python Assembler.py Program.asm")
    else:
        asm_file = sys.argv[1]

    hack_assembler = HackAssembler(asm_file)
    hack_assembler.assemble()
