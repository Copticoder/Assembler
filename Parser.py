import re

class Parser:
    def __init__(self,asmfile) -> None:
        """
        Parses the assembly program by looking ahead one or two tokens to determine the type of instruction. This is very
        naive and simple, it assumes there are no errors in the program source code and no invalid instructions are used.
        """
        self.asmfile=asmfile
        self.length=len(self.asmfile)-1
        self.command=""
        self.counter=-1

    def hasMoreCommands(self):
        """Checks if there are more commands in the asmfile"""
        self.counter+=1
        if self.counter > self.length:
            return False
        return True

    def dest(self):
        """gets the destination part from the c-instruction and checks if present"""
        dest=""
        if "=" in self.command[0]:
            self.command=self.command[0].split("=")
            dest=self.command.pop(0)
        return dest

    def comp(self):
        """gets the comp part from the c-instruction """

        comp=""
        if len(self.command):
            if ";" in self.command[0]:
                self.command=self.command[0].split(";")
            comp=self.command.pop(0)
        return comp

    def jump(self):
        """gets the jump part from the c-instruction and checks if present"""

        jump=""
        if len(self.command):
            jump=self.command.pop(0)
        return jump
        
    def advance(self):
        """proceed to the next instruction if present"""
        if self.hasMoreCommands():
            self.command=self.asmfile[self.counter]
            return True
        return False
    
    def splitAInstr(self):
        """splitting the A-Instruction on the @"""
        self.command=self.command[0].split("@")
        self.command=self.command[1]

                
    def commandType(self):
        """this method removes the whitespaces, endlines and the comments and checks the command type"""
        self.removeCommentsEL()
        if len(self.command)>1:
            self.command=[self.command[0]]
        self.removeWhiteSpaces()
        template=self.command.copy()
        self.command=[template[char] for char in range(len(template)) if template[char]]
        if not len(self.command):
            return None

        if self.command[0][0]=="@":
            self.splitAInstr()
            return "A_Instruction"

        if self.command[0][0]=="(":
            self.command=re.sub("[(|)]","",self.command[0])
            return "L_Instruction"
        
        return "C_Instruction"

    def removeCommentsEL(self):
        """replaces the spaces and removes the endlines and comments"""
        self.command=self.command.replace(" ","")    
        self.command=self.command.strip("\n").split("//")    
    
    def removeWhiteSpaces(self):
        """further remove the whitespaces"""
        self.command=self.command[0].split(" ")

            
        

# parser=Parser('PongL.asm')
# while parser.advance():
#     parser.getInstruction()

# f = open("PongL.hack", "w")
# f.write(parser.instructions)
# f.close()