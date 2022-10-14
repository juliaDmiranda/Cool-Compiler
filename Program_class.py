from enum import Enum,auto
from class_ import Token

class SIG (Enum):
    EndOfProgram    = auto()
    SkipToken       = auto()
    IsEqual         = auto()
    TokenNotFound   = auto()
    TokenFound      = auto()
    IsFormal        = True

class Program():
    def __init__(self, line):
        self.oldProgram = line
        self.program = line
        self.token      = line[0]
        self.bf      = line[0]
        self.err = []
        self.ps_err = []
        self.situation = False

    def nexToken(self, signal):
        if(self.program == []):
            self.addError()
            return SIG.EndOfProgram
        else:
            self.bf      = self.program[0]
            self.oldProgram = self.program
            self.program = self.program[1::]
            if(self.program == []):
                self.addError()
                self.situation = SIG.EndOfProgram
            else:
                self.situation = signal
                self.token = self.program[0]
                self.setPs_err()

    def afToken(self):
        try:
            return self.program[1]
        except IndexError:
            return self.program[0]
    def undo(self):
        self.program = self.oldProgram
        self.token  = self.program[0]

    def addError(self):
        self.err.append(self.ps_err)
        self.setPs_err() # zera o erro por não ocorreu exceção

    def setPs_err(self, error = []):
        self.ps_err = error
